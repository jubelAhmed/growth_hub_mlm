# Generated by Django 3.1.5 on 2021-02-06 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tnx_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
