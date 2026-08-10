from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('cdash/',views.cdash,name='cdash'),
    path('contractorlogout/',views.contractorlogout,name='contractorlogout'),
    path('changepassc/',views.changepassC,name="changepassC"),
    path('cedit/',views.cedit,name='cedit'),
    path('cprofile/',views.cprofile,name='cprofile'),
    path('cviewprojects/',views.cviewprojects,name='cviewprojects'),
    path('applyproject/<id>',views.applyproject,name='applyproject'),
    path('capplications/',views.capplications,name='capplications'),
    path('assignedprojects/',views.assignedprojects,name='assignedprojects'),
    path('addprogress/<id>',views.addprogress,name='addprogress'),
    path('ccompletedprojects/',views.ccompletedprojects,name='ccompletedprojects')


]