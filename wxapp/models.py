from django.db import models

# Create your models here.

class login(models.Model):
     username = models.CharField(max_length = 20,default='ding')
#    password = models.CharField(max_length = 20)
    #loginstatus = models.CharField(max_length = 20)
#    #authsession = models.CharField(max_length = 20)
    
class usersmessagemysqldb(models.Model):
    openid = models.CharField(max_length = 60,default='')
    loginstatus = models.CharField(max_length = 20,default='')
    authsession = models.CharField(max_length = 60,default='')
    nickname = models.CharField(max_length = 20,default='testname')
    
    #idusermessge
    name = models.CharField(max_length = 20,default='')
    sex = models.CharField(max_length = 20,default='')
    age = models.CharField(max_length = 20,default='')
    department = models.CharField(max_length = 20,default='')
    telephone = models.CharField(max_length = 20,default='')
   
    #patient case
    case1 = models.CharField(max_length = 50,default='')
    case2 = models.CharField(max_length = 50,default='')
    case3 = models.CharField(max_length = 50,default='')
    case4 = models.CharField(max_length = 50,default='')
    caseimg = models.CharField(max_length = 50,default='')
    status = models.CharField(max_length = 10,default = '0')
 #   status = models.IntegerField(default = '0')
    # def __str__(self):
    #    return 'username:'+ self.username
