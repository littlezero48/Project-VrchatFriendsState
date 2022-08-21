import threading
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from .models import vrchatLogin, vrchatFriends
# import se

def index(request):
    return render(request, 'index.html')

def login(request):

    global vrchatLoginTest
    global loginState
    usrId = request.POST.get('username')
    usrPw = request.POST.get('password')

    request.session['id'] = usrId

    vrchatLoginTest, loginState = vrchatLogin.vrchatLoginID(usrId,usrPw)

    if vrchatLoginTest != None and loginState == 'success':
        return friendslist(request, vrchatLoginTest)
    # elif searchName != '' :
    #     print(2, id(vrchatLoginTest))
    #     return friendslist(request, vrchatLoginTest, searchName)
    else:
        return render(request, 'login.html', {'loginState' : loginState})


def friendslist(request, vrchatLoginTest):


    vrFriends = vrchatFriends()
    context = vrFriends.vrchatFriends(vrchatLoginTest)

    return render(request, 'friendslist.html', {'context' : context})

