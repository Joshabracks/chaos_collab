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
    try:
        user = User.objects.filter(id = request.session['user'])
    except:
        user = 'no_user'
    if user == 'no_user':
        return render(request, 'main_app/index.html')
    return redirect('/landing')

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
        alias = info['alias'],
        email = info['email'],
        password = hash1,
        )
    request.session['user'] = new_user.id
    context = {
        'user': new_user,
    }
    return redirect('/')

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
        'collabs': Collab.objects.all(),
        'user': User.objects.get(id = request.session['user'])
    }
    return render(request, 'main_app/now.html', context)

def landing(request):
    context = {
        'collabs': Collab.objects.all(),
        'user': User.objects.get(id = request.session['user'])
    }
    return render(request, 'main_app/landing.html', context)

def view_user(request, user_id):
    context = {
        'user_id': User.objects.get(id = user_id),
        'user': User.objects.get(id = request.session['user']),
    }
    return render(request, 'main_app/view_user.html', context)

def post_comment(request):
    Comment.objects.create(
        content = request.POST['content'],
        collab = Collab.objects.get(id = request.POST['collab']),
        user = User.objects.get(id = request.session['user'])
    )
    return redirect(f"/collab/{request.POST['collab']}")



def canvas(request, collab_id):
    request.session['collab'] = 'no_collab'
    request.session['collab'] = collab_id
    colors = chromatic(51)
    color_strs = []
    context = {
        'colors': colors,
        'color_str': " ".join(colors),
        'limit': get_limit(),
        'image_state': Collab.objects.get(id = collab_id).encoded_img,
        'collab': Collab.objects.get(id = collab_id),
        'user': User.objects.get(id = request.session['user'])
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
    return colors

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
    filename = f'{len(Collab.objects.all())+1}.png'
    with open('apps/main_app/static/main_app/images/'+filename, 'wb') as f:
        f.write(image_data)
    Collab.objects.create(
        title = 'Title',
        description = 'Temporary description',
        uploaded_by = User.objects.get(id = request.session['user']),
        encoded_img = request.POST['encoded_img'],
        decoded_img = filename,
        parent = request.POST['parent_id'],
    )
    return()


def view_collab(request, collab_id):
    collab = Collab.objects.get(id = collab_id)
    context = {
        'collab': Collab.objects.get(id = collab_id),
        'user': User.objects.get(id = request.session['user']),
        'parent': Collab.objects.get(id = collab.parent),
        'children': Collab.objects.filter(parent = collab_id),
        'comments': Comment.objects.filter(collab = collab_id),
    }
    return render(request, 'main_app/view_collab.html', context)

def set_avatar(request, collab_id, user_id):
    user = User.objects.get(id = user_id)
    user.avatar = collab_id
    user.save()
    return redirect('/landing')

def rename_collab(request, collab_id):
    collab = Collab.objects.get(id = collab_id)
    collab.title = request.POST['rename']
    collab.save()
    return redirect(f'/collab/{collab_id}')


    # format, imgstr = data.split(baseimagecode) 
    # ext = format.split('/')[-1]
    # data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)