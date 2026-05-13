from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('family', 'Family'),
        ('deluxe', 'Deluxe'),
        ('presidential', 'Presidential'),

    ]
    room_type = models.CharField(max_length= 50, choices=ROOM_TYPES)
    room_name = models.CharField(max_length=100)
    room_description = models.TextField()
    beds = models.IntegerField()
    max_guests = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    amenities = models.ManyToManyField(Amenity)
    capacity = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)
    available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null = True, blank = True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.room_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Room {self.room_name} ({self.get_room_type_display()})'
    
class DiscountCode(models.Model):
    DISCOUNT_TYPES = [
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage'),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value= models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    


class Reservation(models.Model):
    Payement_Method_Choices = [
        ('stripe', 'Credit Card (Stripe)'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash on Arrival'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    room= models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.IntegerField()
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)
    Payment_method = models.CharField(max_length=50, choices=Payement_Method_Choices)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def number_of_nights(self):
        return (self.check_out - self.check_in).days
    
    def calculate_total_price(self):
        base_price = self.room.price * self.number_of_nights()
        # Here you can add logic to apply discounts based on the discount_code
        if self.discount_code and self.discount_code.active:
            if self.discount_code.discount_type == 'fixed':
                return max(base_price - self.discount_code.value, 0)
            elif self.discount_code.discount_type == 'percentage':
                return base_price * (1 - self.discount_code.value / 100)
        return base_price   
    