from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from . import forms
from django.contrib.auth.models import User
from SA_Label_System.models import User_Basic_Info
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.template import RequestContext
from .DataLoader import DataLoader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from . import models
from django.utils import timezone
from django.contrib.auth import logout

# Create your views here.

def index(request):
    #data_loader = DataLoader()
    #data_loader.clean_files()
    #data_loader.load_dataset()
    return render(request, 'SA_Label_System/index.html')


def add_project(request):
    if not request.user.is_authenticated():
        return render(request, 'SA_Label_System/signin.html')
    if request.method == 'POST':
        project_name = request.POST['project-name']
        data_loader = DataLoader()
        data_loader.clean_project_files(project_name)
        data_loader.load_project_dataset(project_name)
        msg_id = 1
        return render(request, 'SA_Label_System/inform.html',{'msg_id':msg_id, 'project_name':project_name})
    return render(request, 'SA_Label_System/add_project.html')


def signin(request):
    if request.user.is_authenticated():
        username = request.user.username
        current_user_info = models.User_Basic_Info.objects.filter(username=username)[0]
        current_user_setting = models.User_Setting.objects.filter(user_basic_info=current_user_info)[0]
        # print('11111111111111111111111')
        #print(type(current_user_setting.project_select))
        if current_user_setting.project_select == '.':
            return redirect('/project_select')
        return redirect('/label')
    if request.method == 'POST':
        username = request.POST['input_username']
        password = request.POST['input_password']
        error_id = 0
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #return render(request, 'SA_Label_System/label.html')
                current_user_info = models.User_Basic_Info.objects.filter(username=username)[0]
                current_user_setting = models.User_Setting.objects.filter(user_basic_info=current_user_info)[0]
                #print('11111111111111111111111')
                if current_user_setting.project_select == '.':
                    return redirect('/project_select')
                return redirect('/label')
            else:
                error_id = 2  # this account is blocked
                return render(request, 'SA_Label_System/error.html', {'error_id':error_id})
        else:
            error_id = 1  # the account does not exist
            return render(request, 'SA_Label_System/error.html', {'error_id':error_id})
    return render(request, 'SA_Label_System/signin.html')


def user_logout(request):
    logout(request)
    error_id = 4
    return render(request, 'SA_Label_System/error.html', {'error_id':error_id})


def signup(request):
    return render(request, 'SA_Label_System/signup.html')



def signup_create_user(request):
    if request.method == 'POST':
        form = forms.signup_form(request.POST)
        if request.POST['input_password'] != request.POST['confirm_password']:
            error_id = 3
            return render(request, 'SA_Label_System/error.html', {'error_id':error_id})
        if form.is_valid():
            user_info = models.User_Basic_Info.objects.filter(username=request.POST['input_username'])
            print(user_info)
            if user_info or form.cleaned_data['input_username']=='sph':
                error_id = 5
                return render(request, 'SA_Label_System/error.html', {'error_id':error_id})
            new_user = User.objects.create_user(username=form.cleaned_data['input_username'], email=form.cleaned_data['input_email'], password=form.cleaned_data['input_password'])
            new_user.save()
            new_user = User_Basic_Info(username=form.cleaned_data['input_username'], nickname='nickname', email_address=form.cleaned_data['input_email'], password=form.cleaned_data['input_password'], label_count=0)
            new_user.save()
            new_user_settings = models.User_Setting(user_basic_info=new_user)
            new_user_settings.save()
            return render(request, 'SA_Label_System/signin.html', {'username':form.cleaned_data['input_username']})
        else:
            print('form is invalid')
    return render(request, 'SA_Label_System/signup.html')


def project_select(request):
    if not models.Label_Project.objects.all().exists():
        msg_id = 2
        return render(request, 'SA_Label_System/inform.html', {'msg_id':msg_id})
    #print('enter label')
    if not request.user.is_authenticated():
        return render(request, 'SA_Label_System/signin.html')
    #print('111111111111111111')
    if request.method == 'POST':
        project_name = request.POST['project_select']
        #print(project_name)
        current_username = request.user.username
        current_user_info = models.User_Basic_Info.objects.get(username=current_username)  # get the current username
        current_user_settings = models.User_Setting.objects.filter(user_basic_info=current_user_info)[0]  # get current user settings
        #label_project_info = models.Label_Project.objects.filter(project_name=project_name)[0]
        current_user_settings.project_select = project_name
        current_user_settings.save()
        #print('222222222222222222222')
        return redirect('/label')
    #print('33333333333333333333')
    projects = models.Label_Project.objects.all()
    return render(request, 'SA_Label_System/carousel.html', {'projects':projects})



def label_style_2(request):
    if not models.Label_Project.objects.all().exists():
        msg_id = 2
        return render(request, 'SA_Label_System/inform.html', {'msg_id':msg_id})

    if not request.user.is_authenticated():
        return render(request, 'SA_Label_System/signin.html')
    if request.method == 'POST':
        #print('label post')
        current_username = request.user.username  #get the current username
        #print(current_username)
        base_image_path = request.POST['absolute_base_image_path']
        label_image_path = request.POST['absolute_label_image_path']
        #print(base_image_path)
        #print(label_image_path)
        current_user_info = models.User_Basic_Info.objects.get(username=current_username)  #get the current username
        #print(current_user_info)
        current_user_info.label_count += 1
        current_user_info.save()
        label_image_info = models.Image_Basic_Info.objects.get(image_path=label_image_path)
        base_image_info = models.Image_Basic_Info.objects.get(image_path=base_image_path)
        #print(current_user_info)
        #print(label_image_info)
        #print(base_image_info)
        label_image_info.image_label_count += 1
        label_image_info.save()
        #print(label_image_info.image_label_count)
        #print(current_user_info.id)
        #print(label_image_info.id)
        #print(models.Image_Label_Count.objects.all())
        #image_label_count_info = models.Image_Label_Count.objects.all()
        #print(image_label_count_info)
        image_label_count_info = models.Image_Label_Count.objects.filter(user_id=current_user_info.id, image_id=label_image_info.id)
        #print('1111111111111')
        if not image_label_count_info:  #if not exists
            #print('22222222222222')
            image_label_count_info = models.Image_Label_Count(user_id=current_user_info, image_id=label_image_info, user_label_count=1)
            image_label_count_info.save()
            #print('3333333333333333333')
        else:
            image_label_count_info = image_label_count_info[0]
            #print(image_label_count_info)
            image_label_count_info.user_label_count += 1
            image_label_count_info.save()

        image_label_info = models.Image_Label_Info(label_image_id=label_image_info, base_image_id=base_image_info, user_id=current_user_info, image_score=float(request.POST['score']), label_time=timezone.now())
        image_label_info.save()

        return redirect('/label_style_2')
    current_username = request.user.username
    current_user_info = models.User_Basic_Info.objects.filter(username=current_username)[0]
    current_user_settings = models.User_Setting.objects.filter(user_basic_info=current_user_info)[0]
    current_project = current_user_settings.project_select
    data_loader = DataLoader()
    data_loader.generate_project_images_path(current_project)
    base_image_path = data_loader.get_base_image_path()
    label_image_path = data_loader.get_label_image_path()
    absolute_base_image_path = data_loader.get_absolute_base_image_path()
    absolute_label_image_path = data_loader.get_absolute_label_image_path()
    return render(request, 'SA_Label_System/label_style_2.html', {'base_image_path':base_image_path, 'label_image_path':label_image_path, 'absolute_base_image_path':absolute_base_image_path, 'absolute_label_image_path':absolute_label_image_path})




def label(request):
    #print('enter label')
    if not models.Label_Project.objects.all().exists():
        msg_id = 2
        return render(request, 'SA_Label_System/inform.html', {'msg_id':msg_id})
    if not request.user.is_authenticated():
        return render(request, 'SA_Label_System/signin.html')
    if request.method == 'POST':
        #print('label post')
        current_username = request.user.username  #get the current username
        #print(current_username)
        base_image_path = request.POST['absolute_base_image_path']
        label_image_path = request.POST['absolute_label_image_path']
        #print(base_image_path)
        #print(label_image_path)
        current_user_info = models.User_Basic_Info.objects.get(username=current_username)  #get the current username
        #print(current_user_info)
        current_user_info.label_count += 1
        current_user_info.save()
        label_image_info = models.Image_Basic_Info.objects.get(image_path=label_image_path)
        base_image_info = models.Image_Basic_Info.objects.get(image_path=base_image_path)
        #print(current_user_info)
        #print(label_image_info)
        #print(base_image_info)
        label_image_info.image_label_count += 1
        label_image_info.save()
        #print(label_image_info.image_label_count)
        #print(current_user_info.id)
        #print(label_image_info.id)
        #print(models.Image_Label_Count.objects.all())
        #image_label_count_info = models.Image_Label_Count.objects.all()
        #print(image_label_count_info)
        image_label_count_info = models.Image_Label_Count.objects.filter(user_id=current_user_info.id, image_id=label_image_info.id)
        #print('1111111111111')
        if not image_label_count_info:  #if not exists
            #print('22222222222222')
            image_label_count_info = models.Image_Label_Count(user_id=current_user_info, image_id=label_image_info, user_label_count=1)
            image_label_count_info.save()
            #print('3333333333333333333')
        else:
            image_label_count_info = image_label_count_info[0]
            #print(image_label_count_info)
            image_label_count_info.user_label_count += 1
            image_label_count_info.save()
            #print('444444444444444444')
        #print('55555555555555555555')
        #print(image_label_count_info.user_label_count)
        #image_label_info = models.Image_Label_Info.objects.filter(label_image_id=label_image_info, base_image_id=base_image_info)
        #print(image_label_info)
        #if not image_label_info:
            #print('666666666666666666')
        image_label_info = models.Image_Label_Info(label_image_id=label_image_info, base_image_id=base_image_info, user_id=current_user_info, image_score=float(request.POST['score']), label_time=timezone.now())
        image_label_info.save()
        #else:
            #print('77777777777777777777')
            #image_label_info = image_label_info[0]
            #image_label_info.image_score = float(request.POST['score'])
            #image_label_info.label_time = timezone.now()
            #image_label_info.save()
        #print(image_label_info.label_time)
        #print('888888888888888888888')
        return redirect('/label')

    #print('dataloader')
    current_username = request.user.username
    current_user_info = models.User_Basic_Info.objects.filter(username=current_username)[0]
    current_user_settings = models.User_Setting.objects.filter(user_basic_info=current_user_info)[0]
    current_project = current_user_settings.project_select
    print(current_project)
    data_loader = DataLoader()
    data_loader.generate_project_images_path(current_project)

    base_image_path = data_loader.get_base_image_path()
    label_image_path = data_loader.get_label_image_path()
    absolute_base_image_path = data_loader.get_absolute_base_image_path()
    absolute_label_image_path = data_loader.get_absolute_label_image_path()
    return render(request, 'SA_Label_System/label.html', {'base_image_path':base_image_path, 'label_image_path':label_image_path, 'absolute_base_image_path':absolute_base_image_path, 'absolute_label_image_path':absolute_label_image_path})




