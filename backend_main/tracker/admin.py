from django.contrib import admin
from tracker.models import (StudyRecordModel,
                            SubjectRecordModel,
                            StaffModel,
                            StudentModel)


admin.site.register(StudyRecordModel)
admin.site.register(SubjectRecordModel)
admin.site.register(StaffModel)
admin.site.register(StudentModel)