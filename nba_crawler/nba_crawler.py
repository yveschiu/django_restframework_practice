from bs4 import BeautifulSoup
import requests
import os
import pymysql
from time import strptime
from datetime import datetime
import mysql_secret
import News


headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

base_url = "https://nba.udn.com"
index_url = "nba/index?gr=www"

url = os.path.join(base_url, index_url)
# print(url)

def get_news_urls():
    news_urls_list = []
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, features="html.parser")
    news_body = soup.select_one("#news_body").select("dt")[0:3]
    for news in news_body:
        news_url = base_url + news.select_one("a").get("href")
        news_urls_list.append(news_url)
        # print(news_url)
    return news_urls_list


def check_uncrawled_news_urls(news_urls_list):
    uncrawled_news_urls_list = []
    conn = pymysql.connect(host=mysql_secret.host,
                           user=mysql_secret.user,
                           passwd=mysql_secret.password,
                           db=mysql_secret.db)
    cur = conn.cursor()

    urls_query = "select url from api_news"

    cur.execute(urls_query)

    query_result_urls_list = [ url[0] for url in cur ]

    for news_url in news_urls_list:
        if news_url not in query_result_urls_list:
            uncrawled_news_urls_list.append(news_url)
        else:
            # print("+"*20)
            # print("inside check_uncrawled_news_urls:")
            print(news_url, "is already crawled.")

    return uncrawled_news_urls_list


def get_news_contents(news_urls_list):
    news_insertion_list = []
    for news_url in news_urls_list:
        resp = requests.get(news_url, headers=headers)
        soup = BeautifulSoup(resp.text, features="html.parser")
        story_body_content = soup.select_one("#story_body_content")

        story_title = story_body_content.select_one(".story_art_title").text
        published_time = story_body_content.select_one(".shareBar__info--author").select_one("span").text
        published_time = strptime(published_time, "%Y-%m-%d %H:%M")

        tmp_news_source = story_body_content.select_one(".shareBar__info--author").text[16:].replace("／", "/").replace("╱", "/").split("/")
        # print(tmp_news_source)
        if len(tmp_news_source) == 3:
            news_source = tmp_news_source[0].strip()
            news_reporter = tmp_news_source[1].strip()
            news_type = tmp_news_source[2].strip()
        elif len(tmp_news_source) == 2: # 缺少記者
            news_source = tmp_news_source[0].strip()
            news_reporter = None
            news_type = tmp_news_source[1].strip()
        else: # 格式不符
            news_source = None
            news_reporter = None
            news_type = None


        story_content = []
        for p in story_body_content.select("p"):
            if not p.text == "":
                story_content.append(p.text.strip())
        article = "\n".join(story_content[1:])

        news = News.News()
        news.title = story_title
        news.url = news_url
        news.published_time = published_time
        news.news_source = news_source
        news.news_reporter = news_reporter
        news.news_type = news_type
        news.news_content = article

        news_insertion_list.append(news)

        print(story_title)
        print(news_url)

    return news_insertion_list


def insert_to_mysql(news_insertion_list):
    conn = pymysql.connect(host=mysql_secret.host,
                           user=mysql_secret.user,
                           passwd=mysql_secret.password,
                           db=mysql_secret.db)
    print("connected to MySQL")
    cur = conn.cursor()

    insert_query = """
                INSERT INTO api_news(title, url, published_time, news_source, news_reporter, news_type, news_content) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    # print(insert_query)

    for news in news_insertion_list:
        try:
            cur.execute(insert_query,
                        (news.title, news.url, news.published_time, news.news_source, news.news_reporter, news.news_type, news.news_content))
            conn.commit()
            print("good query")
        except:
            print("something wrong with mysql")

    cur.close()
    conn.close()
    print("MySQL connection closed")


if __name__ == "__main__":

    news_urls_list = get_news_urls()
    print(news_urls_list)
    print("-----")
    news_to_crawl = check_uncrawled_news_urls(news_urls_list)
    print("News to crawl:", news_to_crawl)
    print(len(news_to_crawl))
    if len(news_to_crawl) == 0:
        print("There is no latest news at", datetime.now())
    else:
        news_insertion_list = get_news_contents(news_to_crawl)
        insert_to_mysql(news_insertion_list)
    print("crawler finished")
