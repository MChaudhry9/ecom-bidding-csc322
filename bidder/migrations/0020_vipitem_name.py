# Generated by Django 5.1.1 on 2024-12-12 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidder', '0019_vipitem_guess'),
    ]

    operations = [
        migrations.AddField(
            model_name='vipitem',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]