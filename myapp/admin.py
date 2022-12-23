from django.contrib import admin
from myapp.models import client
from myapp.models import APP_LINK
from myapp.models import EXCHANGE
from myapp.models import HISTORY
from myapp.models import EXCHANGE_ITEM
# Register your models here.
admin.site.register(client)
admin.site.register(APP_LINK)
admin.site.register(EXCHANGE)
admin.site.register(HISTORY)
admin.site.register(EXCHANGE_ITEM)
