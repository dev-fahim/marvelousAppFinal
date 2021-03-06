# Generated by Django 2.1.5 on 2019-02-05 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base_user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditFundHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_updated', models.BooleanField(default=False)),
                ('is_restored', models.BooleanField(default=False)),
                ('old_description', models.TextField(blank=True, null=True)),
                ('new_description', models.TextField(blank=True, null=True)),
                ('old_fund_added', models.DateField()),
                ('new_fund_added', models.DateField()),
                ('old_amount', models.PositiveIntegerField()),
                ('new_amount', models.PositiveIntegerField()),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('old_uuid', models.UUIDField()),
                ('action_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_credit_fund_histories', to=settings.AUTH_USER_MODEL)),
                ('base_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_credit_fund_histories', to='base_user.BaseUserModel')),
            ],
        ),
        migrations.CreateModel(
            name='CreditFundModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveIntegerField()),
                ('uuid', models.UUIDField(unique=True)),
                ('fund_added', models.DateField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_refundable', models.BooleanField(default=False)),
                ('base_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_funds', to='base_user.BaseUserModel')),
            ],
        ),
        migrations.CreateModel(
            name='CreditFundSettingsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_not_locked', models.BooleanField(default=False)),
                ('base_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fund_settings', to='base_user.BaseUserModel')),
            ],
        ),
        migrations.CreateModel(
            name='CreditFundSourceHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_updated', models.BooleanField(default=False)),
                ('is_restored', models.BooleanField(default=False)),
                ('old_source_name', models.CharField(max_length=120)),
                ('new_source_name', models.CharField(max_length=120)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('old_uuid', models.UUIDField()),
                ('action_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_credit_fund_source_histories', to=settings.AUTH_USER_MODEL)),
                ('base_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_credit_fund_source_histories', to='base_user.BaseUserModel')),
            ],
        ),
        migrations.CreateModel(
            name='CreditFundSourceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('base_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_fund_sources', to='base_user.BaseUserModel')),
            ],
        ),
        migrations.AddField(
            model_name='creditfundsourcehistorymodel',
            name='credit_fund_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_histories', to='credit.CreditFundSourceModel'),
        ),
        migrations.AddField(
            model_name='creditfundmodel',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funds', to='credit.CreditFundSourceModel'),
        ),
        migrations.AddField(
            model_name='creditfundhistorymodel',
            name='credit_fund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_histories', to='credit.CreditFundModel'),
        ),
        migrations.AddField(
            model_name='creditfundhistorymodel',
            name='new_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_new_histories', to='credit.CreditFundSourceModel'),
        ),
        migrations.AddField(
            model_name='creditfundhistorymodel',
            name='old_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_old_histories', to='credit.CreditFundSourceModel'),
        ),
    ]
