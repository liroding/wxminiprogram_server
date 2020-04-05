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
from django.core.cache import cache
#Get an instance of a loggger
logger = logging.getLogger('django')

# wx test app
#appid='wx0e09ec16b9a52aaf'
#appsecret='0e972dcc055cd8f5c60d3fe12dbc822e'

#this is my other app 
appid='wxe3d8a1aee3eed9b6'
appsecret='13dbc41accb74b6e1a14d525ddeedec9'

WEIXIN_TOKEN = 'ding'

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#appid='wxe3d8a1aee3eed9b6'
#appsecret='1c441d00be38e3ec66cd79ff287924ee'

url_code2Session='https://api.weixin.qq.com/sns/jscode2session?appid='+appid\
+'&secret='+appsecret+'&js_code='


url_accesstoken='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appid+'&secret='+appsecret

#sever should to get access token value on time (2 hours)
def get_accesstoken():
    print('[server-log]: to get access token value')
    res = requests.get(url_accesstoken)
    print(url_accesstoken)
    _dict = res.json()
    access_token = _dict['access_token'] #get session_key
    print(access_token)
    cache.set('access_token',access_token)

def checkauthsession(authsessioncode):
        print('authsession = '+ authsessioncode)
        has_authsession = 0
        authsession = authsessioncode
        if(authsession):
            print(authsession)
            all_usersmessage = usersmessagemysqldb.objects.all()
            #to find whether db have authsession
            i = 0
            while i < len(all_usersmessage):
                if authsession in all_usersmessage[i].authsession:    
                    has_authsession = 1
                    print('[server-log]: authsession match !!!')
                    return 1   #match 
                i +=1
            if has_authsession == 0:
                print('[server-log]: authsession no match !!!')
                return 0   #no match
class wxappstruct():
    
    
    def testfunc(request):
        print('[server-log]: hello world !!!')
        return HttpResponse('hello world')
    def wxsubscribes(request):
        find_openid = 0
        openid = 0
        
        print(cache.get('access_token'))
        token = cache.get('access_token')
       
        if request.method == 'POST':
           authsession = request.POST['authsession']
           subscribeid = request.POST['subscribeid']
           print(subscribeid)
           rflag = checkauthsession(authsession)
      
           if rflag == 0:
                return HttpResponse('Authsession no match')
           else:
                #start to get openid in mysqldb
                all_usersmessage = usersmessagemysqldb.objects.all()
                i = 0
                while i < len(all_usersmessage):
                    if authsession in all_usersmessage[i].authsession:    
                            find_openid = 1
                            openid = all_usersmessage[i].openid
                            name = all_usersmessage[i].name
                            print('[server-log]: openid =' + openid)
                            break
                    i +=1
                if find_openid == 0:
                    print('[server-log]: openid no match !!!')
                    return HttpResponse('Connot find openid')
                
                access_token = cache.get('access_token')
                nowtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
                if subscribeid == '1':
                    template_id = 'yknmtxHzvfU4rE84aa9si5LuV0gAW_7KGzEXz7FQgN0'
                    push_data = {
                         "thing1": {
                                   "value": 'Love'
                         },
                         "name2": {
                                   "value": 'chunxiaoxu'
                         },
                         "date4": {
                                   "value": nowtime
                         },
                         "phone_number3": {
                                   "value": '1314'
                         },
                      }
                elif subscribeid == '2':
                    template_id = '8qZXmYaPl9gJsUFQmhtDb73gvkP-lKFivLyroyTpeyI'
                    push_data = {
                        "thing1": {
                                  "value": name
                        },
                        "time3": {
                                  "value": nowtime
                        },
                      }

                if access_token:
                   print('[Server-log] <1>')
                   print(access_token)
                   print('[Server-log] <2>')
                   #start to get openid in mysqldb
                   # 如果存在accesstoken
                   payload = {
                               'touser': openid, #这里为用户的openid
                               'template_id': template_id, #模板id
                               'page': "pages/Preview/Preview",
                               'data': push_data #模板填充的数据
                   }


                   url_sendtemplate = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token='+access_token
                   print('[Server-log]:url_sendtemplate= '+ url_sendtemplate)
                   response = requests.post(url_sendtemplate,json=payload)
                   print(response)
                   print(response.json())
                   #直接返回res结果
                   #return JsonResponse(response.json())
                   return HttpResponse('1111111')
                else:
                   '''
                   return JsonResponse({
                         'err': 'access_token missing'
                })   
                   '''

                   return HttpResponse('222')

    def wxcheckSignature(request):
        
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
        token = WEIXIN_TOKEN
        tmp_list = [timestamp,nonce,token]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        sha = hashlib.sha1()
        sha.update(tmp_str.encode())
        tmp_str = sha.hexdigest()
        print('[server-log] signature:%s' % signature)
        if tmp_str == signature:
             return HttpResponse(echostr)
        else:
             return HttpResponse("weixin index")

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
    def handlecovertxls(request):
        authsession = request.POST['authsession']
        rflag = checkauthsession(authsession)
        if rflag == 1:
             os.system('python /home/liroding/workspace/wxminiprogram_server/wxapp/mysqlcovert_toxls.py')
             return HttpResponse('Server has coverted mysqldb to xls !!!')
        else:
             
             return HttpResponse('Authsession no match')
