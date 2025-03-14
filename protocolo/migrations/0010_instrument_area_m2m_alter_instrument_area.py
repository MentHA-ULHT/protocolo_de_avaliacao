# Generated by Django 4.0.5 on 2022-09-20 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('protocolo', '0009_remove_question_evaluation_scale_alter_answer_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='area_m2m',
            field=models.ManyToManyField(blank=True, default=None, related_name='instruments', to='protocolo.area'),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='xx', to='protocolo.area'),
        ),
    ]
