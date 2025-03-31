from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class HomePageContent(models.Model):
    title = models.CharField(max_length=200, default="Menekşeler")
    logo = models.ImageField(upload_to='images/', null=True, blank=True)
    homepage_image = models.ImageField(upload_to='images/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='images/', null=True, blank=True)
    content_text = models.TextField(default="", blank=True)
    documents = models.ManyToManyField('Document', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if HomePageContent.objects.exists() and not self.pk:
            existing = HomePageContent.objects.first()
            existing.title = self.title
            existing.logo = self.logo
            existing.homepage_image = self.homepage_image
            existing.banner_image = self.banner_image
            existing.content_text = self.content_text
            existing.save()
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ana Sayfa İçeriği"
        verbose_name_plural = "Ana Sayfa İçeriği"

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Doküman Başlığı")
    file = models.FileField(upload_to='documents/', verbose_name="Dosya")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk and Document.objects.exists():
            return
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-upload_date']
        verbose_name = "Doküman"
        verbose_name_plural = "Dokümanlar"

class ContactInfo(models.Model):
    email = models.EmailField(verbose_name="E-posta Adresi")
    phone = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    address = models.TextField(verbose_name="Adres")
    whatsapp = models.CharField(max_length=20, verbose_name="WhatsApp Numarası", default="905555555555", help_text="Örnek: 905551234567 (Başında 90 olmalı, boşluk olmamalı)")
    
    def __str__(self):
        return f"İletişim Bilgileri - {self.email}"
    
    def save(self, *args, **kwargs):
        if not self.pk and ContactInfo.objects.exists():
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "İletişim Bilgileri"
        verbose_name_plural = "İletişim Bilgileri"

class FooterSettings(models.Model):
    footer_description = models.TextField(verbose_name="Footer Açıklaması", default="Menekşeler Diyet ve Sağlıklı Yaşam Merkezi olarak, size özel diyet programları ve sağlıklı yaşam önerileri sunuyoruz.")
    facebook_url = models.URLField(verbose_name="Facebook Linki", blank=True, null=True)
    instagram_url = models.URLField(verbose_name="Instagram Linki", default="https://www.instagram.com/menekseler2025")
    linkedin_url = models.URLField(verbose_name="LinkedIn Linki", blank=True, null=True)
    
    def __str__(self):
        return "Footer Ayarları"
    
    def save(self, *args, **kwargs):
        if not self.pk and FooterSettings.objects.exists():
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Footer Ayarları"
        verbose_name_plural = "Footer Ayarları"

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Çalışan'),
        ('client', 'Danışan'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='home_profile', verbose_name="Kullanıcı")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client', verbose_name="Kullanıcı Tipi")
    phone = models.CharField(max_length=15, verbose_name="Telefon Numarası")
    address = models.TextField(blank=True, verbose_name="Adres")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Boy (cm)")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Kilo (kg)")
    health_conditions = models.TextField(blank=True, verbose_name="Sağlık Durumu")
    allergies = models.TextField(blank=True, verbose_name="Alerjiler")
    medications = models.TextField(blank=True, verbose_name="Kullanılan İlaçlar")
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_user_type_display()}"
    
    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

class DietProgram(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_programs', verbose_name="Danışan")
    employee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='employee_programs', verbose_name="Çalışan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi")
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Hedef Kilo")
    daily_calories = models.IntegerField(verbose_name="Günlük Kalori")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    
    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.start_date} to {self.end_date}"
    
    class Meta:
        verbose_name = "Diyet Programı"
        verbose_name_plural = "Diyet Programları"
        ordering = ['-created_at']

class Meal(models.Model):
    MEAL_TYPE_CHOICES = (
        ('breakfast', 'Kahvaltı'),
        ('lunch', 'Öğle Yemeği'),
        ('dinner', 'Akşam Yemeği'),
        ('snack', 'Ara Öğün'),
    )
    
    program = models.ForeignKey(DietProgram, on_delete=models.CASCADE, related_name='meals', verbose_name="Diyet Programı")
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES, verbose_name="Öğün Tipi")
    time = models.TimeField(verbose_name="Öğün Saati")
    foods = models.TextField(verbose_name="Yiyecekler")
    calories = models.IntegerField(verbose_name="Kalori")
    notes = models.TextField(blank=True, null=True, verbose_name="Notlar")
    
    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.program.client.user.get_full_name()}"
    
    class Meta:
        verbose_name = "Öğün"
        verbose_name_plural = "Öğünler"
        ordering = ['time']