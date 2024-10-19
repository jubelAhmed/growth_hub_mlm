# Generated by Django 3.1.5 on 2021-02-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]