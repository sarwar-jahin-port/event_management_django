from django.shortcuts import render, redirect, get_object_or_404
from event.forms import EventModelForm, CategoryModelForm, RSVPForm
from django.contrib import messages
from event.models import Event
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_admin

def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

def is_participant(user):
    return user.groups.filter(name='participant').exists()

def is_admin_or_organizer(user):
    return user.groups.filter(name='admin').exists() or user.groups.filter(name='organizer').exists()

@login_required
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

    if is_participant(request.user):
        events = base_query.filter(participants=request.user)
        title="My RSVP'd Events"
    else:
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

@login_required
@user_passes_test(is_admin, login_url='no-permission')
def create_event(request):
    event_form = EventModelForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, request.FILES)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, 'Event created successfully')
            return redirect('create-event')
    context = {"event_form": event_form}
    return render(request, 'create_event.html', context)

@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-permission')
def update_event(request, id):
    event = Event.objects.get(id = id)
    event_form = EventModelForm(instance=event)

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance=event)

        if event_form.is_valid():
            print("form is valid")
            event_form.save()
            messages.success(request, 'Event updated successfully')
            return redirect('organizer_dashboard')
        else:
            print("Form is not valid")
            print(event_form.errors)
    context = {"event_form": event_form}
    return render(request, 'create_event.html', context)

@login_required
def view_event(request, id):
    event = Event.objects.get(id = id)
    form = RSVPForm()
    rsvped = event.participants.filter(id=request.user.id).exists()
    context = {"event": event, "form": form, "rsvped": rsvped}
    return render(request, "show_event.html", context)

@login_required
@user_passes_test(is_participant, login_url='no-permission')
def rsvp(request, id):
    event = get_object_or_404(Event, id = id)
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            attending = form.cleaned_data['attending']
            if attending:
                if not event.participants.filter(id=request.user.id).exists():
                    event.participants.add(request.user)
                    # send_mail(
                    #     'Event RSVP Confirmation',
                    #     f'You have successfully RSVP\'d for {event.name}.',
                    #     settings.DEFAULT_FROM_EMAIL,
                    #     [request.user.email],
                    #     fail_silently=False,
                    # )
                    messages.success(request, 'RSVP successful!')
                else:
                    messages.warning(request,"You have already RSVP'd to this event.")
            else:
                event.participants.remove(request.user)
                messages.success(request, "RSVP removed successfully.")
            return redirect('show_event', id=id)
    return redirect('show_event', id=id)


@login_required
@user_passes_test(is_admin, login_url='no-permission')
def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect("organizer_dashboard")
    else:
        messages.error(request, "Something went wrong")
        return redirect("organizer_dashboard")

@login_required
@user_passes_test(is_admin, login_url='no-permission')
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

