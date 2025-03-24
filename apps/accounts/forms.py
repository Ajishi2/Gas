from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, CustomerProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ('service_address', 'billing_address', 'meter_number')

class CustomerRegistrationForm(UserCreationForm):
    service_address = forms.CharField(widget=forms.Textarea)
    billing_address = forms.CharField(widget=forms.Textarea, required=False)
    meter_number = forms.CharField(max_length=20, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 
                  'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.CUSTOMER
        
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                service_address=self.cleaned_data.get('service_address'),
                billing_address=self.cleaned_data.get('billing_address'),
                meter_number=self.cleaned_data.get('meter_number')
            )
        return user

