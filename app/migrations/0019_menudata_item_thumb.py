# Generated by Django 2.1.9 on 2020-09-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200919_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='menudata',
            name='Item_Thumb',
            field=models.FileField(default=1, upload_to='itemthumb/'),
            preserve_default=False,
        ),
    ]
