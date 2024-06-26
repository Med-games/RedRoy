# Generated by Django 4.2.13 on 2024-05-19 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_remove_customuser_phone_customuser_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(default='images/1.jpg', upload_to='event_images/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='available_places',
            field=models.PositiveIntegerField(),
        ),
    ]
