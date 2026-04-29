from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"home.html")

def sign_in(request):
    return render(request,"sign-in.html")

def rooms(request):
    return render(request,"rooms.html")

def contact(request):
    return render(request,"contact.html")