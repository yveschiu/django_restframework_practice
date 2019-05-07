from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from .models import News
from rest_framework import viewsets
# from nba.quickstart.serializers import UserSerializer, GroupSerializer
from .serializers import UserSerializer, GroupSerializer,NewsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows news to be viewed or edited.
    """
    queryset = News.objects.all().order_by("-published_time")
    serializer_class = NewsSerializer


# ajax test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def ajax_list(request):
    print(request.GET.get('name'))
    print(request.GET.get("time"))
    a = range(100)
    return JsonResponse(list(a), safe=False)


def ajax_dict(request):
    is_ajax = False
    if request.is_ajax():
        is_ajax = True
    name_dict = {'twz': 'Love python and Django',
                 'zqxt': 'I am teaching Django', 'is_ajax': is_ajax}
    return JsonResponse(name_dict)


def ajax_jquery(request):
    print(request.GET.getlist('b[]'))
    is_ajax = False
    if request.is_ajax():
        is_ajax = True
    test = {'GET': 'GET',
            'array': [1, 2, 3, 4],
            'a': request.GET['a'],
            'b[]': request.GET.getlist('b[]'),
            'is_ajax': is_ajax,
            }
    return JsonResponse(test)


# @csrf_exempt #忽略 csrf
def ajax_jquery_POST(request):
    print(request.POST.getlist('b[]'))
    is_ajax = False
    if request.is_ajax():
        is_ajax = True
    test = {'POST': 'POST',
            'array': [1, 2, 3, 4],
            'a': request.POST['a'],
            'b[]': request.POST.getlist('b[]'),
            'is_ajax': is_ajax,
            }
    return JsonResponse(test)


# @csrf_exempt #忽略 csrf
def ajax_jquery_sample(request):
    print(request.POST.getlist('b[]'))
    is_ajax = False
    if request.is_ajax():
        is_ajax = True
    test = {'POST': 'POST',
            'array': [1, 2, 3, 4],
            'a': request.POST['a'],
            'b[]': request.POST.getlist('b[]'),
            'is_ajax': is_ajax,
            }
    return JsonResponse(test)
