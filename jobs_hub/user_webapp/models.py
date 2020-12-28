from django.db import models
from common_webapp.models import Account
# Create your models here.

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('For Both', 'For Both'),
)
COURSE_TYPE = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Correspondene', 'Correspondence'),
)
class GernalInfo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.IntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    user_id_proof = models.FileField(upload_to='media/documents/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name_plural = "Gernal Info"

class EducationInfo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    university_name = models.CharField(max_length=100, null=True, blank=True)
    college_name = models.CharField(max_length=100, null=True, blank=True)
    course_type = models.CharField(choices=COURSE_TYPE, max_length=50, null=True, blank=True)
    passing_out_year = models.CharField(max_length=50, null=True, blank=True)
    grading_system = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.education

    class Meta:
        verbose_name_plural = "EducationInfo"

class ExperienceInfo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    organisation_name = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=25, null=True, blank=True)
    starting_date = models.DateField(null=True, blank=True)
    ending_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    upload_documents = models.FileField(upload_to='media/documents/%Y/%m%d/', null=True, blank=True)

    def __str__(self):
        return self.organisation_name

    class Meta:
        verbose_name_plural = "ExperienceInfo"

class JobPreference(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    job_category = models.CharField(max_length=100, null=True, blank=True)
    location_range = models.CharField(max_length=150, null=True, blank=True)
    own_reliable_transportation = models.BooleanField(default=False)
    preferred_pay_rate_for_different_job_positions = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.job_category

    class Meta:
        verbose_name_plural = "JobPreference"

class CertificationInfo(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='media/images/%Y/%m%d/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "CertificationInfo"

class Language(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    lanuage = models.CharField(max_length=50, null=True, blank=True)
    spoken = models.CharField(max_length=50, null=True, blank=True)
    written = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.lanuage

    class Meta:
        verbose_name_plural = "Language"

    