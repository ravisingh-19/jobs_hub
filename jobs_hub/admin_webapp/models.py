from django.db import models
from common_webapp.models import Account

# Create your models here.

JOB_TYPE = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Freelance', 'Freelancer'),
)


GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('For Both', 'For Both'),
)

PAY_TYPE = (
    ('Fixed Pay', 'Fixed Pay'),
    ('Hourly Pay', 'Hourly Pay'),
    ('Weekly Pay', 'Weekly Pay'),
    ('Daily Pay', 'Daily Pay'),
    ('Monthly Pay', 'Monthly Pay'),
)

class JobCategory(models.Model):
    job_category_name = models.CharField(max_length=100, null=True, blank=True)
    job_category_value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.job_category_name
    class Meta:
        verbose_name_plural = "JobCategory"

class JobSubCategory(models.Model):
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True, blank=True)
    job_sub_category = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return self.job_category.job_category_name+":-"+self.job_sub_category

    class Meta:
        verbose_name_plural = "JobSubCategory"

class PostAJob(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, null=True, blank=True)
    job_sub_category = models.ForeignKey(JobSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    job_type = models.CharField(choices=JOB_TYPE, max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    age_limit = models.IntegerField(null=True, blank=True)
    uniform = models.CharField(max_length=150, blank=True)
    pay_type = models.CharField(choices=PAY_TYPE, max_length=50, null=True, blank=True)
    pay_rate = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    no_of_openning = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    location_instructor = models.CharField(max_length=150, null=True, blank=True)
    parking = models.CharField(max_length=50, null=True, blank=True)
    break_time = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    preference = models.CharField(max_length=50, null=True, blank=True)
    appearance_preference = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True)
    view_applicants = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.job_category.job_category_name+ ":-" +self.job_sub_category.job_sub_category

    class Meta:
        verbose_name_plural = "PostAJob"

class BlogCategory(models.Model):
    blog_category_name = models.CharField(max_length=100, null=True, blank=True)
    blog_category_value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.blog_category_name

    class Meta:
        verbose_name_plural = "BlogCategory"

class Blog(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    upload_feature_image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    paragraph_content = models.TextField(null=True, blank=True)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True)
    author_name = models.CharField(max_length=50, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.blog_category.blog_category_name+ ":-" +self.title
    
    class Meta:
        verbose_name_plural = "Blog"
