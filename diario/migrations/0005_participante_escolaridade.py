# Generated by Django 4.0.3 on 2022-09-07 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0004_remove_participante_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participante',
            name='escolaridade',
            field=models.CharField(choices=[('0-4', '0-4'), ('5-9', '5-9'), ('10-12', '10-12'), ('12+', '12+')], default='0-9', max_length=20),
        ),
    ]
