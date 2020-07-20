# Generated by Django 3.0.8 on 2020-07-20 23:21

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import recipe.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(max_length=320)),
                ('image', models.ImageField(default='recipe_image/default_recipe.jpg', upload_to='recipe_image')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('tags', recipe.models.ChoiceArrayField(base_field=models.CharField(choices=[('HH', 'Heart-Healthy'), ('QE', 'Quick&Easy'), ('LC', 'Low-Calorie'), ('GF', 'Gluten-Free'), ('DA', 'Diabetic'), ('VG', 'Vegetarian')], max_length=2), blank=True, size=None)),
                ('ingredients', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=450), size=None)),
                ('instructions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=320), size=None)),
                ('servings', models.IntegerField(default=1)),
                ('time_prep', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), size=3)),
                ('time_cook', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), size=3)),
                ('time_additional', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=0), size=3)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_user', to=settings.AUTH_USER_MODEL)),
                ('favorited_by', models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
