from django.shortcuts import render

# Create your views here.
def home(request):
    user_roles = get_user_roles(request.user)
    context = user_roles
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

