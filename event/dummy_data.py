import random
from django.utils import timezone
from datetime import timedelta
from event.models import Event, Participant, Category

def create_dummy():
    # Clear existing data (optional)
    Event.objects.all().delete()
    Participant.objects.all().delete()
    Category.objects.all().delete()

    # Create Categories
    categories = [
        "Music", "Sports", "Technology", "Education", "Health", "Business"
    ]
    category_objs = []
    for name in categories:
        cat = Category.objects.create(name=name, description=f"This is a {name} category.")
        category_objs.append(cat)

    # Create Participants
    participants = []
    for i in range(10):
        participant = Participant.objects.create(
            name=f"Participant {i+1}",
            email=f"participant{i+1}@example.com"
        )
        participants.append(participant)

    # Create Events
    for i in range(5):
        event = Event.objects.create(
            name=f"Event {i+1}",
            description=f"This is a description for Event {i+1}.",
            date=timezone.now().date() + timedelta(days=random.randint(-5, 10)),
            time=timezone.now().time(),
            location=f"Location {i+1}",
            category=random.choice(category_objs),
        )
        # Add random participants
        event.participants.set(random.sample(participants, random.randint(2, 5)))

    print("✅ Dummy data created successfully!")

