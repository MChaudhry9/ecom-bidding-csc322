from django.contrib import admin
from .models import Item, Bid, Transaction, Rating, Profile, Complaint, Application, Comment, VipItem, Guess
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


class VipItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'guess_range_min', 'guess_range_max')
    actions = ['process_vip_item']

    def process_vip_item(self, request, queryset):
        for vip_item in queryset:
            guesses = vip_item.guesses.all()

            if not guesses.exists():
                self.message_user(request, f"No guesses found for {vip_item}.", level='warning')
                continue

            # Find the closest guess
            closest_guess = min(guesses, key=lambda g: abs(vip_item.price - g.guessed_amount))

            # Update the account balance of the closest guesser's profile
            profile = closest_guess.guesser.profile
            profile.account_balance += vip_item.price
            profile.save()

            guesses.delete()

            # Delete the VipItem itself
            vip_item.delete()

    process_vip_item.short_description = "Process selected VIP items and delete them"

admin.site.register(Comment)
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Transaction)
admin.site.register(Rating)
admin.site.register(Complaint)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(VipItem, VipItemAdmin)
admin.site.register(Guess)