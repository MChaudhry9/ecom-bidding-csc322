# Generated by Django 5.1.3 on 2024-12-12 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidder', '0017_rename_rating_transaction_buyer_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_forced_out',
            field=models.BooleanField(default=False),
        ),
    ]