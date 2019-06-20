from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
import json
import requests

@csrf_exempt
def app_login(request, *args, **kwargs):
    error_msg = {}
    error_msg['success'] = False

    def try_auth(username, password):
        try:
            user = authenticate(username=username, password=password)
            if not user:
                print('no user')
                raise ValueError('Invalid login credentials!')
        except ValueError as e:
            print('caught invalid cred')
            error_msg['message'] = str(e)
        else:
            print('no error')
            error_msg['success'] = True
            error_msg['message'] = "Authentication successful"
            login(request,user)
   
    if request.method=='POST':
        req_data = json.loads(request.body.decode('UTF-8'))
        username = req_data['username']
        email = req_data['email']
        password = req_data['password']   
        try_auth(username,password)        
    else:  
        error_msg['message'] = "Bad request"
    return JsonResponse(error_msg)

@csrf_exempt
def app_register(request):
    error_msg = {}
    error_msg['success'] = False
    if request.method=='POST':
        req_data = json.loads(request.body.decode('UTF-8'))
        username = req_data['username']
        email = req_data['email']
        password = req_data['password']

        try:
            user = User.objects.filter(username=username)
            if user:
                raise ValueError('Found an existing account with given username')
        except:
            # cred = {'username':username, 'password':password}
            # res = requests.get('http://127.0.0.1:8000/login/',cred) #a forced get request
            res = app_login(request) #POST request
            error_msg = res.content
            decoded_error_msg = error_msg.decode('utf-8')
            error_msg = json.loads(decoded_error_msg)
            print(error_msg)
            if error_msg['success'] == False:
                error_msg['message']="""An account with this username already exists.
                 If that's your account try again with valid password, else try another username."""
            else:
                temp_msg = error_msg['message']
                error_msg['message'] = 'You already have a account with give credentials. Redirecting to signin. '+str(temp_msg)
       
        else:
            user = User()
            user.username = username
            user.set_password(password)
            user.email = email
            user.save()
            error_msg['success'] = True
            error_msg['message'] = "Registration successful"

    else:
        error_msg['message'] = "Bad request"
    return JsonResponse(error_msg)


def app_logout(request):
	logout(request)
	return JsonResponse({'success':True,
						 'message':'User logged out successsfully'})