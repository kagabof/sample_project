# Generated by Django 4.0.1 on 2022-01-27 15:51

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import hashes_apps.utils.generators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hash',
            fields=[
                ('id', models.CharField(default=hashes_apps.utils.generators.id_generater, editable=False, max_length=9, primary_key=True, serialize=False)),
                ('added_timestamp', models.DateTimeField(auto_now_add=True)),
                ('hash', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hashes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-added_timestamp'],
            },
        ),
    ]
