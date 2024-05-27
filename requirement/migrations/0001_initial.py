# Generated by Django 5.0.4 on 2024-05-28 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('major', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_no', models.CharField(max_length=2)),
                ('major_type', models.IntegerField(default=1)),
                ('main_major', models.IntegerField(default=0)),
                ('double_major', models.IntegerField(default=0)),
                ('minor_major', models.IntegerField(default=0)),
                ('liberal', models.IntegerField(default=0)),
                ('practical_foreign', models.IntegerField(default=0)),
                ('self_selection', models.IntegerField(default=0)),
                ('total_credit', models.IntegerField(default=0)),
                ('test_type', models.CharField(max_length=10)),
                ('flex', models.IntegerField(default=0)),
                ('flex_speaking', models.IntegerField(default=0)),
                ('toeic', models.IntegerField(default=0)),
                ('toeic_speaking', models.IntegerField(default=0)),
                ('opic', models.CharField(max_length=5)),
                ('major_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='major.major')),
            ],
            options={
                'unique_together': {('major_id', 'student_no', 'major_type')},
            },
        ),
    ]
