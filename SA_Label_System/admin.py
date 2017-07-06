from django.contrib import admin
from django.conf import settings
from . import models
from .models import Image_Basic_Info
from .models import Image_Label_Count
from .models import Image_Label_Info
from .models import User_Basic_Info
from .models import Label_Project
from .models import Project_Group
from .models import User_Setting
from .functions import get_image_score
import csv
# Register your models here.


class Label_Project_Admin(admin.ModelAdmin):
    actions = ['download_image_label_info']

    def download_image_label_info(self, request, queryset):
        data = []
        project_name = queryset[0].project_name
        label_project = models.Label_Project.objects.filter(project_name=project_name)[0]  #找到这个工程
        project_group = models.Project_Group.objects.filter(project_name=label_project)  #找到这个工程下的所有组
        for group in project_group:  #对每个组找到这个组下面的所有图片
            data_group = [group.group_name]
            image_basic_info_list = models.Image_Basic_Info.objects.filter(image_project=label_project, image_group=group, image_type=1)
            for image_basic_info in image_basic_info_list:  #对每张图片开始处理
                image_label_info_list = models.Image_Label_Info.objects.filter(label_image_id=image_basic_info)
                score_list = []
                for image_label_info in image_label_info_list:
                    score_list.append(image_label_info.image_score)  #获取打分列表
                score = get_image_score(score_list)  #获取最终得分
                data_group.append(image_basic_info.image_name)
                data_group.append(score)
            data.append(data_group)
        data_file = open(settings.BASE_DIR+'/SA_Label_System/data/project.csv', 'w')
        writer = csv.writer(data_file)
        m = len(data)
        for i in range(m):
            writer.writerow(data[i])
        data_file.close()
        self.message_user(request, '标注数据已经下载完成!')

    download_image_label_info.short_description = 'Download the labeled data'


admin.site.register(User_Basic_Info)
admin.site.register(Image_Basic_Info)
admin.site.register(Image_Label_Info)
admin.site.register(Image_Label_Count)
admin.site.register(Label_Project, Label_Project_Admin)
admin.site.register(Project_Group)
admin.site.register(User_Setting)


