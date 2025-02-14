from django.urls import path
from event.views import organizer_dashboard, create_event, create_category, view_event, delete_event, update_event

urlpatterns = [
    path('organizer_dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('create-event/', create_event, name='create-event'),
    path('create-category/', create_category, name='create-category'),
    path('show_event/<int:id>/', view_event, name="show_event"),
    path('delete_event/<int:id>/', delete_event, name = "delete_event"),
    path('update_event/<int:id>/', update_event, name="update_event")
]
