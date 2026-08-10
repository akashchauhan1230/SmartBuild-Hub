from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import requests 

# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        enq= Enquiry(name=name, contactno=contactno, email=email, subject=subject, message=message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }
        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request,"Your enquiry has been submitted successfuly.")
        return redirect('contact')
    return render(request, 'contact.html')
def services(request):
    return render(request,'services.html')
def project(request):
    return render(request,'project.html')
def me(request):
    return render(request,'me.html')
def adminlogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        usertype='admin'
        try:
            ad=LoginInfo.objects.get(usertype=usertype,username=username,password=password,status='active')
            if ad is not None:
                request.session['adminid']=username
                messages.success(request,"Welcome Admin")
                return redirect('admindash')

        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid Credentials")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')
def login(request):
    if request.method=='POST':
           usertype=request.POST.get('usertype')
           email=request.POST.get('email')
           password=request.POST.get('password')
          
           try:
               user=LoginInfo.objects.get(usertype=usertype, username=email, password=password)
               if user.status=='active':
                    if user is not None:
                        if user.usertype=='homeowner':
                            request.session['homeownerid']=email
                            userid=request.session.get('homeownerid')
                            user=UserInfo.objects.filter(email=userid).first()
                            name=user.name.title()
                            messages.success(request,f"Welcome {name}")
                            return redirect('hdash')
                        elif user.usertype=='contractor':
                            request.session['contractorid']=email
                            userid=request.session.get('contractorid')
                            user=UserInfo.objects.filter(email=userid).first()
                            name=user.name.title()
                            messages.success(request,f"Welcome {name}")
                            return redirect('cdash')
                        else:
                            messages.error(request,'Invalid Information !')
                            return redirect('login')
               else:
                   messages.error(request,'You are blocked, please contact to admin.')
                   return redirect('login')
                        
           except LoginInfo.DoesNotExist:
               messages.error(request,"Invalid Credentials!")
               return redirect('login')

    return render(request,'login.html')
def signup(request):
    if request.method=='POST':
            usertype=request.POST.get('usertype')
            username=request.POST.get('username')
            contactno=request.POST.get('contactno')
            email=request.POST.get('email')
            password=request.POST.get('password')
            u= LoginInfo.objects.filter(username=email)
            if u:
                messages.error(request,"This email was registered already")
                return redirect('signup')
            
            log=LoginInfo(usertype=usertype,username=email, password=password)
            log.save()
            reg=UserInfo(usertype=usertype, name=username, contact_no=contactno, email=email, password=password,login=log)
            reg.save()
            messages.success(request,"Thankyou for Joining US")
            return redirect('login')
    return render(request,'signup.html')
def forgetpassword(request):
    return render(request,'forgetpassword.html')