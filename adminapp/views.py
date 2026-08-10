from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from happ.models import *
from capp.models import *
from django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    user=UserInfo.objects.count()
    homeowner=UserInfo.objects.filter(usertype='homeowner').count()
    contractor=UserInfo.objects.filter(usertype='contractor').count()
    enquiry=Enquiry.objects.count()
    blocked=LoginInfo.objects.filter(status='blocked').count()
    project=Project.objects.all().count()
    cproject=Project.objects.filter(status='completed').count()
    aproject=Project.objects.filter(status='under_construction').count()
    active=int(((user-blocked)*100)/user)
    context={
        'user':user,
        'homeowner':homeowner,
        'contractor':contractor,
        'adminid':adminid,
        'enquiry':enquiry,
        'blocked':blocked,
        'active':active,
        'project':project,
        'user':user,
        'cproject':cproject,
        'aproject':aproject,
    }
    return render(request,'admindash.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"You are logged out")
        return redirect('adminlogin')
    else:
        return redirect('index')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    enqs=Enquiry.objects.all()
    adminid=request.session.get('adminid')
    return render(request,'viewenq.html',{'enqs':enqs,'adminid':adminid})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    enq=Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,'Enquiry deleted Successfully')
    return redirect('viewenq')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepass(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    if request.method=='POST':
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        cnfpwd=request.POST.get('cnfpwd')
        
        try:
            admin=LoginInfo.objects.get(username=adminid)
            if oldpwd != admin.password:
                messages.error(request,"Old password is incorrect")
                return redirect('changepass')
            elif newpwd != cnfpwd:
                messages.error(request,"New password and confirm password do not matched")
                return redirect('changepass')
            if oldpwd == newpwd:
                messages.error(request,"New password is same as Old password")
                return redirect('changepass')
            else:
                admin.password=newpwd
                admin.save()
                messages.success(request,"Yor password changed Successfully.")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Someting went wrong !")
            return redirect('adminlogin')
    return render(request,'changepass.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def managecontractors(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    login=LoginInfo.objects.filter(usertype='contractor')
    contractor=UserInfo.objects.filter(usertype='contractor')
    combined = zip(contractor, login)
    return render(request,'managecontractors.html',{'adminid':adminid,'combined':combined})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def managehomeowners(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    login=LoginInfo.objects.filter(usertype='homeowner')
    homeowner=UserInfo.objects.filter(usertype='homeowner')
    combined = zip(homeowner, login)
    return render(request,'managehomeowners.html',{'adminid':adminid,'combined':combined})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    login=LoginInfo.objects.get(id=id)
    login.status='blocked'
    login.save()
    if login.usertype =='contractor':
        return redirect('managecontractors')
    else:
        return redirect('managehomeowners')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblock(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('adminlogin')
    login=LoginInfo.objects.get(id=id)
    login.status='active'
    login.save()
    if login.usertype =='contractor':
        return redirect('managecontractors')
    else:
        return redirect('managehomeowners')
    