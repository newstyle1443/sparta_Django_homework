from django.shortcuts import render, redirect
from . models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
# user/views.py
def sign_up_view(request):
    user = request.user.is_authenticated
    if request.method == 'GET': # GET 메서드로 요청이 들어 올 경우
        if not user:
            return render(request, 'user/signup.html')
        else:
            return redirect ('/')
    elif request.method == 'POST': # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)

        if password != password2:
            return render(request, 'user/signup.html')

        else:
            exist_user =  get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
            return redirect('/sign-in')
    
def sign_in_view(request):
    user = request.user.is_authenticated
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        me = authenticate(username=username, password=password)
        if me:
            auth.login(request,me)
            return redirect('/')
        else:
            return redirect('/sign-in')
    elif request.method == 'GET':
        if not user:
            return render(request, 'user/signin.html')
        else:
            return redirect('/')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')