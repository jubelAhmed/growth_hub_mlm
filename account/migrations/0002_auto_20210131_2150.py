# Generated by Django 3.1.5 on 2021-01-31 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentbalancewithdraw',
            name='payment_method',
            field=models.CharField(choices=[('BTC', 'Bitcoin'), ('PERFECT_MONEY', 'Perfect Money'), ('SKRILL', 'Skrill'), ('NETELLER', 'Neteller'), ('PAYPAL', 'PayPal'), ('PAYZA', 'Payza')], default='BTC', max_length=200),
        ),
    ]