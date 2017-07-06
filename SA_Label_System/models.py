from django.db import models

# Create your models here.

class Label_Project(models.Model):
    project_name = models.CharField(max_length=200)
    project_time = models.DateTimeField()
    group_num = models.IntegerField(default=1)
    project_images_num = models.IntegerField(default=1)
    def __str__(self):
        return 'project_name: ' + self.project_name + '$'+'group_num: '+str(self.group_num)+'$'+'images_num: '+str(self.project_images_num)


class Project_Group(models.Model):
    project_name = models.ForeignKey(Label_Project, related_name='pg_project_name')
    group_name = models.CharField(max_length=200)  #the group name
    #group_num = models.ForeignKey(Label_Project, related_name='pg_group_num')
    group_images_num = models.IntegerField(default=1)  #how many images in this group
    group_labeled_num = models.IntegerField(default=0)

    def __str__(self):
        return 'project_name: '+self.project_name.project_name+'#'+'group_name: '+self.group_name+'#'+'group_images_num: '+str(self.group_images_num)+'#'+'group_labeled_num:'+str(self.group_labeled_num)


class Image_Basic_Info(models.Model):
    image_name = models.CharField(max_length=200)  # the length of image name is limited to 200 characters
    image_path = models.CharField(max_length=200)  # the length of image path is limited to 200 characters
    image_group = models.ForeignKey(Project_Group, related_name='ibi_image_group')  # the length of image group name is limited to 200 characters
    image_label_count = models.IntegerField(default=0)  # the times of the image that has been labeled
    image_type = models.IntegerField(default=1)
    image_project = models.ForeignKey(Label_Project, related_name='ibi_image_project')  # the label project name, the same as the dataset folder name

    def __str__(self):
        image_basic_info = 'image_project: ' + self.image_project.project_name +'\t'+ 'image_name:' + self.image_name + '\t' + 'image_type: ' + str(self.image_type) +'\t'+ 'image_path: ' + self.image_path + '#'+ 'image_group: ' + self.image_group.group_name + '#' + 'image_label_count: ' + str(self.image_label_count)
        return image_basic_info


class User_Basic_Info(models.Model):
    username = models.CharField(max_length=32)  #the length of username is limited to 32 characters
    password = models.CharField(max_length=32)  #the length of password is limited to 32 characters
    nickname = models.CharField(max_length=64)  #the length of nickname is limited to 64 characters
    email_address = models.CharField(max_length=128)  #the length of email address is limited 128 characters
    label_count = models.IntegerField(default=0)  # the times of user's labeling


    def __str__(self):
        user_basic_info = 'username: '+self.username + '#'+'nickname: '+self.nickname+'#'+'email_address: '+self.email_address+'||'+'label_count: '+str(self.label_count)
        #print(user_basic_info)
        return user_basic_info

class User_Setting(models.Model):
    user_basic_info = models.ForeignKey(User_Basic_Info, related_name='us_user_basic_info')
    style_select = models.IntegerField(default=1)
    project_select = models.CharField(default='.', max_length=200)

    def __str__(self):
        return 'user: '+self.user_basic_info.username+'#'+'style: '+str(self.style_select)+'#'+'project: '+self.project_select.project_name


class Image_Label_Info(models.Model):
    label_image_id = models.ForeignKey(Image_Basic_Info, related_name='label_image_id')  # use Image_Basic_Info primary key as foreign key
    base_image_id = models.ForeignKey(Image_Basic_Info, related_name='base_image_id')  # use Image_Basic_Info primary key as foreign key
    user_id = models.ForeignKey(User_Basic_Info)  # use User_Basic_Info primary key as foreign key
    image_score = models.FloatField(default=-1)  # the score that user give the two image
    label_time = models.DateTimeField()  # the time that user is labeling

    def __str__(self):
        return 'base_image_id: '+self.base_image_id.image_group.group_name+'||'+'label_image_id: '+self.label_image_id.image_name+'||'+'user_id: '+self.user_id.username


class Image_Label_Count(models.Model):
    user_id = models.ForeignKey(User_Basic_Info, related_name='count_user_id')
    image_id = models.ForeignKey(Image_Basic_Info, related_name='count_image_id')
    user_label_count = models.IntegerField(default=0)  # the number of times that this user has labeled the image

    def __str__(self):
        return 'user_id: '+self.user_id.username+'\t'+'image_id: '+self.image_id.image_name+'\t'+'user_label_count: '+str(self.user_label_count)




