# Generated by Django 3.0.4 on 2020-03-29 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20200329_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='choice',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.Choice'),
        ),
    ]
