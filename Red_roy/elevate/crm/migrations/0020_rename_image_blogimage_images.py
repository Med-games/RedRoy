# Generated by Django 4.2.13 on 2024-05-26 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0019_rename_images_blogimage_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogimage',
            old_name='image',
            new_name='images',
        ),
    ]
