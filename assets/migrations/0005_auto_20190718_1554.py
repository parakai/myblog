# Generated by Django 2.1.8 on 2019-07-18 15:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20190715_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('is_admin', models.BooleanField(default=False, verbose_name='is_Admin')),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=50, null=True, verbose_name='密码')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appusers', to='assets.AppInfo', verbose_name='应用')),
            ],
            options={
                'verbose_name': '应用用户管理',
                'verbose_name_plural': '应用用户管理',
            },
        ),
        migrations.CreateModel(
            name='AssetUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('is_admin', models.BooleanField(default=False, verbose_name='is_Admin')),
                ('username', models.CharField(max_length=50, verbose_name='用户名')),
                ('password', models.CharField(blank=True, max_length=50, null=True, verbose_name='密码')),
            ],
            options={
                'verbose_name': '资产用户管理',
                'verbose_name_plural': '资产用户管理',
            },
        ),
        migrations.RemoveField(
            model_name='userprofilemanager',
            name='app',
        ),
        migrations.RemoveField(
            model_name='userprofilemanager',
            name='asset',
        ),
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ['ip'], 'verbose_name': '资产', 'verbose_name_plural': '资产'},
        ),
        migrations.DeleteModel(
            name='UserProfileManager',
        ),
        migrations.AddField(
            model_name='asset',
            name='assetuser',
            field=models.ManyToManyField(related_name='assets', to='assets.AssetUser'),
        ),
    ]
