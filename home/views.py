from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import HomePageContent, Document, ContactInfo, FooterSettings, UserProfile, DietProgram, Meal
from django.contrib.auth.models import User
from googletrans import Translator
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_http_methods, require_POST
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import json

def translate_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        target_lang = request.POST.get('lang', 'en')
        
        try:
            translator = Translator()
            translation = translator.translate(text, dest=target_lang)
            return JsonResponse({'translated_text': translation.text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def home(request):
    content = HomePageContent.objects.first()
    contact_info = ContactInfo.objects.first()
    footer_settings = FooterSettings.objects.first()
    return render(request, 'home/home.html', {
        'content': content,
        'contact_info': contact_info,
        'footer_settings': footer_settings
    })

def documents(request):
    content = HomePageContent.objects.first()
    docs = Document.objects.all().order_by('-upload_date')
    return render(request, 'home/documents.html', {
        'content': content,
        'documents': docs
    })

@login_required
def client_dashboard(request):
    if request.user.home_profile.user_type != 'client':
        messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
        return redirect('home')
    
    diet_program = DietProgram.objects.filter(client=request.user.home_profile).first()
    if not diet_program:
        messages.info(request, 'Henüz size atanmış bir diyet programı bulunmamaktadır.')
        return render(request, 'home/client_dashboard.html', {'program': None})
    
    meals = Meal.objects.filter(program=diet_program).order_by('time')
    return render(request, 'home/client_dashboard.html', {
        'program': diet_program,
        'meals': meals
    })

@login_required
def employee_dashboard(request):
    if request.user.home_profile.user_type != 'employee':
        messages.error(request, 'Bu sayfaya erişim yetkiniz yok.')
        return redirect('home')
    
    clients = UserProfile.objects.filter(user_type='client')
    programs = DietProgram.objects.filter(employee=request.user.home_profile)
    return render(request, 'home/employee_dashboard.html', {
        'clients': clients,
        'programs': programs
    })

@login_required
def register(request):
    # Kullanıcı tipini kontrol et
    if not request.user.home_profile.user_type in ['admin', 'employee']:
        messages.error(request, 'Yeni kullanıcı kaydı oluşturma yetkiniz yok.')
        return redirect('home')
    
    # Çalışanlar sadece danışan ekleyebilir
    is_admin = request.user.home_profile.user_type == 'admin'
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        user_type = request.POST.get('user_type')
        
        # Çalışanlar sadece danışan ekleyebilir
        if not is_admin and user_type != 'client':
            messages.error(request, 'Sadece danışan kaydı oluşturabilirsiniz.')
            return redirect('register')
        
        # Çalışan kaydı için aktif=False olarak ayarla
        is_active = True if user_type == 'client' else False
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu kullanıcı adı zaten kullanılıyor.')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
        
        UserProfile.objects.create(
            user=user,
            phone=phone,
            user_type=user_type
        )
        
        if user_type == 'client':
            messages.success(request, 'Danışan kaydı başarıyla oluşturuldu!')
        else:
            messages.success(request, 'Çalışan kaydı oluşturuldu. Admin onayı sonrası aktif olacaktır.')
        
        return redirect('employee_dashboard')
    
    return render(request, 'home/register.html', {'is_admin': is_admin})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # E-posta gönderme
        subject = f'Yeni İletişim Formu Mesajı - {name}'
        message = f'İsim: {name}\nE-posta: {email}\n\nMesaj:\n{message}'
        
        try:
            send_mail(
                subject,
                message,
                email,  # Gönderen e-posta
                [settings.DEFAULT_FROM_EMAIL],  # Alıcı e-posta
                fail_silently=False,
            )
            messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
        except Exception as e:
            messages.error(request, 'Mesajınız gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.')
        
        return redirect('home')
    
    return redirect('home')

@login_required
def diet_program(request):
    try:
        diet_program = DietProgram.objects.get(user=request.user)
        meals = Meal.objects.filter(diet_program=diet_program)
        return render(request, 'home/diet_program.html', {
            'diet_program': diet_program,
            'meals': meals
        })
    except DietProgram.DoesNotExist:
        messages.warning(request, 'Henüz bir diyet programınız bulunmamaktadır.')
        return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    
    # Ana sayfadaki gibi context verilerini ekliyoruz
    content = HomePageContent.objects.first()
    contact_info = ContactInfo.objects.first()
    footer_settings = FooterSettings.objects.first()
    
    context = {
        'content': content,
        'contact_info': contact_info,
        'footer_settings': footer_settings,
    }
    return render(request, 'home/login.html', context)