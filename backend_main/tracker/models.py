from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


SUBJECT_CHOICES = [
    ('Tam', 'Tamil'),
    ('Eng', 'English'),
    ('Math', 'Mathematics'),
    ('Sci', 'Science'),
    ('SS', 'Social Studies'),
    ('Comp', 'Computer Science'),
    ('Other', 'Other')
]


class StaffModel(models.Model):
    """
    Model to store staff details.
    """
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name}"
    

class StudentModel(models.Model):
    """
    Model to store student details.
    """
    user_name = models.CharField(max_length=100, verbose_name="Student Name", null=True, blank=True)
    staff = models.ForeignKey(StaffModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Staff")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name}"


class StudyRecordModel(models.Model):
    """
    Model to store records of daily study datas.
    """
    user_name = models.ForeignKey(StaffModel, on_delete=models.CASCADE, verbose_name="Staff Name", null=True, blank=True)
    student_name = models.ForeignKey(StudentModel, verbose_name="Student", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(verbose_name="Date")
    time_in = models.TimeField(verbose_name="Time In")
    time_out = models.TimeField(verbose_name="Time Out")
    total_duration = models.DurationField(verbose_name="Total Duration", null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Study Record"
        verbose_name_plural = "Study Records"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.student_name} - {self.date}"
    
    def save(self, *args, **kwargs):
        
        if not (self.user_name or self.student_name):
            raise ValidationError("Either user_name or student_name must be provided.")
            
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
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    total_2_mark = models.IntegerField(verbose_name="Total 2 Mark Questions Learned", default=0)
    total_5_mark = models.IntegerField(verbose_name="Total 2 Mark Questions Learned", default=0)
    other_qn = models.IntegerField(verbose_name="Other Learned", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Subject Record"
        verbose_name_plural = "Subject Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.user_sub.student_name} - {self.created_at.strftime('%Y-%m-%d')}"
    
    
