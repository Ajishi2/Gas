from django import forms
from .models import ServiceRequest, ServiceRequestAttachment, ServiceRequestComment

class ServiceRequestForm(forms.ModelForm):
    """Form for creating and updating service requests"""
    class Meta:
        model = ServiceRequest
        fields = ['category', 'subject', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class ServiceRequestAttachmentForm(forms.ModelForm):
    """Form for adding attachments to service requests"""
    class Meta:
        model = ServiceRequestAttachment
        fields = ['file']

class ServiceRequestCommentForm(forms.ModelForm):
    """Form for adding comments to service requests"""
    class Meta:
        model = ServiceRequestComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

class ServiceRequestUpdateForm(forms.ModelForm):
    """Form for support staff to update service requests"""
    class Meta:
        model = ServiceRequest
        fields = ['status', 'priority', 'assigned_to']

