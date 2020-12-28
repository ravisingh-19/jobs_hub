from django.contrib import admin
from .models import (GernalInfo, EducationInfo, ExperienceInfo, 
JobPreference, CertificationInfo, Language)

# Register your models here.
admin.site.register(GernalInfo)
admin.site.register(EducationInfo)
admin.site.register(ExperienceInfo)
admin.site.register(JobPreference)
admin.site.register(CertificationInfo)
admin.site.register(Language)

