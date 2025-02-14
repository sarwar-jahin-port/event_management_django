from django.shortcuts import render, redirect
from event.forms import EventModelForm, CategoryModelForm
from django.contrib import messages
from event.models import Event
from django.utils import timezone
from django.db.models import Q, Count

def organizer_dashboard(request):
    type = request.GET.get('type', 'all')
    search = request.GET.get('search', '')

    counts = Event.objects.aggregate(
        participants = Count('participants', distinct=True),
        total = Count('id', distinct=True),
        upcoming = Count('id', distinct=True, filter=Q(date__gt = timezone.now())),
        past = Count('id', distinct=True, filter=Q(date__lt = timezone.now())),
    )

    base_query = Event.objects.select_related('category').prefetch_related('participants').distinct()

    if type == 'all':
        events = base_query.all()
        title = "Today's Events"
    elif type == 'upcoming-events':
        events = base_query.filter(date__gt = timezone.now())
        title = "Upcoming Events"
    elif type == 'past-events':
        events = base_query.filter(date__lt = timezone.now())
        title = "Past Events"

    if search:
        events = base_query.filter(Q(name__icontains=search) | Q(location__icontains=search))

    context = {
        "events": events,
        "counts": counts,
        "title": title
    }

    return render(request, 'organizer_dashboard.html', context)

def create_event(request):
    event_form = EventModelForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event created successfully')
            return redirect('create-event')
    context = {"event_form": event_form}
    return render(request, 'create_event.html', context)

def update_event(request, id):
    event = Event.objects.get(id = id)
    event_form = EventModelForm(instance=event)

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance=event)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event updated successfully')
            return redirect('organizer_dashboard')
    context = {"event_form": event_form}
    return render(request, 'create_event.html', context)

def view_event(request, id):
    event = Event.objects.get(id = id)
    context = {"event": event}
    return render(request, "show_event.html", context)

def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect("organizer_dashboard")
    else:
        messages.error(request, "Something went wrong")
        return redirect("organizer_dashboard")

def create_category(request):
    category_form = CategoryModelForm()

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category created successfully')
            return redirect('create-category')
    context = {"category_form": category_form}
    return render(request, 'create_category.html', context)

# def create_participant(request):
#     participant_form = ParticipantModelForm()

#     if request.method == 'POST':
#         participant_form = ParticipantModelForm(request.POST)
#         if participant_form.is_valid():
#             participant_form.save()
#             messages.success(request, 'Participant created successfully')
#             return redirect('create-participant')
#     context = {"participant_form": participant_form}
#     return render(request, 'create_participant.html', context)