# Generated by Django 2.2.8 on 2021-01-30 10:17

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
            name='UserBalanceWithdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('withdraw_method', models.CharField(choices=[('BTC', 'Bitcoin'), ('PERFECT_MONEY', 'Perfect Money'), ('SKRILL', 'Skrill'), ('NETELLER', 'Neteller'), ('PAYPAL', 'PayPal'), ('PAYZA', 'Payza')], default='Bitcoin', max_length=50)),
                ('accountIdentifier', models.CharField(blank=True, max_length=250, null=True)),
                ('pin', models.CharField(default=1, max_length=250)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('DONE', 'Done'), ('REJECTED', 'Rejected')], default='PENDING', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubwagent', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ubwuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgnetBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('agent', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgentBalanceWithdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('BTC', 'Bitcoin'), ('PERFECT_MONEY', 'Perfect Money'), ('SKRILL', 'Skrill'), ('NETELLER', 'Neteller'), ('PAYPAL', 'PayPal'), ('PAYZA', 'Payza')], default='Bitcoin', max_length=200)),
                ('amount', models.FloatField(default=0.0)),
                ('pin', models.CharField(default=1, max_length=250)),
                ('accountIdentifier', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('DONE', 'Done'), ('REJECTED', 'Rejected')], default='PENDING', max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bwagent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgentBalanceExchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('pin', models.CharField(default=1, max_length=250)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('DONE', 'Done'), ('REJECTED', 'Rejected')], default='PENDING', max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgentBalanceAdd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
