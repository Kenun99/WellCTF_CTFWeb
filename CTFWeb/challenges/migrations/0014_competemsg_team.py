# Generated by Django 2.1.1 on 2018-10-24 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20181017_1116'),
        ('challenges', '0013_competemsg_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='competemsg',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Team'),
        ),
    ]