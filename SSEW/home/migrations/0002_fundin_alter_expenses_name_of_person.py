# Generated by Django 5.0.4 on 2024-06-20 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('online_fund', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cash_fund', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fund_head', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('return_money', 'RETURN MONEY'), ('rubble', 'RUBBLE'), ('stamping_fee', 'STAMPING FEE'), ('battery', 'BATTERY SERVICE'), ('kanta', 'KANTA'), ('repairing', 'Repairing'), ('other', 'OTHERS')], max_length=50)),
                ('remark', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='expenses',
            name='name_of_person',
            field=models.CharField(max_length=50),
        ),
    ]