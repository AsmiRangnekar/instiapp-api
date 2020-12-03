# Generated by Django 2.2.3 on 2019-07-19 19:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bodies', '0023_body_canonical_name'),
        ('events', '0028_event_promotion_boost'),
        ('achievements', '0004_auto_20190720_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferedAchievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_of_creation', models.DateTimeField(auto_now_add=True)),
                ('time_of_modification', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True)),
                ('priority', models.IntegerField(default=0)),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offered_achievements', to='bodies.Body')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offered_achievements', to='events.Event')),
            ],
            options={
                'ordering': ('priority',),
            },
        ),
    ]
