from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import ContactPageContent
from django.conf import settings

def contact(request):
    content = ContactPageContent.objects.first()  # Admin panelinden gelen iletişim bilgilerini al

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # E-Posta Gönderme İşlemi
        send_mail(
            subject=f"İletişim Formu Mesajı - {name}",
            message=f"Gönderen: {name} ({email})\n\nMesaj:\n{message}",
            from_email=settings.EMAIL_HOST_USER,  # SMTP için ayarladığın mail adresi
            recipient_list=["info@menekseler.com"],  # Buraya mesajları almak istediğin mail adresini yaz
            fail_silently=False,
        )

        return redirect("contact")  # Form başarıyla gönderildiğinde tekrar iletişim sayfasına yönlendir

    return render(request, "contact/contact.html", {"content": content})
