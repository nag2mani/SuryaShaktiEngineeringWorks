# Generated by Django 5.0.4 on 2024-07-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='subsource',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]