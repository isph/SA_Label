from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signup_create_user$', views.signup_create_user, name='signup_create_user'),
    url(r'^label$', views.label, name='label'),
    url(r'^label_style_2$', views.label_style_2, name='label_style_2'),
    url(r'^user_logout$', views.user_logout, name='user_logout'),
    #url(r'^inform$', views.inform, name='inform'),
    url(r'^add_project', views.add_project, name='add_project'),
    url(r'^project_select$', views.project_select, name='project_select')
]