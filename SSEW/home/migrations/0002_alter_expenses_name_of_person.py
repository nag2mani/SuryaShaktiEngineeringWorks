# Generated by Django 5.0.4 on 2024-06-24 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='name_of_person',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
