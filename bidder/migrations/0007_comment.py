# Generated by Django 5.1.1 on 2024-12-11 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidder', '0006_remove_application_applicant_application_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('associated_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bidder.item')),
            ],
        ),
    ]