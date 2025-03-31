from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from home.models import HomePageContent

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # Kayıt olduktan sonra ana sayfaya yönlendir
    else:
        form = UserCreationForm()
    
    content = HomePageContent.objects.first()  # Get the first content for navbar
    return render(request, "users/signup.html", {"form": form, "content": content})
