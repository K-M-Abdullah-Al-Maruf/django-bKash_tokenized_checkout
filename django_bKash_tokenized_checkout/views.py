import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
from django.urls import resolve, reverse

__start_time = None
__token_expiration = None
__refresh_token_call_time = None

__grant_token_url = None
__refresh_token_url = None
__tokenized_create_payment_url = None
__non_tokenized_create_payment_url = None
__execute_payment_url = None
__query_payment_url = None
__query_agreement_url = None
__create_agreement_url = None
__execute_agreement_url = None
__cancel_agreement_url = None

__base_url = None
__redirect_url = None
__app_key = None
__app_secret = None
__username = None
__password = None

__id_token = None
__token_expires_in = None
__refresh_token = None
__payment_id = None
__price = None
__timeout_sec = 30

__agreement_ID = None
__agreement_status = None
__agreement_creation_request_id = None
__tokenized_payer_ref = None

def set_app_key(user_app_key):
    global __app_key
    __app_key = user_app_key

def get_app_key():
    global __app_key
    return __app_key

def set_app_secret_key(user_app_secret_key):
    global __app_secret
    __app_secret = user_app_secret_key

def get_app_secret_key():
    global __app_secret
    return __app_secret

def set_username(user_username):
    global __username
    __username = user_username

def get_username():
    global __username
    return __username


def set_password(user_password):
    global __password
    __password = user_password

def get_password():
    global __password
    return __password


def set_base_url(user_base_url):
    global __base_url
    __base_url = user_base_url

def get_base_url():
    global __base_url
    return __base_url

def set_redirect_url(user_redirect_url):
    global __redirect_url
    __redirect_url = user_redirect_url

def get_redirect_url():
    global __redirect_url
    return __redirect_url

def set_grant_token_api(user_grant_token_url):
    global __grant_token_url
    __grant_token_url = user_grant_token_url

def get_grant_token_api():
    global __grant_token_url
    return __grant_token_url

def set_refresh_token_api(user_refresh_token_url):
    global __refresh_token_url
    __refresh_token_url = user_refresh_token_url

def get_refresh_token_api():
    global __refresh_token_url
    return __refresh_token_url

def set_tokenized_create_payment_api(user_tokenized_create_payment_url):
    global __tokenized_create_payment_url
    __tokenized_create_payment_url = user_tokenized_create_payment_url

def get_tokenized_create_payment_api():
    global __tokenized_create_payment_url
    return __tokenized_create_payment_url

def set_non_tokenized_create_payment_api(user_non_tokenized_create_payment_url):
    global __non_tokenized_create_payment_url
    __non_tokenized_create_payment_url = user_non_tokenized_create_payment_url

def get_non_tokenized_payment_api():
    global __non_tokenized_create_payment_url
    return __non_tokenized_create_payment_url

def set_execute_payment_api(user_execute_payment_url):
    global __execute_payment_url
    __execute_payment_url = user_execute_payment_url

def get_execute_payment_api():
    global __execute_payment_url
    return __execute_payment_url

def set_create_agreement_api(user_create_agreement_url):
    global __create_agreement_url
    __create_agreement_url = user_create_agreement_url

def get_create_agreement_api():
    global __create_agreement_url
    return __create_agreement_url

def set_query_payment_api(user_query_payment_url):
    global __query_payment_url
    __query_payment_url = user_query_payment_url

def get_query_payment_api():
    global __query_payment_url
    return __query_payment_url

def set_query_agreement_api(user_query_agreement_url):
    global __query_agreement_url
    __query_agreement_url = user_query_agreement_url

def get_query_agreement_api():
    global __query_agreement_url
    return __query_agreement_url

def set_execute_agreement_api(user_execute_agreement_url):
    global __execute_agreement_url
    __execute_agreement_url = user_execute_agreement_url

def get_execute_agreement_api():
    global __execute_agreement
    return __execute_agreement

def set_cancel_agreement_api(user_cancel_agreement_url):
    global __cancel_agreement_url
    __cancel_agreement_url = user_cancel_agreement_url

def get_cancel_agreement_api():
    global __cancel_agreement_url
    return __cancel_agreement_url


def __time_calculation(time, token_time):
    __day = time.day
    __month = time.month
    __year = time.year
    
    if token_time > 86400:
            extra = token_time - 86400
            token_time = extra

            __day += 1

            if __month in [1,3,5,7,8,10,12]:
                if __day > 31:
                    __day = 1
                    __month += 1
                    if __month > 12:
                        __month = 1
                        __year += 1

            elif __month in [4,6,9,11]:
                if __day > 30:
                    __day = 1
                __month += 1
            else:
                if ( __year % 4 == 0 and __year % 100 != 0 ) or ( __year % 400 == 0 ):
                    if __day > 29:
                        __day = 1
                else:
                    if __day > 28:
                        __day = 28
                __month += 1

    return [__day,__month,__year, token_time]

def __token():
    global __start_time, __token_expiration, __refresh_token_call_time, __refresh_token

    __time = datetime.now(timezone.utc)

    __day = __time.day
    __month = __time.month
    __year = __time.year

    __hours = int(__time.strftime("%H"))
    __minutes = int(__time.strftime("%M"))
    __seconds = int(__time.strftime("%S"))
    __current_time_in_sec = (__hours*3600)+(__minutes*60)+__seconds

    if __refresh_token == None and __token_expiration == None:
        __grant_token()

    if __refresh_token_call_time == None or __token_expiration == None:
        __start_time = __time
        __refresh_token_call_time =  __time_calculation(__time, __current_time_in_sec+3300)
        __token_expiration = __time_calculation(__time, __current_time_in_sec+3600)

    if __refresh_token == None or __current_time_in_sec > __token_expiration[3] or __day > __token_expiration[0] or __month > __token_expiration[1] or __year > __token_expiration[2]:
        __refresh_token_call_time = None
        __token_expiration = None
        __grant_token()
    elif __refresh_token_call_time[3] < __current_time_in_sec < __token_expiration[3]:
        __refresh_token_call_time = None
        __generate_refresh_token()
    
def debugging_print(dict, name):
    i = 0
    print('\n\n',name,'\n\n{',sep='')
    for key in dict:
        i = i+1
        if i == len(dict):
            print('      "',key,'":"',dict.get(key),'"',sep='')
        else:    
            print('      "',key,'":"',dict.get(key),'",',sep='')
        print()
    print('}',end='\n\n')

def __grant_token():
    global __redirect_url, __grant_token_url, __start_time, __token_expiration, __grant_token_url, __refresh_token_url,__id_token, __token_expires_in, __refresh_token, __timeout_sec, __app_key, __app_secret, __username, __password, __base_url
    
    __grant_head = {
        'Content-Type':'application/json',
        'Accept':'application/json',
        'username':__username,
        'password':__password
    }

    __grant_body = {
        'app_key':__app_key,
        'app_secret':__app_secret
    }

    try:
        grant_api_response = (requests.post(__grant_token_url,headers=__grant_head,json=__grant_body, timeout=__timeout_sec)).json()
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__redirect_url+"/grant_token_api_data="+json.dumps({'message':'grant token api timeout'}))

    __id_token = grant_api_response.get("id_token")
    __token_expires_in = grant_api_response.get("expires_in")
    __refresh_token = grant_api_response.get("refresh_token")

    debugging_print(grant_api_response, 'Grant api response =')

def __generate_refresh_token():
    global __redirect_url, __refresh_token_url, __start_time, __token_expiration, __grant_token_url, __refresh_token_url,__id_token, __token_expires_in, __refresh_token, __timeout_sec, __app_key, __app_secret, __username, __password, __base_url

    __refresh_head = {
        'Content-Type':'application/json',
        'Accept':'application/json',
        'username':__username,
        'password':__password
    }

    __refresh_body = {
        'app_key':__app_key,
        'app_secret':__app_secret,
        'refresh_token':__refresh_token
    }

    try:
        refresh_token_api_response = (requests.post(__refresh_token_url, headers=__refresh_head, json=__refresh_body, timeout=__timeout_sec)).json()
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__redirect_url+"/?refresh_token_api_data="+json.dumps(json.dumps({'message':'refresh token api timeout'})))

    __token_expires_in=refresh_token_api_response.get('expires_in')
    __id_token=refresh_token_api_response.get('id_token')
    __refresh_token=refresh_token_api_response.get('refresh_token')
    
    debugging_print(refresh_token_api_response, 'Refresh api response =')

@csrf_exempt
def create_payment(request):  
    global __redirect_url, __non_tokenized_create_payment_url, __tokenized_create_payment_url, __id_token, __base_url, __timeout_sec, __agreement_status, __payment_id, __price
    
    __token()

    if __price == None:
        __price = request.POST.get('total_amount')
        
    if __agreement_status == "Completed":

        __tokenized_payment_head = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'Authorization':__id_token,
            'X-App-Key': __app_key
        }

        __tokenized_payment_body = {
            'mode':'0001',
            'payerReference':__tokenized_payer_ref,
            'callbackURL':f'{__base_url}/django_bKash_tokenized_checkout/execute_payment', 
            'agreementID':__agreement_ID,
            'amount':__price,
            'currency':'BDT',
            'intent':'sale',
            'merchantInvoiceNumber':'INV1',
            'merchantAssociationInfo':'MI05MID54RF09123456789'
        }

        try:
            __tokenized_payment_api_response = (requests.post(__tokenized_create_payment_url, headers=__tokenized_payment_head,json=__tokenized_payment_body, timeout=__timeout_sec)).json()
        except requests.exceptions.Timeout:
            return HttpResponseRedirect(__redirect_url+"/?tokenized_create_payment_api_data="+json.dumps({'message':'tokenized_create_payment_timeout'}))
        
        if ('statusCode' in __tokenized_payment_api_response and __tokenized_payment_api_response.get('statusCode') == '0000'):
            
            __payment_id = __tokenized_payment_api_response.get('paymentID')
            __bkashurl = __tokenized_payment_api_response.get('bkashURL')

            return HttpResponseRedirect(__bkashurl)
        else:
            return HttpResponseRedirect(__redirect_url+"/?tokenized_create_payment_api_data="+json.dumps(__tokenized_payment_api_response))



    else:
        __non_tokenized_create_payment_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'

        __checkout_head = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'Authorization':__id_token,
            'X-App-Key': __app_key
        }

        __checkout_body = {
            'mode':'0011',
            'payerReference':' ',
            'callbackURL':f'{__base_url}/django_bKash_tokenized_checkout/execute_payment',
            'amount':__price,
            'currency':'BDT',
            'intent':'sale',
            'merchantInvoiceNumber':'INV1',
            'merchantAssociationInfo':'MI05MID54RF09123456789'
        }

        try:
            __non_tokenized_payment_api_response = (requests.post(__non_tokenized_create_payment_url, headers=__checkout_head,json=__checkout_body, timeout=__timeout_sec)).json()
        except requests.exceptions.Timeout:
            return HttpResponseRedirect(__redirect_url+"/?non_tokenized_create_payment_api_data="+json.dumps({'message':'non tokenized payment api timeout'}))
        
        debugging_print( __non_tokenized_payment_api_response, "create payment response =")

        if ('statusCode' in  __non_tokenized_payment_api_response and  __non_tokenized_payment_api_response.get('statusCode') == '0000'):
            __payment_id =  __non_tokenized_payment_api_response.get('paymentID')
            __bkashurl =  __non_tokenized_payment_api_response.get('bkashURL')
            return HttpResponseRedirect(__bkashurl)
        else:
            return HttpResponseRedirect(__redirect_url+"/?non_tokenized_create_payment_api_data="+json.dumps(__non_tokenized_payment_api_response))


def __execute_payment(response):
    
    global __redirect_url, __payment_id, __execute_payment_url, __query_payment_url, __id_token, __base_url, __timeout_sec, __app_key, __price, __token_approved, __agreement_ID, __agreement_status

    __token()
    
    __execute_payment_head = {
    'Accept':'application/json',
    'Authorization': __id_token,
    'X-App-Key': __app_key
    }

    __execute_payment_body = {
        'paymentID': __payment_id
    }
    
    try: 
        __execute_payment_api_response = (requests.post(__execute_payment_url, headers=__execute_payment_head, json=__execute_payment_body, timeout=__timeout_sec)).json()
        
    except requests.exceptions.Timeout: 
      
        __query_payment_head ={
            'Content-Type':	"application/json",
            'Accept':'application/json',
            'Authorization': __id_token,
            'X-App-Key': __app_key
        }

        __query_payment_body = {
        'paymentID': __payment_id
        }
        
        try:
            __query_payment_api_response = (requests.post(__query_payment_url, headers=__query_payment_head,json=__query_payment_body, timeout=__timeout_sec)).json()
            debugging_print(__query_payment_api_response, 'query payment api response:')


        except requests.exceptions.Timeout:
            return HttpResponseRedirect(__redirect_url+"/?execute_payment_api_data="+json.dumps({'message':"query timeout"}))
        
        if __query_payment_api_response.get('status') == 'initiated':
            return HttpResponseRedirect(f'{__base_url}/django_bKash_tokenized_checkout/create_payment/')   #if initiated call create payment api
        elif __query_payment_api_response.get('status') == 'success':
            __execute_payment_api_response = __query_payment_api_response
        else:
            return HttpResponseRedirect(__redirect_url+"/?execute_agreement_api_data="+json.dumps(__query_payment_api_response))

    debugging_print(__execute_payment_api_response, 'Execute payment API response=')
    
    __price = None
    
    return HttpResponseRedirect(__redirect_url+"/?execute_payment_api_data="+json.dumps(__execute_payment_api_response))
    


@csrf_exempt
def create_agreement(request):
    global __create_agreement_url, __id_token, __app_key, __agreement_status, __agreement_creation_request_id, __price, __redirect_url

    __token()

    __create_agreement_head={
        'Content-Type':'application/json',
        'Accept':'application/json',
        'Authorization':__id_token,
        'X-App-Key': __app_key
    }
    
    __create_agreement_body = {
        "mode": "0000",
        "callbackURL": f'{__base_url}/django_bKash_tokenized_checkout/execute_agreement',
        "payerReference": " ",
    }

    try:
        __create_agreement_api_response = (requests.post(__create_agreement_url, headers=__create_agreement_head, json=__create_agreement_body, timeout=__timeout_sec)).json()
        print('create_agreement_api_response', __create_agreement_api_response)
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__redirect_url+"/?create_agreement_api_data="+json.dumps({'message':'create agreement api response timeout'}))
        
    if(__create_agreement_api_response.get('statusCode') == '0000'):
        __agreement_status=__create_agreement_api_response.get('agreementStatus')
        __agreement_creation_request_id=__create_agreement_api_response.get('paymentID')

        return HttpResponseRedirect(__create_agreement_api_response.get('bkashURL'))
    else:
        return HttpResponseRedirect(__redirect_url+"/?create_agreement_api_data="+json.dumps(__create_agreement_api_response))


def __execute_agreement(response): 
    global __redirect_url, __query_agreement_url, __execute_agreement_url, __id_token, __app_key, __timeout_sec, __agreement_creation_request_id, __agreement_ID, __agreement_status, __tokenized_payer_ref, __price
   
    __token()

    __execute_agreement_head = {
    'Accept':'application/json',
    'Authorization': __id_token,
    'X-App-Key': __app_key
    }

    __execute_agreement_body = {
        'paymentID': __agreement_creation_request_id
    }

    try:
        __execute_agreement_api_response=(requests.post(__execute_agreement_url, headers=__execute_agreement_head, json=__execute_agreement_body, timeout=__timeout_sec)).json()
    
    except requests.exceptions.Timeout:

        __query_agreement_head ={
            'Content-Type':	"application/json",
            'Accept':'application/json',
            'Authorization': __id_token,
            'X-App-Key': __app_key
        }

        __query_agreement_body = {
        'agreementID': __agreement_creation_request_id
        }

        try:
            __query_payment_api_response = (requests.post(__query_agreement_url, headers=__query_agreement_head,json=__query_agreement_body, timeout=__timeout_sec)).json()
        except requests.exceptions.Timeout:
            return HttpResponseRedirect(__redirect_url+"/?execute_agreement_api_data="+json.dumps({'message':'execute agreement api timeout'}))
        
        debugging_print(__query_payment_api_response, 'Query response api =')

        if __query_payment_api_response.get('status') == 'initiated':
            return HttpResponseRedirect(f'{__base_url}/django_bKash_tokenized_checkout/create_payment/')   #if initiated call create payment api
        elif __query_payment_api_response.get('status') == 'success':
            __execute_agreement_api_response = __query_payment_api_response
        else:
            return HttpResponseRedirect(__redirect_url+"/?execute_agreement_api_data="+json.dumps(__execute_agreement_api_response))
        
    __agreement_ID=__execute_agreement_api_response.get('agreementID')
    __agreement_status=__execute_agreement_api_response.get('agreementStatus')
    __tokenized_payer_ref=__execute_agreement_api_response.get('payerReference')

    debugging_print(__execute_agreement_api_response, 'execute agreement api =')
    
    return HttpResponseRedirect(__redirect_url+"/?execute_agreement_api_data="+json.dumps(__execute_agreement_api_response))

@csrf_exempt
def cancel_agreement(request):
    global __redirect_url, __cancel_agreement_url, __agreement_ID, __agreement_status, __token_approved

    __token()
    
    __cancel_agreement_head = {
    'Content-Type':"application/json",
    'Accept':'application/json',
    'Authorization': __id_token,
    'X-App-Key': __app_key
    }

    __cancel_agreement_body = {
        'agreementID': __agreement_ID
    }

    try:
        __cancel_agreement_api_response = (requests.post(__cancel_agreement_url, headers=__cancel_agreement_head, json=__cancel_agreement_body, timeout=__timeout_sec)).json()
        
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__redirect_url+"/?cancel_agreement_api_data="+json.dumps({'message':'cancel ageement api timeout'}))
    
    if (__cancel_agreement_api_response.get('statusCode') == '0000'):
        __agreement_ID = None
        __agreement_status = None
        __token_approved = False
        return HttpResponseRedirect(__redirect_url+"/?cancel_agreement_api_data="+json.dumps(__cancel_agreement_api_response))
    else:
        return HttpResponseRedirect(__redirect_url+"/?cancel_agreement_api_data="+json.dumps(__cancel_agreement_api_response))
