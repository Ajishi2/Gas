from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from .models import ServiceRequest, ServiceRequestAttachment, ServiceRequestComment
from .forms import (
    ServiceRequestForm, 
    ServiceRequestAttachmentForm, 
    ServiceRequestCommentForm,
    ServiceRequestUpdateForm
)

class CustomerRequiredMixin(UserPassesTestMixin):
    """Mixin to require customer role"""
    def test_func(self):
        return self.request.user.is_customer()

class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to require staff role"""
    def test_func(self):
        return self.request.user.is_support() or self.request.user.is_admin_user()

class ServiceRequestListView(LoginRequiredMixin, ListView):
    """View for listing service requests"""
    model = ServiceRequest
    template_name = 'service_requests/list.html'
    context_object_name = 'service_requests'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        if user.is_customer():
            return ServiceRequest.objects.filter(customer=user)
        else:
            return ServiceRequest.objects.all()

class ServiceRequestDetailView(LoginRequiredMixin, DetailView):
    """View for viewing service request details"""
    model = ServiceRequest
    template_name = 'service_requests/detail.html'
    context_object_name = 'service_request'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_customer():
            return ServiceRequest.objects.filter(customer=user)
        else:
            return ServiceRequest.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = ServiceRequestCommentForm()
        if self.request.user.is_support() or self.request.user.is_admin_user():
            context['update_form'] = ServiceRequestUpdateForm(instance=self.object)
        return context

class ServiceRequestCreateView(LoginRequiredMixin, CustomerRequiredMixin, CreateView):
    """View for creating a new service request"""
    model = ServiceRequest
    form_class = ServiceRequestForm
    template_name = 'service_requests/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attachment_form'] = ServiceRequestAttachmentForm()
        return context
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        self.object = form.save()
        
        # Handle file attachments
        files = self.request.FILES.getlist('file')
        for f in files:
            ServiceRequestAttachment.objects.create(
                service_request=self.object,
                file=f
            )
        
        messages.success(self.request, 'Service request created successfully.')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('service_requests:detail', kwargs={'pk': self.object.pk})

@login_required
def add_comment(request, pk):
    """View for adding a comment to a service request"""
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Check if user has access to this service request
    if request.user.is_customer() and service_request.customer != request.user:
        messages.error(request, "You don't have permission to comment on this request.")
        return redirect('service_requests:list')
    
    if request.method == 'POST':
        form = ServiceRequestCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.service_request = service_request
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
    
    return redirect('service_requests:detail', pk=service_request.pk)

@login_required
def update_service_request(request, pk):
    """View for support staff to update a service request"""
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    
    # Only support staff can update service requests
    if not (request.user.is_support() or request.user.is_admin_user()):
        messages.error(request, "You don't have permission to update this request.")
        return redirect('service_requests:list')
    
    if request.method == 'POST':
        form = ServiceRequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            # If status is changed to resolved, set resolved_at
            if form.cleaned_data['status'] == ServiceRequest.RESOLVED and service_request.status != ServiceRequest.RESOLVED:
                form.instance.resolved_at = timezone.now()
            
            form.save()
            messages.success(request, 'Service request updated successfully.')
    
    return redirect('service_requests:detail', pk=service_request.pk)

