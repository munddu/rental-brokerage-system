from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect,render
from .forms import RegisterForm,LoginForm,PropertyForm,InquiryForm
from .models import Property,Inquiry,KAMPALA_AREAS

def is_admin(user): return user.is_authenticated and user.is_staff
def is_landlord(user): return user.is_authenticated and hasattr(user,'profile') and user.profile.role=='Landlord'

def home(request):
    featured=Property.objects.filter(status='Approved')[:6]
    return render(request,'home.html',{'featured':featured,'areas':KAMPALA_AREAS})

def register_view(request):
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'])
        user.profile.role=form.cleaned_data['role']; user.profile.phone=form.cleaned_data['phone']; user.profile.save()
        login(request,user); messages.success(request,'Registration successful.'); return redirect('home')
    return render(request,'auth/register.html',{'form':form})

def login_view(request):
    form=LoginForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid():
        login(request,form.get_user()); messages.success(request,'Login successful.'); return redirect('home')
    return render(request,'auth/login.html',{'form':form})

def logout_view(request):
    logout(request); messages.info(request,'You have logged out.'); return redirect('home')

def property_list(request):
    properties=Property.objects.filter(status='Approved')
    area=request.GET.get('area'); min_price=request.GET.get('min_price'); max_price=request.GET.get('max_price')
    if area: properties=properties.filter(area=area)
    if min_price: properties=properties.filter(price__gte=min_price)
    if max_price: properties=properties.filter(price__lte=max_price)
    return render(request,'properties/list.html',{'properties':properties,'areas':KAMPALA_AREAS,'selected_area':area,'min_price':min_price or '','max_price':max_price or ''})

def property_detail(request,property_id):
    p=get_object_or_404(Property,id=property_id,status='Approved')
    return render(request,'properties/detail.html',{'property':p,'inquiry_form':InquiryForm()})

@login_required
def send_inquiry(request,property_id):
    p=get_object_or_404(Property,id=property_id,status='Approved')
    form=InquiryForm(request.POST)
    if request.method=='POST' and form.is_valid():
        inquiry=form.save(commit=False); inquiry.property=p; inquiry.tenant=request.user; inquiry.save()
        messages.success(request,'Your inquiry has been sent to the landlord.')
    return redirect('property_detail',property_id=property_id)

@login_required
def add_property(request):
    if not is_landlord(request.user):
        messages.error(request,'Only landlords can add properties.'); return redirect('home')
    form=PropertyForm(request.POST or None,request.FILES or None)
    if request.method=='POST' and form.is_valid():
        p=form.save(commit=False); p.landlord=request.user; p.status='Pending'; p.save()
        messages.success(request,'Property submitted. It is pending admin approval.'); return redirect('landlord_dashboard')
    return render(request,'properties/add.html',{'form':form})

@login_required
def landlord_dashboard(request):
    if not is_landlord(request.user):
        messages.error(request,'Only landlords can access this page.'); return redirect('home')
    properties=Property.objects.filter(landlord=request.user)
    inquiries=Inquiry.objects.filter(property__landlord=request.user)
    return render(request,'dashboards/landlord.html',{'properties':properties,'inquiries':inquiries})

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request,'dashboards/admin_dashboard.html',{'pending':Property.objects.filter(status='Pending'),'approved':Property.objects.filter(status='Approved')[:10],'rejected':Property.objects.filter(status='Rejected')[:10]})

@user_passes_test(is_admin)
def approve_property(request,property_id):
    p=get_object_or_404(Property,id=property_id); p.status='Approved'; p.admin_comment=''; p.save()
    messages.success(request,'Property approved.'); return redirect('admin_dashboard')

@user_passes_test(is_admin)
def reject_property(request,property_id):
    p=get_object_or_404(Property,id=property_id); p.status='Rejected'; p.admin_comment='Rejected by administrator.'; p.save()
    messages.warning(request,'Property rejected.'); return redirect('admin_dashboard')
