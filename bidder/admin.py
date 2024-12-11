from django.contrib import admin
from .models import Item, Bid, Transaction, Rating, Profile, Complaint, Application, Comment
from django.contrib.auth.models import Group
from django.contrib.auth import  get_user_model


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'is_approved', "anti_bot_answer")
    actions = ["approve_user"]

    def approve_user(self, request, queryset):
        # first we loop through all the applications
        for application in queryset:
            # then we check of the application is good by first checking the answer
            if int(application.anti_bot_answer) == 19:

                # if the answer is correct, create a user and save it
                new_user = get_user_model().objects.create_user(
                    username=application.username,
                    password=application.password,
                )

                new_user.save()
                # after the application has been approved, delete the application
                application.delete()


    approve_user.short_description = "Create approved users"


admin.site.register(Comment)
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Transaction)
admin.site.register(Rating)
admin.site.register(Complaint)
admin.site.register(Application, ApplicationAdmin)