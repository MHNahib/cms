# Generated by Django 3.0.2 on 2020-05-03 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_attendence_present'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendence',
            name='session_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.SessionYear'),
        ),
    ]
