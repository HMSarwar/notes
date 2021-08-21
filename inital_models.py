from django.db import models
from djrichtextfield.widgets import RichTextWidget
from django.template.defaultfilters import slugify
from django import forms

from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from djrichtextfield.models import RichTextField
from django.db.models.signals import pre_save





class Tag(models.Model):
    title = models.CharField(max_length=255)



class Notes(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    note_body = RichTextField()
    tag_list = models.CharField(max_length=4088, widget=forms.SelectMultiple)
    created_at = models.DateTimeField()
    deleted = models.IntegerField()



class NoteWisePermittedUser(models.Model):
    note_id = models.ForeignKey(Notes, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_type = models.IntegerField() # view only, edit permission


class Notification(models.Model):
    notification_type = models.IntegerField() # email. sms, push_notification
    notification_event = models.IntegerField() # create, edit, share event
    created_at = models.DateTimeField()
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField() # pending, tried, failed, success
    notification_template_id = models.IntegerField() # template for notification


class Email(models.Model):
    receiver = models.EmailField(blank=False)
    sender = models.EmailField(blank=False)
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE)
    subject = models.CharField(max_length=2048)
    message = RichTextField()
    cc = models.CharField(max_length=2048)
    bcc = models.CharField(max_length=2048)
    status = models.IntegerField()
    sent_at = models.DateTimeField()


class SMS(models.Model):
    receiver = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE)
    message = RichTextField()
    status = models.IntegerField()
    sent_at = models.DateTimeField()



class Token(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128) # hashed token
    expiry = models.DateTimeField()
    used = models.BooleanField()
    created_at = models.DateTimeField()
    used_at = models.DateTimeField()
