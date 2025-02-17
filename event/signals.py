from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from event.models import Event

@receiver(m2m_changed, sender=Event.participants.through)
def notify_participant_on_event_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        print(instance, instance.participants.all())

        participants_emails = [par.email for par in instance.participants.all()]
        print("Checking...", participants_emails)

        send_mail(
            "New Event",
            f"You have been selected to participate in this event: {instance.name}",
            "focelig858@owlny.com",
            participants_emails,
            fail_silently=False
        )