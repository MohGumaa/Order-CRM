# Generated by Django 3.1 on 2020-08-15 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
