# Generated by Django 2.0.3 on 2018-09-21 03:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Composer',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('period', models.CharField(max_length=64, verbose_name='Music era')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistLine',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('sequence', models.IntegerField(verbose_name='Sequence')),
            ],
        ),
        migrations.CreateModel(
            name='PracticeItem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Date added')),
                ('type', models.CharField(max_length=32, verbose_name='Type')),
                ('self_appraisal', models.IntegerField(verbose_name='Self Appraisal')),
                ('difficulty', models.IntegerField(verbose_name='Difficulty')),
                ('composer', models.ForeignKey(blank=True, null=True, on_delete='models.PROTECT', to='journal.Composer')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('time', models.IntegerField(verbose_name='Practiced time')),
                ('rate', models.FloatField(verbose_name='Rate')),
                ('note', models.TextField(blank=True, max_length=256, null=True, verbose_name='Notes')),
                ('date', models.DateField(verbose_name='Date')),
                ('comment', models.TextField(blank=True, max_length=256, null=True, verbose_name='Comment')),
                ('practice_item', models.ForeignKey(on_delete='models.PROTECT', to='journal.PracticeItem')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='playlistline',
            name='item',
            field=models.ForeignKey(on_delete='models.CASCADE', to='journal.PracticeItem'),
        ),
        migrations.AddField(
            model_name='playlistline',
            name='playlist',
            field=models.ForeignKey(on_delete='models.CASCADE', to='journal.Playlist'),
        ),
    ]
