# Generated by Django 4.2.16 on 2024-09-15 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_profile_options_profile_date_profile_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]
