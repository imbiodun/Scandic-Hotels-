from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}))


class ReservationForm(forms.Form):
    guest_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Guest Name'}))
    guest_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Guest Email'}))
    check_in = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    number_of_guests = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Guests'}))
    discount_code = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Discount Code'}))
    special_requests = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Special Requests', 'rows': 3}))
    Payment_method = forms.ChoiceField(choices=[
        ('stripe', 'Credit Card (Stripe)'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash on Arrival'),
    ], widget=forms.Select(attrs={'class': 'form-control'}))
