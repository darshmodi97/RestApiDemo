from django.urls import path
from account import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path("users/", views.All_Users.as_view(), name="users"),
    path('user-detail/<pk>', views.ShowProfile.as_view(), name='show_profile'),
    path('update/', views.UpdateProfile.as_view(), name='update_profile'),
    path('delete/', views.DeleteAccount.as_view(), name='delete_profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
