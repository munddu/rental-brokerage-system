from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from brokerage import views

urlpatterns=[
path('admin/',admin.site.urls),
path('',views.home,name='home'),
path('register/',views.register_view,name='register'),
path('login/',views.login_view,name='login'),
path('logout/',views.logout_view,name='logout'),
path('properties/',views.property_list,name='property_list'),
path('properties/add/',views.add_property,name='add_property'),
path('properties/<int:property_id>/',views.property_detail,name='property_detail'),
path('inquiry/<int:property_id>/',views.send_inquiry,name='send_inquiry'),
path('book/<int:property_id>/', views.book_property, name='book_property'),
path('booking/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
path('booking/reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
path('inquiry/respond/<int:inquiry_id>/', views.respond_inquiry, name='respond_inquiry'),
path('landlord-dashboard/',views.landlord_dashboard,name='landlord_dashboard'),
path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
path('admin-dashboard/approve/<int:property_id>/',views.approve_property,name='approve_property'),
path('admin-dashboard/reject/<int:property_id>/',views.reject_property,name='reject_property'),
path('tenant-dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
