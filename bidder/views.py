from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from pandas.io.clipboard import is_available

from .models import Item, Bid, Transaction, Profile, Complaint, Rating, Application, Comment, ItemRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Q




def home_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Redirect to the suspended page if the user is suspended
        if request.user.profile.is_suspended:
            return redirect('suspended')

    # Logic for anonymous or authenticated users
    return render(request, "bidder/home.html")


# Visitor Views
def browse_items(request):
    """
    View to display all available items to visitors.
    """
    if request.user.is_authenticated:
        # Redirect suspended users to the suspended page
        if request.user.profile.is_suspended:
            return render(request, "bidder/suspended.html")

    # Fetch available items
    items = Item.objects.filter(is_available=True)
    return render(request, "bidder/browse_items.html", {"items": items})




# to render vip page
def vip(request):
    return render(request, 'bidder/vip.html')


def apply_to_become_user(request):
    """
    View for visitors to apply to become registered users.
    """
    if request.user.is_authenticated:
        if request.user.profile.is_suspended:
            return redirect("suspended")

    if request.method == "POST":
        anti_bot_answer = request.POST.get("anti_bot_answer")
        username = request.POST.get("username")
        password = request.POST.get("password")
        new_application = Application(
            anti_bot_answer=anti_bot_answer, username=username, password=password
        )
        new_application.save()
        messages.success(request, "Application submitted successfully. Please wait for approval.")
        return redirect("browse_items")
    else:
        return render(request, "bidder/apply_to_become_user.html")



# User Views
@login_required
def list_item(request):
    """View for users to list items for sale or rent."""
    if request.user.profile.is_suspended:
        return redirect('suspended')
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        starting_price = request.POST.get("starting_price")
        deadline = request.POST.get("deadline")
        display_image = request.FILES.get("display_image")
        item = Item.objects.create(
            owner=request.user,
            name=name,
            description=description,
            starting_price=starting_price,
            deadline=deadline,
            display_image=display_image,
        )
        item.save()
        messages.success(request, "Item listed successfully!")
        return redirect("browse_items")
    return render(request, "bidder/list_item.html")


@login_required
def place_bid(request, item_id):
    if request.user.profile.is_suspended:
        return redirect('suspended')
    """View for users to place bids on an item."""
    item = get_object_or_404(Item, id=item_id)
    comments = Comment.objects.filter(associated_item=item)

    if request.method == "POST":

        if request.POST.get("post_type", "n/a") == "comment":

            new_comment_content = request.POST.get("comment")
            new_comment = Comment(content=new_comment_content, associated_item=item)
            new_comment.save()
            return render(request, "bidder/place_bid.html", {"item": item, "comments": comments})
        else:

            amount = float(request.POST.get("amount"))
            current_highest_bid = max([bid.amount for bid in item.bids.all()], default=item.starting_price)

            if amount > current_highest_bid:

                if request.user.profile.account_balance >= amount:
                    new_bid = Bid.objects.create(item=item, bidder=request.user, amount=amount)
                    new_bid.save()
                    item.current_max_bid = amount
                    item.save()

                    messages.success(request, "Bid placed successfully!")
                else:
                    messages.error(request, "Insufficient balance.")
            else:
                messages.error(request, "Bid amount must be higher than the current bid.")
        return redirect("browse_items")
    return render(request, "bidder/place_bid.html", {"item": item, "comments": comments})

@login_required
def deposit_money(request):
    if request.method == "POST":
        amount = Decimal(request.POST.get("amount", "0"))  # Convert amount to Decimal
        if amount > 0:
            profile = request.user.profile
            profile.account_balance += amount  # This should now work correctly
            profile.save()
            messages.success(request, "Deposit successful!")
        else:
            messages.error(request, "Please enter a valid amount.")
    return render(request, "bidder/deposit_money.html")


@login_required
def withdraw_money(request):
    """View to handle withdrawing money from a user's account."""
    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))  # Convert to Decimal
        if amount <= 0:
            messages.error(request, "Amount must be greater than 0.")
            return redirect("withdraw_money")

        profile = request.user.profile
        if profile.account_balance >= amount:
            profile.account_balance -= amount  # Safe subtraction
            profile.save()
            messages.success(request, f"${amount} successfully withdrawn.")
        else:
            messages.error(request, "Insufficient balance.")
        return redirect("withdraw_money")

    return render(request, "bidder/withdraw_money.html")

@login_required
def rate_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # get the user making this request
    rater = request.user

    if request.method == "POST":
        rating = request.POST.get("rating")
        if rating:
            # if the user making this request is the buyer, they want to rate the seller
            if rater == transaction.buyer:

                transaction.seller_rating = int(rating)  # Assuming 'rating' is a field in the Item model
                transaction.rated_by_buyer = True
                transaction.save()

            # if the user making the request is the seller, they want to rate the buyer
            else:
                transaction.buyer_rating = int(rating)
                transaction.rated_by_seller = True
                transaction.save()

            messages.success(request, "Thank you for rating this item!")
        else:
            messages.error(request, "Please provide a valid rating.")

    return redirect("dashboard")


@login_required
def file_complaint(request):
    """
    Allow users to file complaints against another user by specifying their username.
    """
    if request.user.profile.is_suspended:
        return render(request, "bidder/suspended.html")
    if request.method == "POST":
        accused_username = request.POST.get("accused_user")  # Get username from form input
        description = request.POST.get("description")  # Get description from form input

        # Validate and fetch the accused user
        try:
            accused_user = User.objects.get(username=accused_username)
        except User.DoesNotExist:
            messages.error(request, "The specified user does not exist.")
            return redirect("file_complaint")

        # Create the complaint
        Complaint.objects.create(
            complainant=request.user,
            against_user=accused_user,
            description=description,
        )
        messages.success(request, "Complaint filed successfully.")
        return redirect("browse_items")

    # Render the complaint form
    return render(request, "bidder/file_complaint.html")



# Super User Views
@staff_member_required
def approve_application(request, application_id):
    """Approve an application for a visitor to become a user."""
    application = get_object_or_404(Application, id=application_id)
    application.is_approved = True
    application.save()
    # messages.success(request, f"Application for {application.applicant.username} approved!")
    return redirect("application_list")

@staff_member_required
def handle_complaints(request):
    """View for Super Users to see and resolve complaints."""
    complaints = Complaint.objects.filter(resolved=False)
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.resolved = True
        complaint.save()
        messages.success(request, "Complaint resolved successfully.")
        return redirect("handle_complaints")
    return render(request, "bidder/handle_complaints.html", {"complaints": complaints})

@staff_member_required
def resolve_complaint(request, complaint_id):
    """Resolve a specific complaint."""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()  # Delete the complaint once resolved
    messages.success(request, "Complaint resolved successfully.")
    return redirect("handle_complaints")

def register_user(request):
    """View for user registration."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")  # Redirect to the login page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, "bidder/register.html", {"form": form})


def logout_confirmation(request):
    return render(request, "bidder/logout_confirmation.html")


@login_required
def dashboard(request):
    if request.user.profile.is_suspended:
        return redirect('suspended')

    user = request.user
    profile = user.profile

    # Fetch account-related details
    account_balance = profile.account_balance
    is_vip = profile.is_vip
    user_status = "VIP" if is_vip else "Regular User"

    # Fetch user's items, bids, transactions, and complaints
    items = Item.objects.filter(owner=user)
    bids = Bid.objects.filter(bidder=user)
    transactions = Transaction.objects.filter(buyer=user) | Transaction.objects.filter(seller=user)
    ratings_total = 0
    ratings_count = 0

    for transaction in transactions:
        if transaction.buyer == user and transaction.rated_by_seller == True:
            ratings_count += 1
            ratings_total = ratings_total + transaction.buyer_rating
        elif transaction.seller == user and transaction.rated_by_buyer == True:
            ratings_count += 1
            ratings_total = ratings_total + transaction.seller_rating


    average_rating = ratings_total/ratings_count



    # received_ratings = Transaction.objects.filter((Q(seller=user) | Q(buyer=user)) & Q(rating__isnull=False))
    # given_ratings = Transaction.objects.filter((Q(buyer=user) | Q(seller=user)) & Q(rating__isnull=False))



    complaints = Complaint.objects.filter(complainant=user)

    # rated_transactions = transactions.filter(buyer=user, item__has_rating=True)

    # Prepare unrated transactions (only for buyer's perspective)
    unrated_transactions = transactions.filter(buyer=user, rated_by_buyer=False) | transactions.filter(seller=user, rated_by_seller=False)
    # unrated_transactions = transactions.filter(
    #     Q(buyer=user, rated_by_buyer=False) |
    #     Q(seller=user, rated_by_seller=False)
    # )
    # Update VIP status based on transactions and complaints
    profile.transactions_count = transactions.count()
    profile.complaints_count = complaints.count()
    profile.save()

    context = {
        "user": user,
        "account_balance": account_balance,
        "user_status": user_status,
        "items": items,
        "bids": bids,
        "transactions": transactions,
        "complaints": complaints,
        "unrated_transactions": unrated_transactions,  # Pass unrated transactions
        "average_rating": average_rating,
        # "rated_transactions": rated_transactions,
        # "received_ratings": received_ratings,
        # "given_ratings": given_ratings,
    }

    return render(request, "bidder/dashboard.html", context)






@login_required
def list_request(request):
    if request.user.profile.is_suspended:
        return redirect('suspended')
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        description = request.POST.get("description")
        price_min = request.POST.get("price_min")
        price_max = request.POST.get("price_max")

        if not item_name or not price_min or not price_max:
            messages.error(request, "Please fill in all required fields.")
            return render(request, "bidder/list_request.html")

        if float(price_min) > float(price_max):
            messages.error(request, "Minimum price cannot be greater than maximum price.")
            return render(request, "bidder/list_request.html")

        # Save the request
        ItemRequest.objects.create(
            user=request.user,
            item_name=item_name,
            description=description,
            price_min=price_min,
            price_max=price_max
        )
        messages.success(request, "Your request has been listed successfully!")
        return redirect("browse_requests")  # Redirect to a page to browse all requests (optional)

    return render(request, "bidder/list_request.html")


@login_required
def browse_requests(request):
    if request.user.profile.is_suspended:
        return redirect('suspended')
    requests = ItemRequest.objects.all().order_by("-created_at")
    return render(request, "bidder/browse_requests.html", {"requests": requests})


@login_required
def users_own_listed_items(request):
    # Redirect if user is suspended
    if request.user.profile.is_suspended:
        return redirect('suspended')

    if request.method == "POST":
        bid_id = request.POST.get("bid_id")
        bid = get_object_or_404(Bid, id=bid_id)
        item = bid.item
        owner = bid.item.owner
        bidder = bid.bidder

        # Ensure the bidder has sufficient balance
        if bidder.profile.account_balance >= bid.amount:
            # Deduct amount from bidder based on VIP status
            if bidder.profile.is_vip:
                final_amount = bid.amount * 0.9  # 10% discount
            else:
                final_amount = bid.amount

            # Deduct the amount from the bidder's account
            bidder.profile.account_balance -= final_amount

            # Add the amount to the owner's account
            owner.profile.account_balance += final_amount

            # Mark the item as sold/rented
            item.is_available = False

            # Save the updates
            item.save()
            owner.profile.save()
            bidder.profile.save()

            # Create transactions for both buyer and seller
            Transaction.objects.create(
                buyer=bidder,
                seller=owner,
                item=item,
                amount=final_amount,
                completed_at=datetime.now()
            )

    # Prepare the data for rendering
    logged_in_user = request.user
    all_items = Item.objects.filter(owner=logged_in_user, is_available=True)
    all_items_with_details = []
    for item in all_items:
        all_bids = Bid.objects.filter(item=item)
        all_items_with_details.append({
            "name": item.name,
            "starting_price": item.starting_price,
            "display_image_url": item.display_image.url,
            "bids": all_bids,
        })

    return render(request, "bidder/users_own_listed_items.html", context={"all_items_with_details": all_items_with_details})



def suspended(request):
    suspended_user = request.user
    if request.method == "POST":
        if suspended_user.profile.account_balance > 50:
            suspended_user.profile.account_balance -= 50
            suspended_user.profile.is_suspended = False
            suspended_user.profile.save()

            # restore thier review 5 so they can start fresh
            transactions = Transaction.objects.filter(buyer=suspended_user, seller=suspended_user)
            for transaction in transactions:
                if transaction.buyer == suspended_user:
                    transaction.buyer_rating = 5
                elif transaction.seller == suspended_user:
                    transaction.seller_rating = 5
            return redirect("browse_items")
    return render(request, "bidder/suspended.html")

