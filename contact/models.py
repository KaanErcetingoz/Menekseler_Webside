from django.db import models

class ContactPageContent(models.Model):
    phone_number = models.CharField(max_length=20, default="+90 555 555 55 55")
    email = models.EmailField(default="info@menekseler.com")
    address = models.TextField(default="Firmanın adres bilgisi buraya yazılabilir.")
    description = models.TextField(blank=True, null=True)  # Firma hakkında bilgi
    contact_image = models.ImageField(upload_to='contact/', blank=True, null=True)  # Tanıtım görseli

    def __str__(self):
        return "İletişim Sayfası İçeriği"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"