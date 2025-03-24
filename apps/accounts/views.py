from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import User, CustomerProfile

class CustomerRegistrationView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('dashboard:home')
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_customer():
            if hasattr(self.request.user, 'customer_profile'):
                profile = self.request.user.customer_profile
            else:
                profile = CustomerProfile.objects.create(user=self.request.user)
            
            context['profile_form'] = CustomerProfileForm(instance=profile)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if request.user.is_customer():
            profile_form = CustomerProfileForm(request.POST, instance=request.user.customer_profile)
            if form.is_valid() and profile_form.is_valid():
                return self.form_valid(form, profile_form)
            else:
                return self.form_invalid(form)
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
    
    def form_valid(self, form, profile_form=None):
        form.save()
        if profile_form:
            profile_form.save()
        return super().form_valid(form)

