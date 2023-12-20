# Generated by Django 4.2 on 2023-12-14 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_alter_contract_options_alter_contract_proposal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='currency',
            field=models.CharField(choices=[('USD', 'DOLLAR')], max_length=3),
        ),
        migrations.AlterField(
            model_name='jobproposal',
            name='currency',
            field=models.CharField(choices=[('USD', 'DOLLAR')], max_length=3),
        ),
    ]