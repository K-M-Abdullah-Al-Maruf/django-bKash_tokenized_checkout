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

    path("``preferred_url/``", django_bKash_tokenized_checkout.views.create_payment), ``for non-agreement based checkout url``

and,
    path("``preferred_url/``", django_bKash_tokenized_checkout.views.create_agreement), ``to create an agreement``
