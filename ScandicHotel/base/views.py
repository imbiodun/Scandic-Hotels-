from django.shortcuts import render
from .form import ContactForm
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request,"home.html")

def signup(request):
    return render(request,"signup.html")

def rooms(request):
    return render(request,"rooms.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Here you can add code to send an email or save the message to the database
            send_mail(
                'Contact Form Submission',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                email,
                ['scandichotelnoreply@gmail.com'],
                fail_silently=False,
            )
            return render(request, "contact_success.html", {"name": name})
    else:        
        form = ContactForm()   
    return render(request,"contact.html", {"form": form})
