from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path("login/", auth_views.LoginView.as_view(template_name="bidder/login.html"), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(template_name="bidder/logout_confirmation.html"), name="logout"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('logoutconfirm/', views.logout_confirmation, name="logout-confirmation"),
    path("browse/", views.browse_items, name="browse_items"),
    path("apply/", views.apply_to_become_user, name="apply_to_become_user"),

    # User views
    path("dashboard/", views.dashboard, name="dashboard"),
    path("items/list/", views.list_item, name="list_item"),
    path("items/<int:item_id>/bid/", views.place_bid, name="place_bid"),
    path("deposit/", views.deposit_money, name="deposit_money"),
    path("withdraw/", views.withdraw_money, name="withdraw_money"),
    path("rate/<int:user_id>/", views.rate_user, name="rate_user"),
    path("file_complaint/", views.file_complaint, name="file_complaint"),
    path('handle_complaints/', views.handle_complaints, name='handle_complaints'),
    path("resolve_complaint/<int:complaint_id>/", views.resolve_complaint, name="resolve_complaint"),
    path("register/", views.register_user, name="register_user"),
    path('vip/', views.vip, name='vip'),
    path("list-request/", views.list_request, name="list_request"),
    path('browse-requests/', views.browse_requests, name='browse_requests'),
    path('users-own-listed-items/', views.users_own_listed_items, name='users_own_listed_items'),
    path("suspended/", views.suspended, name='suspended'),

]