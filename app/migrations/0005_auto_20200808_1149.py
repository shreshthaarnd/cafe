# Generated by Django 2.1.9 on 2020-08-08 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_customerdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentData',
            fields=[
                ('Add_Date', models.DateTimeField(auto_now=True)),
                ('Pay_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Order_ID', models.CharField(max_length=100)),
                ('Customer_ID', models.CharField(max_length=15)),
                ('Amount', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'PaymentData',
            },
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='City',
            field=models.CharField(default='Not Availiable', max_length=20),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='State',
            field=models.CharField(default='Not Availiable', max_length=20),
        ),
    ]
