from django.shortcuts import render, redirect
from users.forms import AssignRoleForm, CustomRegistrationForm, LoginForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    print("rendered sign_up")
    form = CustomRegistrationForm()
    if request.method == "POST":
        print("clicked sign up button")
        form = CustomRegistrationForm(request.POST)
        # print(form.cleaned_data)
        if form.is_valid():
            print("form is valid")
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            # user.is_active = False
            user.save()
            print("user created")
            messages.success(
                request, 'A Confirmation mail sent. Please check you email')
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {"form": form})

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('sign-in')
    
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    # print(users)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {"users": users})

# @user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create-group')
    return render(request, 'admin/create_group.html', {"form": form})

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)

        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')
        
    return render(request, 'admin/assign_role.html', {"form": form})

def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})