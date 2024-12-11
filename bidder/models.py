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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"




class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    is_available = models.BooleanField(default=True)  # False once sold/rented
    display_image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    associated_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.amount} on {self.item.name}"

class Transaction(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)  # Each item can only have one transaction
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} bought {self.item.name} from {self.seller.username}"

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_ratings")
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_ratings")
    score = models.IntegerField()  # 1 (worst) to 5 (best)
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



