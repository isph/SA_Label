import os
import random
from . import global_data
from django.conf import settings
from . import models
from django.utils import timezone


class DataLoader(object):
    def __init__(self):
        self.base_dir = settings.BASE_DIR+'/SA_Label_System/static/SA_Label_System/img/'
        #self.base_dir = settings.STATIC_URL+'SA_Label_System/img/'
        self.base_image_file = ''
        self.label_image_file = ''
        self.absolute_base_image_path = ''
        self.absolute_label_image_path = ''
        self.base_image_name = global_data.base_image_name

    def clean_project_files(self, project_folder):
        project_name = models.Label_Project.objects.filter(project_name=project_folder)
        # print(project_name)
        if project_name:  # if the project does not exists
            return
        base_dir = self.base_dir+project_folder+'/'
        folders = os.listdir(base_dir)
        for folder in folders:
            folder_path = base_dir+folder+'/'
            images = os.listdir(folder_path)
            for image in images:
                if image.startswith('.'):
                    os.remove(os.path.join(folder_path, image))
                    print("Delete File: " + os.path.join(folder_path, image))


    def load_project_dataset(self, project_folder):
        project_name = models.Label_Project.objects.filter(project_name=project_folder)
        #print(project_name)
        if not project_name:  # if the project does not exists
            base_dir = self.base_dir + project_folder+'/'
            folders = os.listdir(base_dir)  # list all folders
            folders_len = len(folders)
            project_object = models.Label_Project(project_name=project_folder, project_time=timezone.now(), group_num=folders_len)
            project_object.save()
            project_images_num = 0
            for folder in folders:
                images = os.listdir(base_dir+folder+'/')  #list all image in the folder
                project_images_num += len(images)
                project_group = models.Project_Group(project_name=project_object, group_name=folder, group_images_num=len(images))
                project_group.save()
                for image in images:
                    image_full_path = base_dir+folder+'/'+image
                    image_type = 1
                    if image == global_data.base_image_name:
                        image_type = 0
                    image_base_info = models.Image_Basic_Info(image_name=image, image_path=image_full_path, image_group=project_group, image_type=image_type, image_project=project_object)
                    image_base_info.save()  #save the image basic information to database
            project_object.project_images_num = project_images_num
            project_object.save()
            print('end load data')

    def load_dataset(self):
        projects = os.listdir(self.base_dir)  #list all projects
        print(projects)
        for project in projects:
            project_name = models.Label_Project.objects.filter(project_name=project)
            #print(project_name)
            if not project_name:  # if the project does not exists
                base_dir = self.base_dir + project+'/'
                folders = os.listdir(base_dir)  # list all folders
                folders_len = len(folders)
                project_object = models.Label_Project(project_name=project, project_time=timezone.now(), group_num=folders_len)
                project_object.save()
                project_images_num = 0
                for folder in folders:
                    images = os.listdir(base_dir+folder+'/')  #list all image in the folder
                    project_images_num += len(images)
                    project_group = models.Project_Group(project_name=project_object, group_name=folder, group_images_num=len(images))
                    project_group.save()
                    for image in images:
                        image_full_path = base_dir+folder+'/'+image
                        image_type = 1
                        if image == global_data.base_image_name:
                            image_type = 0
                        image_base_info = models.Image_Basic_Info(image_name=image, image_path=image_full_path, image_group=project_group, image_type=image_type, image_project=project_object)
                        image_base_info.save()  #save the image basic information to database
                project_object.project_images_num = project_images_num
                project_object.save()
            print('end load data')

    def get_base_image_path(self):
        return self.base_image_file

    def get_label_image_path(self):
        return self.label_image_file

    def get_absolute_base_image_path(self):
        return self.absolute_base_image_path

    def get_absolute_label_image_path(self):
        return self.absolute_label_image_path

    def generate_project_images_path(self, project_folder):
        base_project = project_folder
        base_dir = self.base_dir+base_project
        project_object = models.Label_Project.objects.get(project_name=base_project)
        #base_image = models.Image_Basic_Info.objects.filter(image_project=project_object, image_type=0)
        #base_image_len = len(base_image)


        label_image_list = models.Image_Basic_Info.objects.filter(image_project=project_object, image_type=1, image_label_count__lt=6)  #get images which labeled times < 6
        label_image_len = len(label_image_list)
        random_num = random.randint(0, label_image_len-1)
        label_image_info = label_image_list[random_num]
        label_image_file = label_image_info.image_path
        path, filename = os.path.split(label_image_file)
        base_image_file = path+'/'+self.base_image_name
        self.absolute_label_image_path = label_image_file
        self.absolute_base_image_path = base_image_file
        self.base_image_file = '../../static/SA_Label_System/img/'+base_project+'/'+label_image_info.image_group.group_name+'/'+self.base_image_name
        self.label_image_file = '../../static/SA_Label_System/img/'+base_project+'/'+label_image_info.image_group.group_name+'/'+filename



        #folders = os.listdir(base_dir)
        #folders_len = len(folders)  #get the length of folders
        #rand_folder_num = random.randint(0, folders_len-1)
        #folders_dir = self.base_dir + folders[rand_folder_num] + '/'#get folder path
        #self.base_image_path = '../../static/SA_Label_System/img/'+folders[rand_folder_num]+ '/0.png'
        #images = os.listdir(folders_dir)  #get all images
        #self.base_image_path = '../../static/SA_Label_System/img/' + folders[rand_folder_num] + '/' + images[0]
        #self.absolute_base_image_path = self.base_dir + folders[rand_folder_num] + '/' + images[0]
        #images_len = len(images)
        #rand_image_num = random.randint(1, images_len-1)
        #self.label_image_path = '../../static/SA_Label_System/img/'+folders[rand_folder_num]+ '/' + images[rand_image_num]  #get the label image path
        #self.absolute_label_image_path = self.base_dir+folders[rand_folder_num] + '/' + images[rand_image_num]