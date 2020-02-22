from django.db import models

# Create your models here.

class login(models.Model):
     username = models.CharField(max_length = 20,default='ding')
#    password = models.CharField(max_length = 20)
    #loginstatus = models.CharField(max_length = 20)
#    #authsession = models.CharField(max_length = 20)
    
class usersmessagemysqldb(models.Model):
    openid = models.CharField(max_length = 60,null = True)
    loginstatus = models.CharField(max_length = 20,null = True)
    authsession = models.CharField(max_length = 60,null =True)
    nickname = models.CharField(max_length = 20,default='testname')
    
    #idusermessge

    name = models.CharField(max_length = 20,null = True)
    sex = models.CharField(max_length = 20,null = True)
    age = models.CharField(max_length = 20,null = True)
    department = models.CharField(max_length = 20,null = True)
    telephone = models.CharField(max_length = 20,null = True)
   
    #patient case
    caseimg = models.CharField(max_length = 50,null = True)
    # def __str__(self):
    #    return 'username:'+ self.username
