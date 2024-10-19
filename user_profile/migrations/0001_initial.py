# Generated by Django 2.2.8 on 2021-01-30 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(default='Primary', max_length=200, unique=True)),
                ('package_amount', models.FloatField(default=0)),
                ('display_package_name', models.CharField(default='Primary', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UsePositionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('status_id', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reguser', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.TextField(blank=True, max_length=300, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('division', models.CharField(blank=True, max_length=200, null=True)),
                ('district', models.CharField(blank=True, max_length=200, null=True)),
                ('thana', models.CharField(blank=True, max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, default='../static/profile.jpg', null=True, upload_to='photos/%Y/%m/%d')),
                ('mobile_no', models.CharField(blank=True, max_length=20, null=True)),
                ('tnx_no', models.CharField(blank=True, editable=False, max_length=10, null=True)),
                ('user_position_status', models.CharField(choices=[('ACTIVE', 'Active'), ('DEACTIVE', 'Deactive'), ('OFFER_SHOWABLE', 'Offer_Showable'), ('TODAY_WINNER', 'Today_Winner')], default='Active', max_length=25)),
                ('status', models.BooleanField(default=True)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('current_wallet', models.FloatField(default=0)),
                ('registration_wallet', models.FloatField(default=0)),
                ('sponsor_wallet', models.FloatField(default=0)),
                ('founder_wallet', models.FloatField(default=0)),
                ('user_current_status', models.CharField(choices=[('NEW_USER', 'new'), ('ON_HOLD', 'hold'), ('TOP_HUNDRED', 'tophundred'), ('WINNER', 'winner')], default='NEW_USER', max_length=11)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_agent', to=settings.AUTH_USER_MODEL)),
                ('package_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Package')),
                ('sponsor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_sponsor', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]