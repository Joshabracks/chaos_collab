from django.shortcuts import render, redirect
from apps.main_app.models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'main_app/index.html')

def register(request):
    errors = User.objects.validate_user(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    info = request.POST
    hash1 = bcrypt.hashpw(info['password'].encode(), bcrypt.gensalt())
    new_user = User.objects.create(
        name = info['name'],
        screen_name = info['screen_name'],
        email = info['email'],
        password = hash1,
        )
    request.session['user'] = new_user.id
    context = {
        'user': new_user,
    }
    return render(request, 'main_app/main.html', context)

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    user = User.objects.get(email = request.POST['email'])
    request.session['user'] = user.id
    return redirect('/')

def logout(request):
    del request.session['user']
    return redirect('/')

def look(request):
    return render(request, 'main_app/now.html')














def canvas(request):
    colors = chromatic(17)

    context = {
        'colors': colors,
        'limit': get_limit(),
    }
    return render(request, 'main_app/canvas.html', context)

def chromatic(divisor):
    colors = []
    for r in range(0, 255, divisor):
        for g in range(0, 255, divisor):
            for b in range(0, 255, divisor):
                hue = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
                colors.append(hue)
    return colors

def get_limit():
    arr = []
    for i in range(225):
        arr.append('Carl')
    return arr
