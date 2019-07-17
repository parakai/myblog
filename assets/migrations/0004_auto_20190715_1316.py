# Generated by Django 2.1.8 on 2019-07-15 13:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20190712_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='name',
            new_name='hostname',
        ),
        migrations.AlterField(
            model_name='asset',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
