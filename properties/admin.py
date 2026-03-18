from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Review, User, Property, UserProfile, AgencyProfile

admin.site.register(Property)
admin.site.register(User, UserAdmin)

admin.site.register(UserProfile)
admin.site.register(AgencyProfile)
admin.site.register(Review)
