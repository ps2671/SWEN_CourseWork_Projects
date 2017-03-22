# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-04 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0007_auto_20161203_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='template_type',
            field=models.CharField(choices=[('PAPER_SUBMISSION_AUTHOR_NOTIF', 'Paper Submission Notification for Author'), ('PAPER_SUBMISSION_PCC_NOTIF', 'Paper Submission Notification for PCC'), ('REVIEW_REQUEST_PCM_NOTIF', 'Review Request Notification for PCM'), ('REVIEWS_COMPLETE_PCC_NOTIF', 'Reviews Complete Notification for PCC'), ('PAPER_SUBMISSION_REMINDER', 'Paper Submission Reminder for Authors'), ('PAPER_SUBMISSION_TODAY_REMINDER', 'Paper Submission Today Reminder for Authors'), ('REVIEW_REQUEST_REMINDER', 'Review Request Reminder for PCMs'), ('REVIEW_REQUEST_TODAY_REMINDER', 'Review Request Today Reminder for PCMs'), ('REVIEW_SUBMISSION_REMINDER', 'Review Submission Reminder for PCMs'), ('REVIEW_SUBMISSION_TODAY_REMINDER', 'Review Submission Today Reminder for PCMs')], max_length=50, unique=True),
        ),
    ]