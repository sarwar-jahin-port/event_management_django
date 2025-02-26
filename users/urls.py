from django.urls import path
from users.views import group_list, assign_role, sign_up, sign_in, sign_out, admin_dashboard, create_group, activate_user, ProfileView, EditProfileView, CustomPasswordResetView, ChangePassword, CustomPasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/group-list/', group_list, name='group-list'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
