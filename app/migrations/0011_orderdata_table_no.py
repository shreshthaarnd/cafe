# Generated by Django 3.0.3 on 2020-08-27 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200822_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdata',
            name='Table_No',
            field=models.CharField(default='Not Assigned', max_length=50),
        ),
    ]
