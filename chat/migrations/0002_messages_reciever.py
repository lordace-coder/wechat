# Generated by Django 4.2 on 2023-06-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='reciever',
            field=models.CharField(default='lordace_lordace2', max_length=180),
        ),
    ]
