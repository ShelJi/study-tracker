from django.contrib import admin
from tracker.models import (StudyRecordModel,
                            SubjectRecordModel)


admin.site.register(StudyRecordModel)
admin.site.register(SubjectRecordModel)