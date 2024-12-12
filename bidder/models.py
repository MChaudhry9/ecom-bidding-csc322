from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    is_available = models.BooleanField(default=True)  # False once sold/rented
    display_image = models.ImageField(upload_to="images/", null=True, blank=True)
    current_max_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.PositiveIntegerField(null=True, blank=True)  # Rating value (1-5)
    has_rating = models.BooleanField(default=False)  # To check if already rated

    def __str__(self):
        return self.name


class Transaction(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)  # Each item can only have one transaction
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    completed_at = models.DateTimeField(auto_now_add=True)
    seller_rating = models.PositiveIntegerField(null=True, blank=True) # Allow null if no rating yet
    buyer_rating = models.PositiveIntegerField(null=True, blank=True)
    rated_by_seller = models.BooleanField(default=False)
    rated_by_buyer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buyer.username} bought {self.item.name} from {self.seller.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_vip = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    times_suspended = models.IntegerField(default=0)
    is_forced_out = models.BooleanField(default=False) 
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # overwrite the default save method
    def save(self, *args, **kwargs):
        profile_transactions_as_buyer = Transaction.objects.filter(buyer=self.user)
        profile_transactions_as_seller = Transaction.objects.filter(seller=self.user)
        all_transactions_count = len(profile_transactions_as_buyer) + len(profile_transactions_as_seller)
        all_complaints_count = len(Complaint.objects.filter(against_user=self.user))

        # Calculate average rating
        ratings = Rating.objects.filter(rated_user=self.user)
        self.average_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0

        # calculate average rating
        # get all transactions associated with user
        transactions = Transaction.objects.filter(buyer=self.user) | Transaction.objects.filter(seller=self.user)
        ratings_gotten_total = 0
        ratings_gotten_count = 0
        ratings_given_count = 0
        ratings_given_total = 0

        # loop through them and find the users average rating
        print(transactions)
        for transaction in transactions:
            if transaction.buyer == self.user:
                if transaction.rated_by_seller:
                    ratings_gotten_count += 1
                    # print(3)
                    ratings_gotten_total += transaction.buyer_rating
                if transaction.rated_by_buyer:
                    ratings_given_count += 1
                    ratings_given_total += transaction.seller_rating
                    # print(33)

            elif transaction.seller == self.user:
                if transaction.rated_by_seller:
                    # print(34554)
                    ratings_given_count += 1
                    ratings_given_total += transaction.buyer_rating
                if transaction.rated_by_buyer:
                    # print(344444)
                    ratings_gotten_count += 1
                    ratings_gotten_total += transaction.seller_rating

        average_gotten_ratings = 0
        average_given_ratings = 0
        if ratings_gotten_count > 0:
            average_gotten_ratings = ratings_gotten_total / ratings_gotten_count
        if ratings_given_count > 0:
            average_given_ratings = ratings_given_total / ratings_given_count
        # if their rating is less 2 and have more than 3 ratings, then they will be suspended
        # also if they are too mean or too generous, they are suspended
        # print(average_given_ratings, ratings_given_count)
        # if (average_gotten_ratings < 2 and ratings_gotten_count > 3):
        #     print("ll")
        # if ((ratings_given_count >= 3) and
        #         (not (2 <= average_given_ratings <= 4))):
        #     print("pppp")
        if (average_gotten_ratings < 2 and ratings_gotten_count > 3) or ((ratings_given_count >= 3) and
                (not (2 <= average_given_ratings <= 4))):

            self.is_suspended = True



        #  if user has 5000+, and more than 5 transactions and no complaints, save them as a vip

        if self.account_balance > 5000.00 and all_transactions_count >= 5 and all_complaints_count == 0:
            self.is_vip = True
        #     if the user doesn't meet these requirements, or he broke the last two, remove them from vip status
        else:
            self.is_vip = False

        # if user is a vip user, trying to suspend hime will simply remove their vip status
        if self.is_vip and self.is_suspended:
            self.is_suspended = False
            self.is_vip = False

        # if after all the processes, the user is deemed as suspended, increment suspension count
        if self.is_suspended:
            self.times_suspended = 1 + self.times_suspended

        # if total suspension count reaches 3, delete the users profile
        if self.times_suspended == 3:
            self.delete()

        super().save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    associated_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    was_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bidder.username} - {self.amount} on {self.item.name}"


class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_ratings")
    score = models.IntegerField() # 1 (worst) to 5 (best)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater.username} rated {self.rated_user.username}: {self.score}"

class Complaint(models.Model):
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complaints")
    against_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accused")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Complaint by {self.complainant.username} against {self.against_user.username}"


class Application(models.Model):
    anti_bot_answer = models.CharField(max_length=255)  # To store the answer to the anti-bot question
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)




class ItemRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2)
    price_max = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} requests {self.item_name} (${self.price_min} - ${self.price_max})"


class VipItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    guess_range_min = models.IntegerField()
    guess_range_max = models.IntegerField()
    display_image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f"VipItem priced at {self.price}"

class Guess(models.Model):
    guesser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guesses")
    vip_item = models.ForeignKey(VipItem, on_delete=models.CASCADE, related_name="guesses")
    guessed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    closeness = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Guess by {self.guesser} for name '{self.vip_item.name}' with guessed amount {self.guessed_amount}"