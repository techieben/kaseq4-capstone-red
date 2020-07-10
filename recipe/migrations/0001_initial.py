# Generated by Django 3.0.8 on 2020-07-09 18:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recpie', '0008_auto_20200709_0348'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(max_length=320)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('servings', models.IntegerField(default=1)),
                ('time_prep_days', models.IntegerField(default=0)),
                ('time_prep_hours', models.IntegerField(default=0)),
                ('time_prep_mins', models.IntegerField(default=0)),
                ('time_cook_days', models.IntegerField(default=0)),
                ('time_cook_hours', models.IntegerField(default=0)),
                ('time_cook_mins', models.IntegerField(default=0)),
                ('time_additional_days', models.IntegerField(default=0)),
                ('time_additional_hours', models.IntegerField(default=0)),
                ('time_additional_mins', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='recpie.Author')),
                ('favorites', models.ManyToManyField(blank=True, related_name='user_favorite', to='recpie.Author')),
            ],
        ),
    ]