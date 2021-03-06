# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-04 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0008_auto_20161204_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentsubmission',
            name='finalRating',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='event_type',
            field=models.CharField(choices=[('PAPER_SUBMISSION', 'Paper Submission'), ('ACCOUNT_UPDATE', 'Account Update'), ('PCM_ACCOUNT_DELETION', 'PCM Account Deletion'), ('PCM_ASSIGNED_PAPER', 'PCM Assigned Paper'), ('REVIEWS_COMPLETE', 'Reviews Complete'), ('PAPER_SUBMISSION_REMINDER', 'Paper Submission Reminder'), ('PCM_SUBMIT_REVIEW', 'PCM Submit Review'), ('PCM_SUBMIT_REVIEW_LIST', 'PCM Submit Review List'), ('FINAL_RATING', 'Final Rating for submission is complete'), ('REVIEW_CONFLICT', 'Review Conflict')], max_length=50),
        ),
        migrations.AlterField(
            model_name='template',
            name='template_type',
            field=models.CharField(choices=[('PAPER_SUBMISSION_AUTHOR_NOTIF', 'Paper Submission Notification for Author'), ('PAPER_SUBMISSION_PCC_NOTIF', 'Paper Submission Notification for PCC'), ('REVIEW_REQUEST_PCM_NOTIF', 'Review Request Notification for PCM'), ('REVIEWS_COMPLETE_PCC_NOTIF', 'Reviews Complete Notification for PCC'), ('USER_ACCOUNT_UPDATE_NOTIF', 'User Account Update Notification')], max_length=50, unique=True),
        ),
    ]
