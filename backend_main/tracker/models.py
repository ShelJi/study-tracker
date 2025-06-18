from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


SUBJECT_CHOICES = [
    ('Tam', 'Tamil'),
    ('Eng', 'English'),
    ('Math', 'Mathematics'),
    ('Sci', 'Science'),
    ('SS', 'Social Studies'),
    ('Comp', 'Computer Science'),
    ('Other', 'Other')
]


class StudyRecordModel(models.Model):
    """
    Model to store records of daily study datas.
    """
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Date")
    time_in = models.TimeField(verbose_name="Time In")
    time_out = models.TimeField(verbose_name="Time Out")
    total_duration = models.DurationField(verbose_name="Total Duration")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Study Record"
        verbose_name_plural = "Study Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.date}"
    
    def save(self, *args, **kwargs):
        dummy_date = datetime.today().date()
        in_dt = datetime.combine(dummy_date, self.time_in)
        out_dt = datetime.combine(dummy_date, self.time_out)

        if out_dt < in_dt:
            out_dt += timedelta(days=1)

        self.total_duration = out_dt - in_dt
        super().save(*args, **kwargs)
        

class SubjectRecordModel(models.Model):
    """
    Model to store records of daily study subjects.
    """
    user_sub = models.ForeignKey(StudyRecordModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, verbose_name="Subject", choices=SUBJECT_CHOICES)
    time_spent = models.DurationField(verbose_name="Time Spent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Subject Record"
        verbose_name_plural = "Subject Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject}"