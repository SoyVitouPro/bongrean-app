# Generated by Django 4.2.16 on 2024-09-23 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_instructor_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='media/videos/'),
        ),
    ]
