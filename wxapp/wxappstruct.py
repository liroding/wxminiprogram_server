from django.contrib import admin
import os,sys
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render,render_to_response
from django.template.context import RequestContext
import requests
import hashlib
from wxapp.models import usersmessagemysqldb
import time
import logging

#Get an instance of a loggger
logger = logging.getLogger('django')

# wx test app
#appid='wx0e09ec16b9a52aaf'
#appsecret='0e972dcc055cd8f5c60d3fe12dbc822e'

#this is my other app 
appid='wxe3d8a1aee3eed9b6'
appsecret='13dbc41accb74b6e1a14d525ddeedec9'



PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#appid='wxe3d8a1aee3eed9b6'
#appsecret='1c441d00be38e3ec66cd79ff287924ee'
url_code2Session='https://api.weixin.qq.com/sns/jscode2session?appid='+appid\
+'&secret='+appsecret+'&js_code='
class wxappstruct():
    def testfunc(request):
        print('[server-log]:hello world')
        return HttpResponse("Hello World")
    def onlogin(request):
        has_user = 0
        wx_code = request.GET['code']
        username = request.GET['username']
        print('[server-log]:onlogin func for (res.code)')
        print('[server-log]:wx_code:'+wx_code)
        print('[server-log]:username:'+username)
        tmpurl=url_code2Session+wx_code+'&grant_type=authorization_code'
        print(tmpurl)
        res = requests.get(tmpurl)
        _dict = res.json()
        session_key = _dict['session_key'] #get session_key
        openid = _dict['openid']
        #get authsession
        sha = hashlib.sha1()
        sha.update(openid.encode())
        authsession = sha.hexdigest() #define our session for auth
        print('[server-log]:authsession:' + authsession)
        #storage username & openid to db
        all_usersmessage = usersmessagemysqldb.objects.all()
        #to find whether db have openid data
        i = 0
        while i < len(all_usersmessage):
                if openid in all_usersmessage[i].openid:    
                    has_user = 1
                    print('[server-log]: db has this username information')
                    break
                i +=1
        if has_user == 0:
                print('[server-log]: db do not this openid,then to storage')
                usermessage = usersmessagemysqldb()
                usermessage.authsession = authsession
                usermessage.openid = openid
                usermessage.nickname = username
                usermessage.save()
        print('[server-log]:wxserver return the data :'+ str(res.json()))
        #return HttpResponse('key 12')
        return JsonResponse({'authsession':authsession})

    def idmessagehandle(request):
        has_authsession = 0
        name = request.POST['name']
        sex = request.POST['checkbox']
        age = request.POST['age']
        department = request.POST['department']
        telephone = request.POST['telephone']
        authsession = request.POST['authsession']
        if(authsession):
            print(authsession)
            all_usersmessage = usersmessagemysqldb.objects.all()
            #to find whether db have authsession
            i = 0
            while i < len(all_usersmessage):
                if authsession in all_usersmessage[i].authsession:    
                    has_authsession = 1
                    print('[server-log]: authsession pass !!!')
                    #do logic demand handle
                    all_usersmessage[i].name = name
                    all_usersmessage[i].sex = sex
                    all_usersmessage[i].age = age
                    all_usersmessage[i].department = department
                    all_usersmessage[i].telephone = telephone
                    all_usersmessage[i].save()
                    print('[server-log]:update the database finish !!!')
                    return HttpResponse('Sever has update the database !')
                    
                i +=1
            if has_authsession == 0:
                print('[server-log]: authsession no match !!!')
                return HttpResponse('attach authsession is error,no matching with userid(openid)')
        return HttpResponse('attach authsession is null !!!')

    def fileupload(request):
        if request.method == "POST":
            image_file = request.FILES.get('file')
            authsession = request.POST['authsession']
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
            filename = nowtime  #this is UTC time,hour shoud +8 will be beijing time
            print(filename)
            #storage the file to server
            path = PROJECT_ROOT + '/static/uploads/' #django env
            logger.info('info')
            logger.debug('debug')
            logger.error('error')
	    #print(path) 
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + filename + '.PNG','wb+') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
            
                all_usersmessage = usersmessagemysqldb.objects.all()
                #to find whether db have authsession
                i = 0
                while i < len(all_usersmessage):
                    #print('<1>' + authsession)
                    #print('<2>' + all_usersmessage[i].authsession)
                    if authsession == all_usersmessage[i].authsession:    
                       all_usersmessage[i].caseimg = filename + '.PNG'
                       all_usersmessage[i].save()
                       print('[server-log]:storage the upload picture !!')
                       return HttpResponse('Sever has update the database !')
                    i +=1
        else:
            return HttpResponse('server cannot handle GET request !!!!')
        print('[server-log]:fileupload')
        return HttpResponse('file upload success !!!')
    def querymysqldb(request):
        has_authsession = 0
        reqid = request.POST['reqid']
        authsession = request.POST['authsession']
        logger.info('[server-log]:'+ reqid)
        if(authsession):
            print(authsession)
            all_usersmessage = usersmessagemysqldb.objects.all()
            #to find whether db have authsession
            i = 0
            while i < len(all_usersmessage):
                if authsession in all_usersmessage[i].authsession:    
                    has_authsession = 1
                    print('[server-log]: authsession pass !!!')
                    #do logic demand handle
                    if reqid == '3':
 
                        name = all_usersmessage[i].name
                        logger.info('[server-log]:name ='+ name)
                        sex  = all_usersmessage[i].sex
                        age  = all_usersmessage[i].age
                        department =  all_usersmessage[i].department
                        telephone = all_usersmessage[i].telephone
                        print('[server-log]:get the database data !!!')
                        return JsonResponse({'authsession':authsession,'name':name,\
                                             'sex':sex,'age':age,'department':department, \
                                             'telephone':telephone  \
                                       })
                    
                i +=1
            if has_authsession == 0:
                print('[server-log]: authsession no match !!!')
                return HttpResponse('attach authsession is error,no matching with userid(openid)')
        return HttpResponse('attach authsession is null !!!')
    def patientcasehandle(request):
        logger.info('[server-log]:enter patient case handle')
        has_authsession = 0
        itemsdata = request.POST['itemsdata']
        itemsdata_2 = request.POST['itemsdata_2']
        authsession = request.POST['authsession']
        #_list = list(itemsdata)
        #logger.info(_list[])
        logger.info('[server-log]: itemsdata_2= '+ itemsdata_2)
        if(authsession):
            print(authsession)
            all_usersmessage = usersmessagemysqldb.objects.all()
            #to find whether db have authsession
            i = 0
            while i < len(all_usersmessage):
                if authsession in all_usersmessage[i].authsession:    
                    has_authsession = 1
                    print('[server-log]: authsession pass !!!')
                    #do logic demand handle
                    #all_usersmessage[i].case1 = itemsdata
                    #all_usersmessage[i].case2 = itemsdata_2
                    #all_usersmessage[i].save()
                    print('[server-log]:update the database finish !!!')
                    return HttpResponse('Sever has update the database !')
                    
                i +=1
            if has_authsession == 0:
                print('[server-log]: authsession no match !!!')
                return HttpResponse('attach authsession is error,no matching with userid(openid)')
        return HttpResponse('attach authsession is null !!!')
