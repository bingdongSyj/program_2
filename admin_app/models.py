from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)#昵称
    email = models.EmailField()
    phone=models.CharField(max_length=15)#电话
    password = models.CharField(max_length=100)#密码
    status = models.BooleanField(default=False)#状态
    c_time=models.DateTimeField(auto_now_add=True)#创建时间
    class Meta:
        db_table = 'user'