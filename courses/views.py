from django.shortcuts import render,redirect
from courses.models import *
from courses.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
import random
# Create your views here.

def home(request):
    return render(request,'home.html')

def courses(request):
    CO = Course.objects.all()
    return render(request,'courses.html',{'CO':CO})

def courseDetails(request):
    return render(request,'course-details.html')

def courseDetails(request,id=None):
    CO = Course.objects.get(id = id)
    l = [i for i in CO.course_bullets.split('.') if CO.course_bullets]
    return render(request,'course-details.html',{'CO':CO,'points':l[:-1]})

def enrollment(request):
    return render(request,'enrollment.html')


def enrollment(request,id):
    print(id)
    return render(request,'enrollment.html')

def confirmation(request):
    return render(request,'confirmation.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')



def otpgenerator():
    return random.randint(100000,999999)

def otp_page(request):
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp = request.session.get('otp')
        otp_source = request.session.get('otp_source')
        otp_expiry = request.session.get('otp_expiry')

        if otp_expiry and datetime.now() > datetime.strptime(otp_expiry, '%Y-%m-%d %H:%M:%S'):
            return render(request, 'otp_page.html', {'error': 'OTP has expired. Please try again.'})

        if entered_otp and int(entered_otp) == otp:
            if otp_source == 'login' or otp_source == 'loginresendOTP':
                return redirect('login_continue')
        else:
            return HttpResponse('Invalid OTP')
    return render(request,'otp_page.html')



def resendOTP(request):
    resendotp = otpgenerator()

    username = request.session.get('username')
    UO = User.objects.get(username=username)

    send_mail(
                    'Login OTP',
f"""
Dear {username},

Your ShopEasy login OTP is {resendotp}. This OTP is valid for the next 2 minutes.

Please do not share this OTP with anyone. If you did not request this, please contact our support team immediately.

Thank you,
The ShopEasy Team
""",
                    'hareeshgarisha@gmail.com',
                    [UO.email],
                    fail_silently=False
                          )
    request.session['otp'] = resendotp
    request.session['otp_source'] = 'loginresendOTP'
    request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
    return redirect('otp_page')


def login(request):
    ELF = UserLoginForm()
    if request.method == 'POST':
        ELFDO = UserLoginForm(request.POST)
        if ELFDO.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            AUO = authenticate(username=username,password=password)
            if AUO and AUO.is_active:
                otp = otpgenerator()
                UO = User.objects.get(username= username)
                send_mail(
                    'Login OTP',
f"""
Dear {username},

Your ShopEasy login OTP is {otp}. This OTP is valid for the next 2 minutes.

Please do not share this OTP with anyone. If you did not request this, please contact our support team immediately.

Thank you,
The ShopEasy Team
""",
                    'hareeshgarisha@gmail.com',
                    [UO.email],
                    fail_silently=False
                          )
                request.session['otp'] = otp
                request.session['username'] = username
                request.session['password'] = password
                request.session['otp_source'] = 'login'
                request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')
                return redirect('otp_page')
            else:
                return HttpResponse('Invalid User')
    return render(request,'login.html',{'ELF':ELF})


def login_continue(request):
    if request.session.get('username'):
        username = request.session.get('username')
        password = request.session.get('password')
        AUO = authenticate(username = username,password=password)
        login(request,AUO)
        request.session['username'] = username
        return HttpResponseRedirect(reverse('lms'))
    else:
        return HttpResponse('Invalid user')

@login_required
def Userlogut(request):
    logout(request)
    return render(request,'home.html')

def register(request):
    EUFO = UserMF()
    EPFO = ProfileMF()
    if request.method == 'POST' and request.FILES:
        NMUFDO = UserMF(request.POST)
        NMPFDO = ProfileMF(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            
            MUFDO = NMUFDO.save(commit=False)
            pwd = NMUFDO.cleaned_data['password']
            MUFDO.set_password(pwd)
            MUFDO.save()

            MPFDO = NMPFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()


            current_datetime = datetime.now()
            current_date = current_datetime.strftime("%Y-%m-%d")
            current_time = current_datetime.strftime("%H:%M:%S")
            
            
            send_mail(
            'Registration Of Elearn',
            f"""
Hi {MPFDO.first_name},

You have successfully logged into your ShopEasy account on {current_date} at {current_time}.

If this was you, no further action is needed. If you suspect any unauthorized access, please reset your password immediately or contact our support team.

Happy Shopping,  
The Elearn Team

""",
            'hareeshgarisha@gmail.com',
            [MUFDO.email],
            fail_silently=True
            )
            
            return render(request,'register.html',{'EUFO':EUFO,'EPFO':EPFO,'success':'Registration is Done Successfully'})
        else:
            return HttpResponse('invalid')
    return render(request,'register.html',{'EUFO':EUFO,'EPFO':EPFO})

def lms(request):
    courses = {
        "web-development": [
            {"title": "HTML Basics", "url": "videos/video1.mp4"},
            {"title": "CSS Basics", "url": "videos/css-basics.mp4"},
            {"title": "JavaScript Basics", "url": "videos/javascript-basics.mp4"},
        ],
        "data-science": [
            {"title": "Intro to Python", "url": "videos/video2.mp4"},
            {"title": "Data Analysis with Pandas", "url": "videos/pandas.mp4"},
            {"title": "Data Visualization", "url": "videos/data-viz.mp4"},
        ],
        "graphic-design": [
            {"title": "Introduction to Graphic Design", "url": "videos/intro-graphic-design.mp4"},
            {"title": "Photoshop Basics", "url": "videos/photoshop-basics.mp4"},
            {"title": "Illustrator Basics", "url": "videos/illustrator-basics.mp4"},
        ],
    }
    return render(request, 'lms.html', {'courses': courses})
