from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.service_requests.models import ServiceRequest

@login_required
def dashboard_home(request):
    """Dashboard home view"""
    user = request.user
    context = {}
    
    if user.is_customer():
        # Customer dashboard
        service_requests = ServiceRequest.objects.filter(customer=user)
        
        context.update({
            'total_requests': service_requests.count(),
            'pending_requests': service_requests.filter(status=ServiceRequest.PENDING).count(),
            'in_progress_requests': service_requests.filter(status=ServiceRequest.IN_PROGRESS).count(),
            'resolved_requests': service_requests.filter(status=ServiceRequest.RESOLVED).count(),
            'recent_requests': service_requests.order_by('-created_at')[:5],
        })
    else:
        # Support staff dashboard
        if user.is_support():
            # Support rep sees assigned requests and unassigned ones
            service_requests = ServiceRequest.objects.filter(
                Q(assigned_to=user) | Q(assigned_to__isnull=True)
            )
        else:
            # Admin sees all requests
            service_requests = ServiceRequest.objects.all()
        
        # Get requests from the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_requests = service_requests.filter(created_at__gte=thirty_days_ago)
        
        context.update({
            'total_requests': service_requests.count(),
            'pending_requests': service_requests.filter(status=ServiceRequest.PENDING).count(),
            'in_progress_requests': service_requests.filter(status=ServiceRequest.IN_PROGRESS).count(),
            'resolved_requests': service_requests.filter(status=ServiceRequest.RESOLVED).count(),
            'urgent_requests': service_requests.filter(priority=ServiceRequest.URGENT).count(),
            'recent_requests': service_requests.order_by('-created_at')[:10],
            'assigned_to_me': service_requests.filter(assigned_to=user).count() if user.is_support() else None,
            'unassigned_requests': service_requests.filter(assigned_to__isnull=True).count(),
        })
    
    return render(request, 'dashboard/home.html', context)

