# Generated by Django 4.2.16 on 2024-09-22 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='static/videos/'),
        ),
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='static/thumbnials'),
        ),
    ]
