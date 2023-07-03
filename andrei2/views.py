from django.shortcuts import render,redirect
from  django.contrib.auth import authenticate,login, logout
from django.contrib import messages
# # Create your vie ws here.
# def login_user(request):
#     return render(request, 'auth/login.html',{})
# def login_user2(request):
#     return render(request, 'auth/login2.html',{})