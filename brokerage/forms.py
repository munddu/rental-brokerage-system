from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Property, Inquiry, Booking, InquiryResponse, USER_ROLES

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    role=forms.ChoiceField(choices=USER_ROLES)
    phone=forms.CharField(required=False)
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
    def clean(self):
        data=super().clean()
        if data.get('password')!=data.get('confirm_password'):
            raise forms.ValidationError('Passwords do not match.')
        return data

class LoginForm(AuthenticationForm): pass

class PropertyForm(forms.ModelForm):
    class Meta:
        model=Property
        fields=['title','description','area','price','total_units','access_road_description','facilities','image','video']
        widgets={'description':forms.Textarea(attrs={'rows':4}),
                 'access_road_description':forms.Textarea(attrs={'rows':3}),
                 'facilities':forms.Textarea(attrs={'rows':3})}

class InquiryForm(forms.ModelForm):
    class Meta:
        model=Inquiry
        fields=['message']
        widgets={'message':forms.Textarea(attrs={'rows':4,'placeholder':'Write your inquiry here...'})}

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter booking message'
            })
        }

class InquiryResponseForm(forms.ModelForm):
    class Meta:
        model = InquiryResponse
        fields = ['response']

        widgets = {
            'response': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write response to tenant'
            })
        }