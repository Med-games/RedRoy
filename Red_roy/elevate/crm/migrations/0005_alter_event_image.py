# Generated by Django 4.2.13 on 2024-05-19 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='images/1.png', upload_to='media/'),
        ),
    ]