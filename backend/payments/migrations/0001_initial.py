# Generated by Django 2.2.6 on 2019-11-13 02:16

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
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(max_length=500)),
                ('line_2', models.CharField(max_length=500, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100, null=True)),
                ('zip', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier_in_payment_option', models.CharField(choices=[('T0', 'TIER0'), ('T1', 'TIER1'), ('T2', 'TIER2'), ('T3', 'TIER3')], default='T0', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='BillingInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(default=None, max_length=100, null=True, verbose_name='Stripe Customer ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('delivery_address', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.Address')),
                ('payment_tier', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.PaymentTier')),
            ],
        ),
    ]
