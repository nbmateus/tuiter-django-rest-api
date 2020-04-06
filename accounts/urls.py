from django.urls import path, include
from allauth.account.views import ConfirmEmailView, PasswordResetDoneView
from rest_auth.views import PasswordResetConfirmView
from rest_auth.registration.views import VerifyEmailView
from .views import  (
    userProfileView, profileFollowerListView, profileFollowingListView, registrationCompleteView, doFollowOrUnfollowView, updateProfile
)

urlpatterns = [
    path('password/reset/confirm/complete/', PasswordResetDoneView.as_view(), name='password_reset_complete'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('registration/account-email-verification-sent/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('registration/', include('rest_auth.registration.urls')),
    path('registration/complete/', registrationCompleteView, name='account_confirm_complete'),
    path('', include('rest_auth.urls')),
    path('profile/<str:username>/', userProfileView, name='profile_detail'),
    path('profile/<str:username>/followers/', profileFollowerListView, name='profile_follower_list'),
    path('profile/<str:username>/following/', profileFollowingListView, name='profile_following_list'),
    path('profile/<str:username>/follow-or-unfollow/', doFollowOrUnfollowView, name='follow_or_unfollow'),
    path('profile/<str:username>/update/', updateProfile, name='profile_update'),

    
    
]