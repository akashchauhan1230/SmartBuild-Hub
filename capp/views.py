from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from happ.models import Project
from .models import *
from decimal import Decimal
from django.views.decorators.cache import cache_control

# Create your views here
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cdash(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    project=Project.objects.filter(contractor=contractor).count()
    cproject=Project.objects.filter(contractor=contractor,status='completed').count()
    aproject=Project.objects.filter(contractor=contractor,status='under_construction').count()
    applications=ContractorApplication.objects.filter(contractor=contractor).count()
    pa=ContractorApplication.objects.filter(contractor=contractor, status='pending').count()
    ra=ContractorApplication.objects.filter(contractor=contractor, status='rejected').count()
    aa=ContractorApplication.objects.filter(contractor=contractor, status='approved').count()

    context={
        'name':contractor.name.title(),
        'contractorid':contractor.email,
        'project':project,
        'aproject':aproject,
        'cproject':cproject,
        'applications':applications,
        'pa':pa,
        'ra':ra,
        'aa':aa
    }
    return render(request,'cdash.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contractorlogout(request):
    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('login')
    else:
        return redirect('index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassC(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    if request.method=='POST':
        oldpwd=request.POST.get('oldpwd')
        newpwd=request.POST.get('newpwd')
        cnfpwd=request.POST.get('cnfpwd')
        
        try:
            login=LoginInfo.objects.get(username=contractorid)
            contractor=UserInfo.objects.filter(email=contractorid).first()
            if oldpwd != contractor.password:
                messages.error(request,"Old password is incorrect")
                return redirect('changepassC')
            elif newpwd != cnfpwd:
                messages.error(request,"New password and confirm password do not matched")
                return redirect('changepassC')
            if oldpwd == newpwd:
                messages.error(request,"New password is same as Old password")
                return redirect('changepassC')
            else:
                login.password=newpwd
                contractor.password=newpwd
                login.save()
                contractor.save()
                messages.success(request,"Yor password changed Successfully.")
                return redirect('cdash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Someting went wrong !")
            return redirect('login')
    return render(request,'changepassc.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cedit(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    context={
        'name':contractor.name,
        'contactno':contractor.contact_no,
        'email':contractor.email,
        'address':contractor.address,
        'bio':contractor.bio,

    }
    if request.method=='POST':
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        bio=request.POST.get('bio')
        profile=request.FILES.get('profile')
        contractor.name=name
        contractor.contact_no=contactno
        contractor.address=address
        contractor.bio=bio
        try:
            if profile:
                contractor.picture=profile
            contractor.save()
            messages.success(request,"Your profile updated successfully")
            return redirect('cdash')
        except:
            messages.error("Somthing went wrong")
            return redirect('cedit')
        
    return render(request,'cedit.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cprofile(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    context={
        'name':contractor.name,
        'contactno':contractor.contact_no,
        'email':contractor.email,
        'address':contractor.address,
        'bio':contractor.bio,
        'profile':contractor.picture,

    }
    return render(request,'cprofile.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cviewprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    projects=Project.objects.filter(contractor=None)
    context={
        'name':contractor.name.title(),
        'contractorid':contractor.email,
        'project':projects
    }
    return render(request,'cviewprojects.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def applyproject(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    project=Project.objects.get(id=id)
    context={
        'name':contractor.name.title(),
        'contractorid':contractor.email,
        'project':project,
    }
    application=ContractorApplication.objects.filter(project=project,contractor=contractor)
    if application.exists():
        messages.warning(request,'You have already applied for this project')
        return redirect('cviewprojects')
    if request.method=="POST":
        proposal_text=request.POST.get('proposal_text')
        design_file=request.POST.get('design_file')
        estimated_budget=request.POST.get('estimated_budget')
        try:
            estimated_budget=Decimal(request.POST.get('estimated_budget'))
        except:
            messages.error(request,"Invalid estimated budget")
            return redirect('cviewsprojects')
        estimated_duration=request.POST.get('estimated_duration')
        app=ContractorApplication(
            contractor=contractor,
            project=project,
            proposal_text=proposal_text,
            design_file=design_file,
            estimated_budget=estimated_budget,
            estimated_duration=estimated_duration
        )
        app.save()
        messages.success(request,'Project application submitted successfully')
        return redirect('cviewprojects')

    return render(request,'applyproject.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def capplications(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    applications=ContractorApplication.objects.filter(contractor=contractor)
    context={
        'name':contractor.name.title(),
        'contractorid':contractor.email,
        'applications':applications
    }
    return render(request,'capplications.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def assignedprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    projects=Project.objects.filter(contractor=contractor)
    context={
        'name':contractor.name.title(),
        'contractorid':contractor.email,
        'projects':projects
    }
    return render(request,'assignedprojects.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addprogress(request,id):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    project=Project.objects.get(id=id)
    context={
        'name':contractor.name.title(),
        'contractorid':contractor.email,
        'project':project
    }
    if request.method=='POST':
        update_text=request.POST.get('update_text')
        image=request.FILES.get('image')
        progress_percent=int(request.POST.get('progress_percent'))
        pu=ProgressUpdate(
            project=project,
            update_text=update_text,
            image=image,
            progress_percent=progress_percent,
            updated_by=contractor
        )
        if progress_percent>100:
            messages.error(request,"Progress can not be more than 100%")
            return redirect('addprogress',id=id)
        elif progress_percent<0 or progress_percent<project.progress:
            messages.error(request,'Progress can not be less than 0% or previous progress')
            return redirect('addprogress',id=id)
        if progress_percent==100:
            project.status='completed'
        project.progress=progress_percent
        project.save()
        pu.save()   
        messages.success(request,'Progress updated Successfully')
        return redirect('assignedprojects')
        
    return render(request,'addprogress.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ccompletedprojects(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    projects=Project.objects.filter(contractor=contractor,status='completed')
    context={
        'name':contractor.name.title(),
        'homeownerid':contractor.email,
        'projects':projects
    }
    return render(request,'ccompletedprojects.html',context)