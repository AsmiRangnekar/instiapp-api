# Generated by Django 3.2.16 on 2022-11-16 18:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('querybot', '0002_auto_20211205_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatBotLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField(blank=True)),
                ('reaction', models.IntegerField()),
            ],
            options={
                'verbose_name': 'UnresolvedQuery',
                'verbose_name_plural': 'UnresolvedQueries',
            },
        ),
    ]
