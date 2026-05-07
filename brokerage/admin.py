from django.contrib import admin
from .models import Profile,Property,Inquiry

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','role','phone')
    list_filter=('role',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=('title','area','price','landlord','status','created_at')
    list_filter=('status','area')
    list_editable=('status',)
    search_fields=('title','area','landlord__username')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display=('property','tenant','created_at')
