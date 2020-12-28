from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(JobCategory)
admin.site.register(JobSubCategory)
admin.site.register(PostAJob)
admin.site.register(BlogCategory)
admin.site.register(Blog)