# Generated by Django 3.0.2 on 2020-06-08 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_donation_otherscharge_tutionfee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otherscharge',
            name='class_name',
        ),
    ]