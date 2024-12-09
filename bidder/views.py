from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Item, Bid, Transaction, Profile, Complaint, Rating, Application
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.db.models import Q


def home_view(request):
    return render(request, "bidder/home.html")

# Visitor Views
def browse_items(request):
    """View to display all available items to visitors."""
    items = Item.objects.filter(is_available=True)
    return render(request, "bidder/browse_items.html", {"items": items})



# to render vip page
def vip(request):
    return render(request, 'bidder/vip.html')


@login_required
def apply_to_become_user(request):
    """View for visitors to apply to become registered users."""
    if request.method == "POST":
        answer = request.POST.get("anti_bot_answer")
        if answer:  # Validate the answer to the anti-bot question
            Application.objects.create(applicant=request.user, anti_bot_answer=answer)
            messages.success(request, "Application submitted successfully. Please wait for approval.")
            return redirect("browse_items")
        else:
            messages.error(request, "Please answer the anti-bot question.")
    return render(request, "bidder/apply_to_become_user.html")


# User Views
@login_required
def list_item(request):
    """View for users to list items for sale or rent."""
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        starting_price = request.POST.get("starting_price")
        deadline = request.POST.get("deadline")
        item = Item.objects.create(
            owner=request.user,
            name=name,
            description=description,
            starting_price=starting_price,
            deadline=deadline,
        )
        messages.success(request, "Item listed successfully!")
        return redirect("browse_items")
    return render(request, "bidder/list_item.html")


@login_required
def place_bid(request, item_id):
    """View for users to place bids on an item."""
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        current_highest_bid = max([bid.amount for bid in item.bids.all()], default=item.starting_price)
        if amount > current_highest_bid:
            if request.user.profile.account_balance >= amount:
                Bid.objects.create(item=item, bidder=request.user, amount=amount)
                messages.success(request, "Bid placed successfully!")
            else:
                messages.error(request, "Insufficient balance.")
        else:
            messages.error(request, "Bid amount must be higher than the current bid.")
        return redirect("browse_items")
    return render(request, "bidder/place_bid.html", {"item": item})

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
def rate_user(request, user_id):
    """Allow users to rate another user after a transaction."""
    rated_user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        score = int(request.POST.get("score"))
        comment = request.POST.get("comment", "")
        Rating.objects.create(rater=request.user, rated_user=rated_user, score=score, comment=comment)
        messages.success(request, "Rating submitted successfully.")
        return redirect("browse_items")
    return render(request, "bidder/rate_user.html", {"rated_user": rated_user})

@login_required
def file_complaint(request):
    """
    Allow users to file complaints against another user by specifying their username.
    """
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
    messages.success(request, f"Application for {application.applicant.username} approved!")
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
    user = request.user
    account_balance = user.profile.account_balance
    is_vip = user.profile.is_vip
    user_status = "VIP" if is_vip else "Regular User"  # Handle logic here

    # Fetch additional data for the dashboard
    items = Item.objects.filter(owner=user)
    bids = Bid.objects.filter(bidder=user)
    transactions = Transaction.objects.filter(buyer=user) | Transaction.objects.filter(seller=user)
    complaints = Complaint.objects.filter(complainant=user)

    context = {
        "user": user,
        "account_balance": account_balance,
        "user_status": user_status,  # Pass status here
        "items": items,
        "bids": bids,
        "transactions": transactions,
        "complaints": complaints,
    }

    return render(request, "bidder/dashboard.html", context)
