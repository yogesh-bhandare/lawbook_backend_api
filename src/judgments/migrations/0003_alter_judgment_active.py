# Generated by Django 5.1.3 on 2024-11-20 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judgments', '0002_alter_judgment_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judgment',
            name='active',
            field=models.BooleanField(default=False, help_text='Scrape daily?'),
        ),
    ]