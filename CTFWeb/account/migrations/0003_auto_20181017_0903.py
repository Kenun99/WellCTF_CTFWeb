# Generated by Django 2.1.1 on 2018-10-17 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='mateA',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mateA', to='account.Person'),
        ),
        migrations.AddField(
            model_name='team',
            name='mateB',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mateB', to='account.Person'),
        ),
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leader', to='account.Person'),
        ),
    ]
