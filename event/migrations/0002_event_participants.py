# Generated by Django 5.1.6 on 2025-02-07 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participants', to='event.participant'),
        ),
    ]
