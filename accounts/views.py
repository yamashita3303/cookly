from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from .models import CustomUser

def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)

def signup(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    new_user = CustomUser(username=username, email=email, password=password)
    new_user.save()
    return HttpResponse('ユーザーの作成に成功しました')

def signin(request):
    username = request.POST['username']
    password = request.POST['password']

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return HttpResponse('ログインに失敗しました')

    if user.password == password:
        login(request, user)  # これを実行するとユーザをログイン状態にできる
        return HttpResponseRedirect('/accounts')
    else:
        return HttpResponse('ログインに失敗しました')
    
def signout(request):
    logout(request)
    return HttpResponseRedirect('/accounts')