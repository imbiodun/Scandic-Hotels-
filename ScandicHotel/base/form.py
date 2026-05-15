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



from allauth.account.forms import SignupForm,LoginForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Add placeholders
            if field_name == 'email':
                field.widget.attrs['placeholder'] = 'your@email.com'
            elif field_name == 'username':
                field.widget.attrs['placeholder'] = 'Choose a username'
            elif field_name == 'password1':
                field.widget.attrs['placeholder'] = 'Create a password'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Confirm your password'

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Style login fields
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Add placeholders
            if field_name == 'login':
                field.widget.attrs['placeholder'] = 'Enter your email or username'
            elif field_name == 'password':
                field.widget.attrs['placeholder'] = 'Enter your password'
