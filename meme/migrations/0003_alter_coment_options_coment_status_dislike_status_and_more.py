# Generated by Django 4.1.5 on 2023-01-24 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme', '0002_dislike_added_like_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coment',
            options={'ordering': ['-added']},
        ),
        migrations.AddField(
            model_name='coment',
            name='status',
            field=models.CharField(default='c', max_length=1),
        ),
        migrations.AddField(
            model_name='dislike',
            name='status',
            field=models.CharField(default='d', max_length=1),
        ),
        migrations.AddField(
            model_name='like',
            name='status',
            field=models.CharField(default='l', max_length=1),
        ),
        migrations.DeleteModel(
            name='Interaction',
        ),
    ]