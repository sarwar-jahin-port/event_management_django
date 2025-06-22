from django.urls import path
from event.views import rsvp, OrganizerDashboardView, CreateEventView, create_category, ViewEvent, DeleteEventView, updateEventView
from event import views
urlpatterns = [
    path('organizer_dashboard/', OrganizerDashboardView.as_view(), name='organizer_dashboard'),
    path('create-event/', CreateEventView.as_view(), name='create-event'),
    path('create-category/', create_category, name='create-category'),
    path('show_event/<int:id>/', ViewEvent.as_view(), name="show_event"),
    path('show_event/<int:id>/rsvp/', rsvp, name='rsvp'),
    path('delete_event/<int:id>/', DeleteEventView.as_view(), name = "delete_event"),
    path('update_event/<int:id>/', updateEventView.as_view(), name="update_event"),
    path('events/', views.public_events, name='public-events'),
]
