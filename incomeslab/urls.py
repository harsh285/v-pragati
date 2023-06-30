from django.urls import path, include
from incomeslab import views

app_name = 'incomeslab'

urlpatterns = [
    path('', views.Dashboard.as_view(), name="home"),
    path('generate_id_pin/', views.GenerateIDPin.as_view(), name="generateIDPin"),
    path('generate_id_pin/<pk_pin_id>/', views.GenerateIDPinDetail.as_view(), name="generateIDPinDetail"),
    path('sponser_income/', views.ReferralDetail.as_view(), name="referralDetail"),
    path('add_referral/', views.AddReferralCode.as_view(), name="addReferralCode"),
]
