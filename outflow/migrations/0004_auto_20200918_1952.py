# Generated by Django 3.0.6 on 2020-09-18 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outflow', '0003_expensein_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expensein',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loss',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]