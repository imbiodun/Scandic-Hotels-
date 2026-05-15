from django.shortcuts import render

from .form import ContactForm, ReservationForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Amenity, Reservation, Room, DiscountCode
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import date 
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.
def home(request):
    rooms = Room.objects.all()[:3] 
    return render(request,"home.html", {'rooms': rooms})

def signup(request):
    return render(request,"signup.html")

def rooms(request):
    rooms = Room.objects.all() 
    return render(request,"rooms.html", {'rooms': rooms})

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

def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, "room_detail.html", {"room": room})

@login_required
def reservation(request, slug):
    room = Room.objects.get(slug=slug)

    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():

            # 1. Get cleaned data
            guest_name = form.cleaned_data['guest_name']
            guest_email = form.cleaned_data['guest_email']
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            number_of_guests = form.cleaned_data['number_of_guests']
            discount_code = form.cleaned_data['discount_code']
            special_requests = form.cleaned_data['special_requests']
            Payment_method = form.cleaned_data['Payment_method']

            # 2. Look up discount code
            discount = None

            if discount_code:
                try:
                    discount = DiscountCode.objects.get(
                        code=discount_code,
                        active=True
                    )
                except DiscountCode.DoesNotExist:
                    discount = None

            # 3. Store reservation data in session
            request.session['reservation_data'] = {
                'guest_name': guest_name,
                'guest_email': guest_email,
                'check_in': str(check_in),
                'check_out': str(check_out),
                'number_of_guests': number_of_guests,
                'discount_code': discount_code,
                'special_requests': special_requests,
                'Payment_method': Payment_method,
                'room_slug': slug,
            }

            # 4. Calculate total price
            nights = (check_out - check_in).days
            base_price = nights * room.price

            if discount:
                if discount.discount_type == 'fixed':
                    total = max(0, base_price - discount.value)
                else:
                    total = base_price * (1 - discount.value / 100)
            else:
                total = base_price

            # 5. Dynamically detect domain
            domain = request.build_absolute_uri("/").rstrip("/")

            success_url = (
                f"{domain}/reservation/reservation_success/"
                f"?session_id={{CHECKOUT_SESSION_ID}}"
            )

            cancel_url = (
                f"{domain}/rooms/{slug}/reservation/"
            )

            # 6. Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],

                line_items=[{
                    'price_data': {
                        'currency': 'eur',

                        'product_data': {
                            'name': room.room_name,
                        },

                        'unit_amount': int(total * 100),
                    },

                    'quantity': 1,
                }],

                mode='payment',

                success_url=success_url,
                cancel_url=cancel_url,
            )

            # 7. Redirect to Stripe Checkout
            return redirect(checkout_session.url)

    else:
        form = ReservationForm()

    return render(
        request,
        "reservation.html",
        {
            'form': form,
            'room': room,
        }
    )

'''
def reservation_success(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('home')

    from datetime import date
    room = Room.objects.get(slug=reservation_data['room_slug'])
    
    # Look up discount
    discount = None
    if reservation_data['discount_code']:
        try:
            discount = DiscountCode.objects.get(code=reservation_data['discount_code'], active=True)
        except DiscountCode.DoesNotExist:
            discount = None

    # Calculate total price
    check_in = date.fromisoformat(reservation_data['check_in'])
    check_out = date.fromisoformat(reservation_data['check_out'])
    nights = (check_out - check_in).days
    base_price = room.price * nights

    if discount:
        if discount.discount_type == 'fixed':
            total_price = max(0, base_price - discount.value)
        else:
            total_price = base_price * (1 - discount.value / 100)
    else:
        total_price = base_price

    # Create reservation
    reservation = Reservation.objects.create(
        room=room,
        user=request.user,
        guest_name=reservation_data['guest_name'],
        guest_email=reservation_data['guest_email'],
        check_in=check_in,
        check_out=check_out,
        number_of_guests=reservation_data['number_of_guests'],
        discount_code=discount,
        special_requests=reservation_data['special_requests'],
        Payment_method=reservation_data['Payment_method'],
        total_price=total_price,
    )

    send_mail(
        'Reservation Confirmation',
        f'Thank you for your reservation, {reservation.guest_name}!\n\n'
        f'Room: {reservation.room.room_name}\n'
        f'Check-in: {reservation.check_in}\n'
        f'Check-out: {reservation.check_out}\n'
        f'Total Price: €{reservation.total_price}\n\n'
        f'Payment Method: {reservation.Payment_method}\n\n'
        f'Reservation Date: {reservation.created_at.strftime("%Y-%m-%d %H:%M")}\n\n'
        'We look forward to welcoming you to Scandic Hotel!',
        settings.DEFAULT_FROM_EMAIL,
        [reservation.guest_email],
        fail_silently=True,
    )

    # Clear session
    del request.session['reservation_data']

    return render(request, "reservation_success.html", {"reservation": reservation})
'''
def reservation_success(request):
    reservation_data = request.session.get('reservation_data')
    
    # Session lost after Stripe redirect — very common on deployed sites
    if not reservation_data:
        session_id = request.GET.get('session_id')
        if not session_id:
            return redirect('home')
        
        # Verify payment was actually successful with Stripe
        try:
            stripe_session = stripe.checkout.Session.retrieve(session_id)
            if stripe_session.payment_status != 'paid':
                return redirect('home')
        except Exception:
            return redirect('home')
        
        # Session is gone but payment was confirmed
        # Show generic success page
        return render(request, "reservation_success.html", {
            "reservation": None,
        })

    room = Room.objects.get(slug=reservation_data['room_slug'])
    
    discount = None
    if reservation_data['discount_code']:
        try:
            discount = DiscountCode.objects.get(
                code=reservation_data['discount_code'], active=True
            )
        except DiscountCode.DoesNotExist:
            discount = None

    check_in = date.fromisoformat(reservation_data['check_in'])
    check_out = date.fromisoformat(reservation_data['check_out'])
    nights = (check_out - check_in).days
    base_price = room.price * nights

    if discount:
        if discount.discount_type == 'fixed':
            total_price = max(0, base_price - discount.value)
        else:
            total_price = base_price * (1 - discount.value / 100)
    else:
        total_price = base_price

    reservation = Reservation.objects.create(
        room=room,
        user=request.user,
        guest_name=reservation_data['guest_name'],
        guest_email=reservation_data['guest_email'],
        check_in=check_in,
        check_out=check_out,
        number_of_guests=reservation_data['number_of_guests'],
        discount_code=discount,
        special_requests=reservation_data['special_requests'],
        Payment_method=reservation_data['Payment_method'],
        total_price=total_price,
    )

    try:
        send_mail(
            'Reservation Confirmation',
            f'Thank you for your reservation, {reservation.guest_name}!\n\n'
            f'Room: {reservation.room.room_name}\n'
            f'Check-in: {reservation.check_in}\n'
            f'Check-out: {reservation.check_out}\n'
            f'Total Price: €{reservation.total_price}\n\n'
            f'Payment Method: {reservation.Payment_method}\n\n'
            f'Reservation Date: {reservation.created_at.strftime("%Y-%m-%d %H:%M")}\n\n'
            'We look forward to welcoming you to Scandic Hotel!',
            settings.DEFAULT_FROM_EMAIL,
            [reservation.guest_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Email failed: {e}")

    del request.session['reservation_data']

    return render(request, "reservation_success.html", {"reservation": reservation})

@login_required
def profile(request):
    from django.utils import timezone
    today = timezone.now().date()
    
    upcoming = Reservation.objects.filter(user=request.user, check_out__gte=today).order_by('check_in')
    past = Reservation.objects.filter(user=request.user, check_out__lt=today).order_by('-check_in')
    total_stays = past.count()
    
    # Membership tier
    if total_stays >= 10:
        membership = 'Gold'
    elif total_stays >= 5:
        membership = 'Silver'
    else:
        membership = 'Bronze'
    
    return render(request, "profile.html", {
        'upcoming': upcoming,
        'past': past,
        'membership': membership,
        'total_stays': total_stays,
    })

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')