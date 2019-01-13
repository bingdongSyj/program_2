from django.db import models

# Create your models here.


class DataInfo(models.Model):
    cityid = models.CharField(max_length=5)
    category = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    salary = models.CharField(max_length=100, null=True)
    emp_type = models.CharField(max_length=100, null=True)
    working_exp = models.CharField(max_length=100, null=True)
    edu_level = models.CharField(max_length=100, null=True)
    company_type = models.CharField(max_length=100, null=True)
    company_size = models.CharField(max_length=100, null=True)
    company_url = models.CharField(max_length=200, null=True)
    emp_num = models.CharField(max_length=10, null=True)
    main_business = models.CharField(max_length=100, null=True)
    company_website = models.CharField(max_length=100, null=True)
    company_welfare = models.CharField(max_length=200, null=True)
    company_introduce = models.TextField()
    city = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'xpath_and_more'
