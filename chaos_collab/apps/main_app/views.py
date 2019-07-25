from django.shortcuts import render, redirect
from apps.main_app.models import *
from django.contrib import messages
import bcrypt
import base64
from base64 import b64decode
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import render
 


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
    context = {
        'collabs': Collab.objects.all()
    }
    return render(request, 'main_app/now.html', context)














def canvas(request):
    colors = chromatic(51)

    color_strs = []
     



    context = {
        'colors': colors,
        'color_str': " ".join(colors),
        'limit': get_limit(),
    }
    return render(request, 'main_app/canvas.html', context)

def chromatic(divisor):

    grays = []
    bluegreens = []
    blues = []
    bluereds = []
    redblues = []
    reds = []
    redgreens =[]
    greenreds = []
    greens = []
    greenblues = []
    colors = []

    for r in range(0, 256, divisor):
        for g in range(0, 256, divisor):
            for b in range(0, 256, divisor):
                hue = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
                if (b == r) and (b == g):
                    grays.append(hue)
                else:
                    colors.append(hue)
    for i in grays:
        colors.append(i)
                # elif ((b == r) and (b > g)) or ((b == g) and (b > r)):
                #     if r == g:
                #         blues.append(hue)
                #     if r > g:
                #         bluereds.append(hue)
                #     else:
                #         bluegreens.append(hue)
                    
                # elif ((r == b) and (r > g)) or ((r == g) and (r > b)):
                #     if b == g:
                #         reds.append(hue)
                #     if b > g:
                #         redblues.append(hue)
                #     else:
                #         redgreens.append(hue)
                # else:
                #     if r == b:
                #         greens.append(hue)
                #     if r > b:
                #         greenreds.append(hue)
                #     else:
                #         greenblues.append(hue)  

    
    # for i in grays:
    #     colors.append(i)
    # for i in greens:
    #     colors.append(i)
    # for i in greenblues:
    #     colors.append(i)
    # for i in bluegreens:
    #     colors.append(i)
    # for i in blues:
    #     colors.append(i)   
    # for i in bluereds:
    #     colors.append(i)
    # for i in redblues:
    #     colors.append(i)
    # for i in reds:
    #     colors.append(i)
    # for i in redgreens:
    #     colors.append(i)
    # for i in greenreds:
    #     colors.append(i)

    return colors

    # def chromatic(divisor):
    # colors = []
    # for r in range(0, 255, divisor):
    #     for g in range(0, 255, divisor):
    #         for b in range(0, 255, divisor):
    #             hue = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
    #             colors.append(hue)
    # return colors

def get_limit():
    arr = []
    for i in range(225):
        arr.append('Carl')
    return arr

def create_collab(request):
    
    split_data = request.POST['encoded_img'].split('data:image/png;base64,')
    print(split_data)
    print('*'*50)
    image_data = b64decode(split_data[1])
    filename = f'{len(Collab.objects.all())}.png'
    with open('apps/main_app/static/main_app/images/'+filename, 'wb') as f:
        f.write(image_data)
    Collab.objects.create(
        title = 'Title',
        description = 'Temporary description',
        encoded_img = request.POST['encoded_img'],
        decoded_img = filename,
    )
    return()






    # format, imgstr = data.split(baseimagecode) 
    # ext = format.split('/')[-1]
    # data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)