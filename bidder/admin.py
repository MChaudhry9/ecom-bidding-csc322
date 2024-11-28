from django.contrib import admin
from .models import Item, Bid, Transaction, Rating, Profile, Complaint, Application
from django.contrib.auth.models import Group

admin.site.unregister(Group)


admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Transaction)
admin.site.register(Rating)
admin.site.register(Complaint)
admin.site.register(Application)