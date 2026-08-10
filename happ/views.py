from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .forms import ProjectForm
from happ.models import *
from capp.models import *
from django.utils import timezone
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    project=Project.objects.filter(homeowner=homeowner).count()
    cproject=Project.objects.filter(homeowner=homeowner,status='completed').count()
    aproject=Project.objects.filter(homeowner=homeowner,status='under_construction').count()
    pendingp=Project.objects.filter(homeowner=homeowner,status='planned').count()
    context={
        'name':homeowner.name.title(),
        'homeownerid':homeowner.email,
        'project':project,
        'aproject':aproject,
        'cproject':cproject,
        'pendingp':pendingp
    }
    return render(request,'hdash.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeownerlogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('index')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassH(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    if request.method=='POST':
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        cnfpwd=request.POST.get('cnfpwd')
        
        try:
            login=LoginInfo.objects.get(username=homeownerid)
            homeowner=UserInfo.objects.filter(email=homeownerid).first()
            if oldpwd != homeowner.password:
                messages.error(request,"Old password is incorrect")
                return redirect('changepassH')
            elif newpwd != cnfpwd:
                messages.error(request,"New password and confirm password do not matched")
                return redirect('changepassH')
            if oldpwd == newpwd:
                messages.error(request,"New password is same as Old password")
                return redirect('changepassH')
            else:
                login.password=newpwd
                homeowner.password=newpwd
                login.save()
                homeowner.save()
                messages.success(request,"Yor password changed Successfully.")
                return redirect('hdash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Someting went wrong !")
            return redirect('login')
    return render(request,'changepassh.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hedit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    context={
        'name':homeowner.name,
        'contactno':homeowner.contact_no,
        'email':homeowner.email,
        'address':homeowner.address,
        'bio':homeowner.bio,

    }
    if request.method=='POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        bio=request.POST.get('bio')
        profile=request.FILES.get('profile')
        homeowner.name=name
        homeowner.contact_no=contactno
        homeowner.address=address
        homeowner.bio=bio
        try:
            if profile:
                homeowner.picture=profile
            homeowner.save()
            messages.success(request,"Your profile updated successfully")
            return redirect('hdash')
        except:
            messages.error("Somthing went wrong")
            return redirect('hedit')
        
    return render(request,'hedit.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    context={
        'name':homeowner.name,
        'contactno':homeowner.contact_no,
        'email':homeowner.email,
        'address':homeowner.address,
        'bio':homeowner.bio,
        'profile':homeowner.picture,

    }
    return render(request,'hprofile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    form=ProjectForm()
    context={
        'name':homeowner.name,
        'contactno':homeowner.contact_no,
        'email':homeowner.email,
        'address':homeowner.address,
        'bio':homeowner.bio,
        'profile':homeowner.picture,
        'form':form,

    }
    if request.method=="POST":
        form=ProjectForm(request.POST)
        if form.is_valid():
            project=form.save(commit=False)
            project.homeowner=homeowner
            project.save()
            messages.success(request,'Project has been added')
            return redirect('addproject')
        else:
            messages.error(request,'Invalid Form')
            return redirect('addproject')
    return render(request,'addproject.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hviewproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    projects=Project.objects.filter(homeowner=homeowner)
    context={
        'name':homeowner.name.title(),
        'homeownerid':homeowner.email,
        'project':projects
    }
    return render(request,'hviewproject.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    project=Project.objects.get(id=id)
    applications=ContractorApplication.objects.filter(project=project)
    context={
        'name':homeowner.name.title(),
        'homeownerid':homeowner.email,
        'project':project,
        'applications':applications
    }
    return render(request,'hviewapplications.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rejectapl(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    app=ContractorApplication.objects.get(id=id)
    app.status='rejected'
    app.save()
    messages.success(request,'Application has been rejected')
    return redirect('hviewapplications', id=app.project.id) 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def approveapl(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    app=ContractorApplication.objects.get(id=id)
    project=Project.objects.get(id=app.project.id)
    apps=ContractorApplication.objects.filter(project=app.project).update(status='rejected')
    app.status='approved'
    app.save()
    project.contractor=app.contractor
    project.start_date= timezone.now()
    project.status='under_construction'
    project.save()
    messages.success(request,'Application has been approved')
    return redirect('hviewapplications', id=app.project.id) 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def runningprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner,status='under_construction')
    context={
        'name':homeowner.name.title(),
        'homeownerid':homeowner.email,
        'projects':projects
    }
    return render(request,'runningprojects.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewupdates(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    updates=ProgressUpdate.objects.filter(project=project)
    context={
        'name':homeowner.name.title(),
        'homeownerid':homeowner.email,
        'project':project,
        'updates':updates
    }
    return render(request,'viewupdates.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hcompletedprojects(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    projects=Project.objects.filter(homeowner=homeowner,status='completed')
    context={
        'name':homeowner.name.title(),
        'homeownerid':homeowner.email,
        'projects':projects
    }
    return render(request,'hcompletedprojects.html',context)