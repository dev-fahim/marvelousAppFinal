# Generated by Django 2.1.5 on 2019-02-05 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=True)),
                ('uuid', models.UUIDField(unique=True)),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('base_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='base_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
