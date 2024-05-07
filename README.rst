===============================
django_bKash_tokenized_checkout
===============================

django-polls is a Django app to conduct web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_bKash_tokenized_checkout" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = [
            ...,
            "django_bKash_tokenized_checkout",
        ]

2. Include the polls URLconf in your project urls.py like this to create payment for both agreement and non-agreement based checkout url::

        path("django_bKash_tokenized_checkout/",include("django_bKash_tokenized_checkout.urls"))


Implementation
--------------

D-jango - bKash_tokenized_checkout

1) Download the package from the “dist” folder in the github repository. File will be named as or similar to:
	
    django_bkash_tokenized_checkout-version.tar.gz
	
    For example:
	django_bkash_tokenized_checkout-0.1.tar.gz

2) Run the following command in terminal:

        python -m pip install --user location/path of the package

    Note: do not keep the location/path of the package inside quotation marks.

3) During package installation if faced with the error “User site-packages are not visible in this virtualenv.” then to solve it:
    i) Go to the `pyvenv.cfg` file in the Virtual environment folder.
   ii) Set the `include-system-site-packages` to `true` and save the change.
  iii) Reactivate the virtual environment.

4) After successful installation go to “settings.py” and include the app in the installed app using:

        'django_bKash_tokenized_checkout.apps.bKash_tokenized_checkoutConfig'

5) Go to “__init__.py” and import the package's views using:
	
        from django_bKash_tokenized_checkout import views as package_view


6) Using the set methods of the package's views provide the following credentials in the “__init__.py” file.

    i) For non-agreement based checkout url:

        package_view.set_base_url("")
        package_view.set_app_key("")
        package_view.set_app_secret_key("")
        package_view.set_username("")
        package_view.set_password("")
        package_view.set_grant_token_api("")
        package_view.set_refresh_token_api("")
        package_view.set_non_tokenized_create_payment_api("")
        package_view.set_execute_payment_api("")
        package_view.set_query_payment_api("")

   ii) For agreement based checkout url:

        package_view.set_base_url("")
        package_view.set_app_key("")
        package_view.set_app_secret_key("")
        package_view.set_username("")
        package_view.set_password("")
        package_view.set_grant_token_api("")
        package_view.set_refresh_token_api("")
        package_view.set_tokenized_create_payment_api("")
        package_view.set_execute_payment_api("")
        package_view.set_query_payment_api("")
        package_view.set_create_agreement_api("")
        package_view.set_execute_agreement_api("")
        package_view.set_cancel_agreement_api("”)

7) Similarly you can also use get methods for all the set methods to retrieve the corresponding data. Similar to the set methods.

8) Now go to “url.py” and point to the new module name:
        
        urlpatterns = [
        .. .. .. .. .. .. .. .. .. ..
        path("django_bKash_tokenized_checkout/",include("django_bKash_tokenized_checkout.urls"))
        ]

9) In order to complete payment, use the following url to redirect and send the amount to pay with the variable named "total_amount” during POST request.
        “base_url/path or page if any/ django_bKash_tokenized_checkout/create_payment/”

10) In order to create agreement, use the following url to redirect
        “base_url/path or page if any/ django_bKash_tokenized_checkout/create_agreement/”

11) In order to cancel agreement, use the following url to redirect
        “base_url/path or page if any/ django_bKash_tokenized_checkout/cancel_agreement/”

12) All the APIs will return data in json format. The data are unchanged responses received from bKash's end.
All data will be sent from the backend with the 'API's name' followed by an '='.
	
    For example:
        http://127.0.0.1:8000/?execute_agreement_api_data=%7B%22statusCode%22:%20%222054%22,%20%22statusMessage%22:%20%22Agreement%20execution%20pre-requisite%20hasn%27t%20been%20met%22%7D

        Here in the frontend to catch the json u need to use the variable name “execute_agreement_api_data” and get the json and handle it accordingly.

    Another example:
        http://127.0.0.1:8000/tokenized_homepage/?agreement_creation_data=execute_agreement_api_data={"paymentID"%3A+"TR0000qGwKk6R1715008446097"%2C+"agreementID"%3A+"TokenizedMerchant0219SNPXK1715008466051"%2C+"agreementStatus"%3A+"Completed"%2C+"agreementExecuteTime"%3A+"2024-05-06T21%3A14%3A26%3A051+GMT+0600"%2C+"payerReference"%3A+"01619777283"%2C+"customerMsisdn"%3A+"01619777283"%2C+"statusCode"%3A+"0000"%2C+"statusMessage"%3A+"Successful"}

        Here in the frontend to catch the json u need to use the variable name “execute_agreement_api_data” and get the json and handle it accordingly.

13) Here is a list of used API and variable name with which they will send the json data:


          API -------> Json response variable name  -------> Reason(s)             
   i) Grant token API  ------->  grant_token_api_data  ------->  If case of any errors
  ii) Refresh token API  ------->  refresh_token_api_data   ------->  If case of any errors
 iii)Create payment API (agreement based checkout)  ------->  tokenized_create_payment_api_data  ------->  bKash's API response and in case of any errors                                                                                                                         
  iv) Create payment API (non-agreement based checkout) ------->  non_tokenized_create_payment_api_data -------> bKash's API response and in case of any errors                                                                                               
   v) Execute payment API  ------->  execute_payment_api_data  ------->| bKash's API response and in case of any errors                                                                                                 
  vi) Create Agreement API   -------> create_agreement_api_data   -------> bKash's API response and in case of any errors                                                                                              
 vii) Execute Agreement API   ------->  execute_agreement_api_data -------> bKash's API response and in case of any errors                                                                                                       
viii) Cancel Agreement API   ------->  cancel_agreement_api_data   -------> bKash's API response and in case of any errors                                                                                   


