from django.urls import path
from . import views

app_name = 'service_requests'

urlpatterns = [
    path('', views.ServiceRequestListView.as_view(), name='list'),
    path('create/', views.ServiceRequestCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.ServiceRequestDetailView.as_view(), name='detail'),
    path('<uuid:pk>/comment/', views.add_comment, name='add_comment'),
    path('<uuid:pk>/update/', views.update_service_request, name='update'),
]

