from django.shortcuts import render

from .models import Property

def home(request):
    properties = Property.objects.all().order_by("-created_at")
    return render(request, "home.html", {"properties": properties})

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})
