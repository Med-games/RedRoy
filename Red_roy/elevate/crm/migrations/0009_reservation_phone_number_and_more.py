# Generated by Django 4.2.13 on 2024-05-20 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='association',
            field=models.CharField(choices=[('cinema', 'Red Roy cinema'), ('theatre', 'Red Roy theatre'), ('coffee', 'Red Roy coffee')], max_length=255),
        ),
    ]
