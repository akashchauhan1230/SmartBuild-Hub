from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('hdash/',views.hdash,name='hdash'),
    path('homeownerlogout/',views.homeownerlogout,name='homeownerlogout'),
    path('changepassh/',views.changepassH,name="changepassH"),
    path('hedit/',views.hedit,name='hedit'),
    path('hprofile/',views.hprofile,name='hprofile'),
    path('addproject/',views.addproject,name='addproject'),
    path('hviewproject',views.hviewproject,name='hviewproject'),
    path('hviewapplications/<id>',views.hviewapplications,name='hviewapplications'),
    path('rejectapl/<id>',views.rejectapl,name='rejectapl'),
    path('approveapl/<id>',views.approveapl,name='approveapl'),
    path('runningprojects/',views.runningprojects,name='runningprojects'),
    path('viewupdates/<id>',views.viewupdates,name='viewupdates'),
    path('hcompletedprojects/',views.hcompletedprojects,name='hcompletedprojects')

]