# Generated by Django 2.0.7 on 2018-07-26 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appgu', '0009_auto_20180725_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsposts',
            name='writtenby',
            field=models.ForeignKey(db_column='dealerID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]