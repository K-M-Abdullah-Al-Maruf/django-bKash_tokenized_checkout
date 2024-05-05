import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone

# __base_url = 'http://127.0.0.1:8000'

# __app_key = '4f6o0cjiki2rfm34kfdadl1eqq'
# __app_secret = '2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b'

# __username = 'sandboxTokenizedUser02'
# __password = 'sandboxTokenizedUser02@12345'

__start_time = None
# __test_time = None
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
    print("username is =",__username)
    __username = user_username
    print("after replacing username is =",__username)

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


def __time_precesion(time, token_time):
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
        __refresh_token_call_time =  __time_precesion(__time, __current_time_in_sec+3300) #3300
        __token_expiration = __time_precesion(__time, __current_time_in_sec+3600) #3600

    print("current_time =", __time)
    print("start_time =", __start_time)
    print("end_time =", __time)
    print("time Y =", __time.year)
    print()
    print("time_comparison <=", __start_time < __time)
    print("time_comparison >=", __start_time > __time)
    print("time_comparison ===", __start_time == __time)

    print("Hours =", __hours )
    print("minutes =", __minutes)
    print("seconds =", __seconds)
    print("__token_expiration seconds =", __token_expiration)
    print("current_total seconds =", __current_time_in_sec)

    if __refresh_token == None or __current_time_in_sec > __token_expiration[3] or __day > __token_expiration[0] or __month > __token_expiration[1] or __year > __token_expiration[2]:
        print("\n\n\ncalling grant")
        print("refresh token =", __refresh_token)
        __refresh_token_call_time = None
        __token_expiration = None
        __grant_token()
    elif __refresh_token_call_time[3] < __current_time_in_sec < __token_expiration[3]:
        print("\n\n\ncalling refresh")
        __refresh_token_call_time = None
        __generate_refresh_token()
    else:
        print("skipping")
    
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
    global __grant_token_url, __start_time, __token_expiration, __grant_token_url, __refresh_token_url,__id_token, __token_expires_in, __refresh_token, __timeout_sec, __app_key, __app_secret, __username, __password, __base_url

    #Grant api for token
    # grant_url = f'{__base_url}/tokenized/checkout/token/grant'

    # __grant_token_url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"
    print("grant_url =",__grant_token_url)

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
        return HttpResponseRedirect(__base_url+"/grant_token_api_data="+json.dumps({'message':'grant token api timeout'}))

    __id_token = grant_api_response.get("id_token")
    __token_expires_in = grant_api_response.get("expires_in")
    __refresh_token = grant_api_response.get("refresh_token")

    # __token()

    debugging_print(grant_api_response, 'Grant api response =')

def __generate_refresh_token():
    global __refresh_token_url, __start_time, __token_expiration, __grant_token_url, __refresh_token_url,__id_token, __token_expires_in, __refresh_token, __timeout_sec, __app_key, __app_secret, __username, __password, __base_url


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

    #refresh_token_url = f'{__base_url}/tokenized/checkout/token/refresh'
    # __refresh_token_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/refresh'

    try:
        refresh_token_api_response = (requests.post(__refresh_token_url, headers=__refresh_head, json=__refresh_body, timeout=__timeout_sec)).json()
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__base_url+"/?refresh_token_api_data="+json.dumps(json.dumps({'message':'refresh token api timeout'})))

    __token_expires_in=refresh_token_api_response.get('expires_in')
    __id_token=refresh_token_api_response.get('id_token')
    __refresh_token=refresh_token_api_response.get('refresh_token')
    
    # __token()

    debugging_print(refresh_token_api_response, 'Refresh api response =')

@csrf_exempt
def create_payment(request):  
    global __non_tokenized_create_payment_url, __tokenized_create_payment_url, __id_token, __base_url, __timeout_sec, __agreement_status, __payment_id, __price
    
    __token()

    # remove the comments for line 163-164 and delete line 165 ****
    if __price == None:
        __price = request.POST.get('amount_textfield')
    # __price = 22
    print('in create payment and agreement status =', __agreement_status)
    if __agreement_status == "Completed":
        #Create tokenized payment api
        # __tokenized_create_payment_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'

        __tokenized_payment_head = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'Authorization':__id_token,
            'X-App-Key': __app_key
        }

        __tokenized_payment_body = {
            'mode':'0001',
            'payerReference':__tokenized_payer_ref,
            'callbackURL':f'{__base_url}/django_bKash_tokenized_chekout/execute_payment', 
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
            return HttpResponseRedirect(__base_url+"/?tokenized_create_payment_api_data="+json.dumps({'message':'tokenized_create_payment_timeout'}))
        
        
        if ('statusCode' in __tokenized_payment_api_response and __tokenized_payment_api_response.get('statusCode') == '0000'):
            print("tokenized create payment response", __tokenized_payment_api_response,'\n')
            payment_id = __tokenized_payment_api_response.get('paymentID')
            bkashurl = __tokenized_payment_api_response.get('bkashURL')
            print('bkash url =', bkashurl)
            print('redirecting to bkashurl')
            return HttpResponseRedirect(bkashurl)
        else:
            return HttpResponseRedirect(__base_url+"/?tokenized_create_payment_api_data="+json.dumps(__tokenized_payment_api_response))



    else:
        #Create payment Api
        # __non_tokenized_create_payment_url = f'{__base_url}/tokenized/checkout/create'
        __non_tokenized_create_payment_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'

        __checkout_head = {
            'Content-Type':'application/json',
            'Accept':'application/json',
            'Authorization':__id_token,
            'X-App-Key': __app_key
        }

        __checkout_body = {
            'mode':'0011',
            'payerReference':'01619777283',
            'callbackURL':f'{__base_url}/django_bKash_tokenized_chekout/execute_payment',
            'amount':__price,
            'currency':'BDT',
            'intent':'sale',
            'merchantInvoiceNumber':'INV1',
            'merchantAssociationInfo':'MI05MID54RF09123456789'
        }

        try:
             __non_tokenized_payment_api_response = (requests.post(__non_tokenized_create_payment_url, headers=__checkout_head,json=__checkout_body, timeout=__timeout_sec)).json()
        except requests.exceptions.Timeout:
            return HttpResponseRedirect(__base_url+"/?non_tokenized_create_payment_api_data="+json.dumps({'message':'non tokenized payment api timeout'}))
        print("before debugging print")
        debugging_print( __non_tokenized_payment_api_response, "create payment response =")

        if ('statusCode' in  __non_tokenized_payment_api_response and  __non_tokenized_payment_api_response.get('statusCode') == '0000'):
            __payment_id =  __non_tokenized_payment_api_response.get('paymentID')
            __bkashurl =  __non_tokenized_payment_api_response.get('bkashURL')
            return HttpResponseRedirect(__bkashurl)
        else:
            return HttpResponseRedirect(__base_url+"/?non_tokenized_create_payment_api_data="+json.dumps(__non_tokenized_payment_api_response))


def __execute_payment(response):
    print('inside result')
    global __payment_id, __execute_payment_url, __query_payment_url, __id_token, __base_url, __timeout_sec, __app_key, __price, __token_approved, __agreement_ID, __agreement_status

    __token()

    # __current_url = response.get_full_path()

    #Handling the error case when payment is canceled with cancel button in bkash url rather then give a error
    # if 'cancel' in __current_url:
    #     print('agreement status', __agreement_status)
    #     if __agreement_ID == None:
    #         return HttpResponseRedirect(__base_url)
    #     else:
    #         if __token_approved:
    #             return HttpResponseRedirect(__base_url+"/tokenized_homepage/")
    #         else:
    #             return HttpResponseRedirect(__base_url+"/cancel_agreement/")
            
    #Execute payment api
    __execute_payment_head = {
    'Accept':'application/json',
    'Authorization': __id_token,
    'X-App-Key': __app_key
    }

    __execute_payment_body = {
        'paymentID': __payment_id
    }
    
    # execute_payment_url = f'{__base_url}/tokenized/checkout/execute'
    # __execute_payment_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute'

    try: 
        __execute_payment_api_response = (requests.post(__execute_payment_url, headers=__execute_payment_head, json=__execute_payment_body, timeout=__timeout_sec)).json()
        
    except requests.exceptions.Timeout: 
        #Query payment api
        # query_payment_url = f"{__base_url}/tokenized/checkout/payment/status"
        # __query_payment_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status'

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
            return HttpResponseRedirect(__base_url+"/?execute_payment_api_data="+json.dumps({'message':"query timeout"}))
        
        # query_payment_api_response['status'] = 'initiated' or 'success'
        if __query_payment_api_response.get('status') == 'initiated':
            return HttpResponseRedirect(f'{__base_url}/create_payment/')   #if initiated call create payment api
        else:
            __execute_payment_api_response = __query_payment_api_response
    debugging_print(__execute_payment_api_response, 'Execute payment API response=')
    __price = None
    
    
    return HttpResponseRedirect(__base_url+"/?execute_payment_api_data="+json.dumps(__execute_payment_api_response))


@csrf_exempt
def create_agreement(request):
    global __create_agreement_url, __id_token, __app_key, __agreement_status, __agreement_creation_request_id, __price

    __token()

    # __create_agreement_url = f'{__base_url}/tokenized/checkout/create'
    # __create_agreement_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'
    
    __create_agreement_head={
        'Content-Type':'application/json',
        'Accept':'application/json',
        'Authorization':__id_token,
        'X-App-Key': __app_key
    }
    
    __create_agreement_body = {
        "mode": "0000",
        "callbackURL": f'{__base_url}/django_bKash_tokenized_chekout/execute_agreement',
        "payerReference": "01619777283",
    }

    try:
        __create_agreement_api_response = (requests.post(__create_agreement_url, headers=__create_agreement_head, json=__create_agreement_body, timeout=__timeout_sec)).json()
        print('create_agreement_api_response', __create_agreement_api_response)
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__base_url+"/?create_agreement_api_data"+json.dumps({'message':'create agreement api response timeout'}))
        
    
    if(__create_agreement_api_response.get('statusCode') == '0000'):
        __agreement_status=__create_agreement_api_response.get('agreementStatus')
        __agreement_creation_request_id=__create_agreement_api_response.get('paymentID')

        print("agreement status =", __agreement_status)
        print("agreement_creation_request_id", __agreement_creation_request_id)
        print("create agreement --> bkashurl")
        return HttpResponseRedirect(__create_agreement_api_response.get('bkashURL'))
    else:
        return HttpResponseRedirect(__base_url+"/?create_agreement_api_data"+json.dumps(__create_agreement_api_response))


def __execute_agreement(response): 
    global __query_agreement_url, __execute_agreement_url, __id_token, __app_key, __timeout_sec, __agreement_creation_request_id, __agreement_ID, __agreement_status, __tokenized_payer_ref, __price
   
    # need to check lines 474-480 
    # __current_url = response.get_full_path()
    # if 'cancel' in __current_url:
    #     if __agreement_ID == None:
    #         print('inside tokenized_result cancel')
    #         return HttpResponseRedirect(__base_url)
    #     else:
    #         return HttpResponseRedirect(__base_url+"/tokenized_homepage/")
    
    __token()

    print('in tokenized result')
    print('agreement creation request id =', __agreement_creation_request_id)

    #Execute agreement api
    __execute_agreement_head = {
    'Accept':'application/json',
    'Authorization': __id_token,
    'X-App-Key': __app_key
    }

    __execute_agreement_body = {
        'paymentID': __agreement_creation_request_id
    }

    # __execute_agreement_url=f'{__base_url}/tokenized/checkout/execute'
    # __execute_agreement_url='https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute'

    try:
        __execute_agreement_api_response=(requests.post(__execute_agreement_url, headers=__execute_agreement_head, json=__execute_agreement_body, timeout=__timeout_sec)).json()
    # execute_agreement_api_response = None
    except requests.exceptions.Timeout:
    # if execute_agreement_api_response == None:
        # __query_agreement_url=f'{__base_url}/tokenized/checkout/agreement/status'  
        # __query_agreement_url='https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/agreement/status'

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
            print('inside except')
            return HttpResponseRedirect(__base_url+"/?execute_agreement_api_data="+json.dumps({'message':'execute agreement api timeout'}))
        
        debugging_print(__query_payment_api_response, 'Query response api =')

        # query_payment_api_response['status'] = 'initiated' or 'success'
        if __query_payment_api_response.get('status') == 'initiated':
            return HttpResponseRedirect(f'{__base_url}/checkout/')   #if initiated call create payment api
        elif len(__query_payment_api_response) == 2:
            return HttpResponseRedirect(__base_url+"/?execute_agreement_api_data="+json.dumps(__execute_agreement_api_response))
        else:
            __execute_agreement_api_response = __query_payment_api_response
    
    __agreement_ID=__execute_agreement_api_response.get('agreementID')
    __agreement_status=__execute_agreement_api_response.get('agreementStatus')
    __tokenized_payer_ref=__execute_agreement_api_response.get('payerReference')

    debugging_print(__execute_agreement_api_response, 'execute agreement api =')
    
    # return HttpResponseRedirect(__base_url+"/?pgw=agreement&statusCode="+__execute_agreement_api_response.get("statusCode")+'&statusMessage='+__execute_agreement_api_response.get("statusMessage"))
    return HttpResponseRedirect(__base_url+"/?execute_agreement_api_data="+json.dumps(__execute_agreement_api_response))
    # return JsonResponse(__execute_agreement_api_response)

def cancel_agreement(request):
    global __cancel_agreement_url, __agreement_ID, __agreement_status, __token_approved

    __token()
    
    print('in cancel')

    #Cancle Agreement payment api
    __cancel_agreement_head = {
    'Content-Type':"application/json",
    'Accept':'application/json',
    'Authorization': __id_token,
    'X-App-Key': __app_key
    }

    __cancel_agreement_body = {
        'agreementID': __agreement_ID
    }

    # __cancel_agreement_url = f'{__base_url}/tokenized/checkout/agreement/cancel'
    # __cancel_agreement_url = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/agreement/cancel'
    
    print('calling cancel agreement api')
    try:
        __cancel_agreement_api_response = (requests.post(__cancel_agreement_url, headers=__cancel_agreement_head, json=__cancel_agreement_body, timeout=__timeout_sec)).json()
        print('cancel agreement =', __cancel_agreement_api_response)
    except requests.exceptions.Timeout:
        return HttpResponseRedirect(__base_url+"/?cancel_agreement_api_data="+json.dumps({'message':'cancel ageement api timeout'}))
    
    if (__cancel_agreement_api_response.get('statusCode') == '0000'):
        print('cancel agreement success')
        __agreement_ID = None
        __agreement_status = None
        __token_approved = False
        return HttpResponseRedirect(__base_url+"/?cancel_agreement_api_data="+json.dumps(__cancel_agreement_api_response))
    else:
        print('cancel_agreement error')
        return HttpResponseRedirect(__base_url+"/?cancel_agreement_api_data="+json.dumps(__cancel_agreement_api_response))
