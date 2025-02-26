from django.shortcuts import render, redirect, get_object_or_404
from event.forms import EventModelForm, CategoryModelForm, RSVPForm
from django.contrib import messages
from event.models import Event
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required, user_passes_test
from users.views import is_admin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View

def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

def is_participant(user):
    return user.groups.filter(name='participant').exists()

def is_admin_or_organizer(user):
    return user.groups.filter(name='admin').exists() or user.groups.filter(name='organizer').exists()

@method_decorator(login_required, name='dispatch')
class OrganizerDashboardView(ListView):
    model = Event
    template_name = 'organizer_dashboard.html'
    context_object_name = 'events'

    def get_queryset(self):
        base_query = Event.objects.select_related('category').prefetch_related('participants').distinct()

        if is_participant(self.request.user):
            events = base_query.filter(participants=self.request.user)
            return events
        
        type = self.request.GET.get('type', 'all')
        search = self.request.GET.get('search', '')

        if type == 'all':
            events = base_query.all()
        elif type == 'upcoming-events':
            events = base_query.filter(date__gt=timezone.now())
        elif type == 'past-events':
            events = base_query.filter(date__lt=timezone.now())

        if search:
            events = events.filter(Q(name__icontains=search) | Q(location__icontains=search))

        return events
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = Event.objects.aggregate(
            participants=Count('participants', distinct=True),
            total=Count('id', distinct=True),
            upcoming=Count('id', distinct=True, filter=Q(date__gt=timezone.now())),
            past=Count('id', distinct=True, filter=Q(date__lt=timezone.now())),
        )
        context['counts'] = counts

        if is_participant(self.request.user):
            context['title'] = "My RSVP'd Events"
        elif self.request.GET.get('type') == 'upcoming-events':
            context['title'] = "Upcoming Events"
        elif self.request.GET.get('type') == 'past-events':
            context['title'] = "Past Events"
        else:
            context['title'] = "Today's Events"

        return context

create_event_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]

@method_decorator(create_event_decorators, name='dispatch')
class CreateEventView(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'create_event.html'
    success_url = 'create-event'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Event created successfully')
        return super.form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Form submission failed. Please check the errros below')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['event_form'] = context.get('form')
        return context

update_event_decorators = [login_required, user_passes_test(is_admin_or_organizer, login_url='no-permission')]
class updateEventView(UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'create_event.html'
    success_url = 'organizer_dashboard'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Event, id = id)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Event updated successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Form submission failed. Please check the errors below')
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = context.get('form')
        return context

@method_decorator(login_required, name='dispatch')
class ViewEvent(DetailView):
    model = Event
    template_name = 'show_event.html'
    context_object_name = 'event'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        event = self.object
        rsvped = event.participants.filter(id = self.request.user.id).exists()
        context['form'] = RSVPForm()
        context['rsvped'] = rsvped
        return context


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


# @login_required
# @user_passes_test(is_admin, login_url='no-permission')
# def delete_event(request, id):
#     if request.method == "POST":
#         event = Event.objects.get(id = id)
#         event.delete()
#         messages.success(request, "Task Deleted Successfully")
#         return redirect("organizer_dashboard")
#     else:
#         messages.error(request, "Something went wrong")
#         return redirect("organizer_dashboard")

delete_event_decorators = [login_required, user_passes_test(is_admin, login_url='no-permission')]
@method_decorator(delete_event_decorators, name='dispatch')
class DeleteEventView(View):
    def post(self, request, id, *args, **kwargs):
        event = get_object_or_404(Event, id = id)
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect ("organizer_dashboard")
    
    def get(self, request, id, *args, **kwargs):
        messages.error(request, 'Something went wrong')
        return redirect('organizer_dashboard')

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

