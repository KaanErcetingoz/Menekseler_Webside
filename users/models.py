from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_code = models.CharField(max_length=20, unique=True)
    disease = models.TextField(blank=True, null=True)
    blood_test = models.FileField(upload_to='blood_tests/', blank=True, null=True)
    diet_program = models.TextField(blank=True, null=True)
    previous_treatments = models.TextField(blank=True, null=True)
    is_consultant = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class HomePageContent(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama/Tanıtım Yazısı")
    image = models.ImageField(upload_to='homepage_images/', blank=True, null=True, verbose_name="Görsel")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ana Sayfa İçeriği"
        verbose_name_plural = "Ana Sayfa İçerikleri"