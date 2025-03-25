# Gas Utility Service Portal

A comprehensive Django application for managing customer service requests for gas utility companies. This system allows customers to submit service requests online, track their status, and communicate with support representatives.

## Features

- **User Management**
  - Role-based access (Customer, Support Representative, Administrator)
  - Custom user profiles with account information
  - Secure authentication and authorization

- **Service Request Management**
  - Submit service requests with detailed information
  - Attach files to service requests
  - Categorize and prioritize requests
  - Track request status (Pending, In Progress, Resolved, Closed)

- **Request Tracking**
  - View all service requests and their current status
  - Filter requests by status, priority, and date
  - Comment system for communication between customers and support staff
  - Detailed history of request updates

- **Dashboard**
  - Overview of request statistics
  - Quick access to pending and urgent requests
  - Recent activity tracking
  - Role-specific dashboards for customers and support staff

## Technology Stack

- **Backend**: Django 4.2
- **Database**: MySQL
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Forms**: django-crispy-forms with crispy-bootstrap5
- **File Storage**: Django's FileField with local storage

## Installation

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

