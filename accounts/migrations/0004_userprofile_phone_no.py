# Generated by Django 5.1.3 on 2024-12-17 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone_no',
            field=models.CharField(default='', max_length=13),
        ),
    ]
