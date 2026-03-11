from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Student User'),
        ('agency', 'Agency'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField(verbose_name="Price (£/week)")
    zip_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    address = models.CharField(max_length=300, blank=True, verbose_name="Full Address")
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Longitude")
    distance_from_campus = models.CharField(max_length=50, blank=True, verbose_name="Distance from Campus")

    @property
    def price_pcm(self):
        return round((self.price * 52) / 12)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='collected_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} collected {self.property.title}"


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'property')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.property.title} ({self.rating}/5)"
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    university = models.CharField(max_length=100, blank=True, verbose_name="University")
    bio = models.TextField(blank=True, verbose_name="Bio")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"



class AgencyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency_profile')
    avatar = models.ImageField(upload_to='agency_avatars/', blank=True, null=True, verbose_name="Avatar/Logo")
    agency_name = models.CharField(max_length=200, blank=True, verbose_name="Agency Name")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    office_address = models.TextField(blank=True, verbose_name="Office Address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agency_name or f"{self.user.username}'s Agency Profile"

    def get_total_properties(self):
        """Get total number of properties posted by this agency"""
        return Property.objects.filter(owner=self.user).count()

    def get_avg_rating(self):
        """Calculate average rating of all properties from this agency"""
        properties = Property.objects.filter(owner=self.user)
        if not properties.exists():
            return 0
        
        total_rating = 0
        count = 0
        for prop in properties:
            reviews = prop.reviews.all()
            if reviews.exists():
                for review in reviews:
                    total_rating += review.rating
                    count += 1
        
        return round(total_rating / count, 1) if count > 0 else 0

    class Meta:
        verbose_name = "Agency Profile"
        verbose_name_plural = "Agency Profiles"
