# Generated by Django 4.2.13 on 2024-05-19 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_rename_name_event_title_event_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='images/1.png', upload_to='event_images/'),
        ),
    ]
