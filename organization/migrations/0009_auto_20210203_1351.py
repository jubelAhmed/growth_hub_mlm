# Generated by Django 3.1.5 on 2021-02-03 13:51

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20210203_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketing',
            name='market_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
