from django.urls import path
from . import views
urlpatterns=[
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('delenq/<id>',views.delenq,name='delenq'),
    path('changepass/',views.changepass,name="changepass"),
    path('managehomeowners/',views.managehomeowners,name='managehomeowners'),
    path('managecontractors/',views.managecontractors,name='managecontractors'),
    path('block/<id>',views.block,name='block'),
    path('unblock/<id>',views.unblock,name='unblock'),
]