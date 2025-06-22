from django.shortcuts import render
from datetime import date
from event.models import Event
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def home(request):
    user_roles = get_user_roles(request.user)

    # Get 6 upcoming events for the home page
    upcoming_events = Event.objects.filter(
        date__gte=date.today()
    ).order_by('date')[:6]
    
    # Add events to context
    context = {
        **user_roles,  # Spread the user roles
        'events': upcoming_events,
        'total_events': Event.objects.filter(date__gte=date.today()).count(),
    }
    
    return render(request, 'home.html', context)

def no_permission(request):
    return render(request, 'no_permission.html')

def get_user_roles(user):
    is_organizer = False
    is_admin = False
    is_participant = False

    if user.is_authenticated:
        is_organizer = user.groups.filter(name='organizer').exists()
        is_admin = user.groups.filter(name='admin').exists()
        is_participant = user.groups.filter(name='participant').exists()
    
    return {
        'is_organizer': is_organizer,
        'is_admin': is_admin,
        'is_participant': is_participant,
    }


# Add these simple view functions to your views.py

def about(request):
    """About page view"""
    user_roles = get_user_roles(request.user)
    context = user_roles
    return render(request, 'about.html', context)

def contact(request):
    """Contact page view with form handling"""
    user_roles = get_user_roles(request.user)
    
    if request.method == 'POST':
        # Handle contact form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you can:
        # 1. Save to database
        # 2. Send email notification
        # 3. Add to your CRM
        
        # For now, just show a success message
        messages.success(request, 'Thank you for your message! We\'ll get back to you within 24 hours.')
        return redirect('contact')
    
    context = user_roles
    return render(request, 'contact.html', context)