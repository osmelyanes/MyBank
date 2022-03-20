import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyBank.settings")

import django

django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

from MyBank.settings import SOCIALACCOUNT_PROVIDERS

if __name__ == "__main__":
    try:
        site = Site.objects.get(id=1)
        site.domain = '127.0.0.1:8001'
        site.name = '127.0.0.1:8001'
        site.save()

        social_app, created = SocialApp.objects.get_or_create(id=1,
                                                              provider='google',
                                                              name='OAuth',
                                                              client_id=SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
                                                              secret=SOCIALACCOUNT_PROVIDERS['google']['APP']['secret'],
                                                              key='')
        social_app.sites.add(site)
        print('Succeed configuring OAuth.')

    except Exception as e:
        print('Failure configuring OAuth.')
        raise (repr(e))
