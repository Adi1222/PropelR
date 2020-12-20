from django.urls import path, include

from PropelRapp import apiViews
from . import views, apiViews

urlpatterns = [
    path('', views.login_request, name='login'),

    path('register/', views.register, name='register'),

    path('Dashboard/', views.dashboard, name='dashboard'),




#************************************API DATA URLS******************************************

    path('Dashboard/Visitors/', apiViews.get_visitors_data, name='get_visitors_data'),

    path('Dashboard/Vehicles/', apiViews.get_vehicles_data, name='get_vehicles_data'),

    path('Dashboard/Age/', apiViews.get_age_data, name='get_age_data'),

    path('Dashboard/Gender/', apiViews.get_gender_data, name='get_gender_data'),

    path('Dashboard/Repeat-Visitors/', apiViews.get_repeat_visitors_data, name='get_repeat_visitors_data'),

    path('Dashboard/Repeat-Vehicles/', apiViews.get_repeat_vehicles_data, name='get_repeat_vehicles_data'),

    path('Dashboard/Camera-Tampering/', apiViews.get_camera_tampering_data, name='get_camera_tampering_data'),





    path('Dashboard/Visitors-Count/Details/', views.visitor_details_dashboard, name='visitor_details_dashboard'),

    path('Dashboard/Vehicle-Count/Details/', views.vehicle_details_dashboard, name='vehicle_details_dashboard'),

    path('Dashboard/Age/Details/', views.age_details_dashboard, name='age_details_dashboard'),

    path('Dashboard/Gender/Details/', views.gender_details_dashboard, name='gender_details_dashboard'),

    path('Dashboard/Repeat-Vehicles-Count/Details/', views.repeat_vehicle_details_dashboard, name='repeat_vehicle_details_dashboard'),

    path('Dashboard/Repeat-Visitors-Count/Details/', views.repeat_visitor_details_dashboard, name='repeat_visitor_details_dashboard'),

    path('Dashboard/Camera-Tampering/Details/', views.camera_tampering_details_dashboard, name='camera_tampering_details_dashboard'),

    path('Cluster/get_cameras/', views.get_cameras, name='get_cameras'),

    path('get_clusters/', views.get_clusters, name='get_clusters'),

    # path('Profile/<username>/', views.profile, name='profile'),

    path('Profile/', views.profile, name='profile'),

    # path('Profile/<username>/change-password', views.change_password, name='change_password'),


    path('Profile/change-password/', views.change_password, name='change_password'),



    path('Report/Visitors-Count/', views.count_visitors, name='count_visitors'),

    path('Report/Age-Gender/', views.age_gender, name='age_gender'),

    path('Report/Vehicle-Count/', views.count_vehicles, name='count_vehicles'),

    path('Report/Repeat-Vehicles-Count/', views.repeat_vehicles_count, name='repeat_vehicles_count'),

    path('Report/Repeat-Visitors/', views.repeat_visitors_count, name='repeat_visitors_count'),

    path('Report/Camera-Tampering/', views.camera_tampering, name='camera_tampering'),



    path('Report/Visitors-Count/Details/', views.visitor_details, name='visitor_details'),

    path('Report/Vehicle-Count/Details/', views.vehicle_details, name='vehicle_details'),

    path('Report/Age-Gender/Details/', views.age_details, name='age_details'),

    path('Report/Repeat-Vehicles-Count/Details/', views.repeat_vehicle_details, name='repeat_vehicle_details'),

    path('Report/Repeat-Visitors/Details/', views.repeat_visitor_details, name='repeat_visitor_details'),

    path('Report/Camera-Tampering/Details/', views.camera_tampering_details, name='camera_tampering_details'),



    path('Super-Admin/algorithms/', views.algo_list, name='algo_list'),

    path('Super-Admin/algorithms/Add_Algorithm/', views.add_algo, name='add_algo'),

    path('Super-Admin/algorithms/Edit_Algorithm/<int:algo_id>/', views.edit_algo, name='edit_algo'),

    path('Super-Admin/algorithms/Delete_Algorithm/<int:algo_id>/', views.delete_algo, name='delete_algo'),






    path('Super-Admin/Customers/', views.customer_list, name='customer_list'),

    path('Super-Admin/Customers/Add_Customer/', views.add_customer, name='add_customer'),

    path('Super-Admin/Customers/Edit_Customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),

    path('Super-Admin/Customers/Delete_Customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),




    path('Super-Admin/Bill-Plan/', views.bill_list, name='bill_list'),

    path('Super-Admin/Bill-Plan/Add_Bill/', views.add_bill, name='add_bill'),

    path('Super-Admin/Bill-Plan/Edit_Bill/<int:bill_id>/', views.edit_bill, name='edit_bill'),

    path('Super-Admin/Bill-Plan/Delete_Bill/<int:bill_id>/', views.delete_bill, name='delete_bill'),




    path('Super-Admin/Menu/', views.menu_list, name='menu_list'),

    path('Super-Admin/Menu/Add_Menu/', views.add_menu, name='add_menu'),

    path('Super-Admin/Menu/Edit_Menu/<int:menu_id>/', views.edit_menu, name='edit_menu'),

    path('Super-Admin/Menu/Delete_Menu/<int:menu_id>/', views.delete_menu, name='delete_menu'),






    path('Super-Admin/SubMenu/', views.submenu_list, name='submenu_list'),

    path('Super-Admin/SubMenu/Add_SubMenu/', views.add_submenu, name='add_submenu'),

    path('Super-Admin/SubMenu/Edit_SubMenu/<int:submenu_id>/', views.edit_submenu, name='edit_submenu'),

    path('Super-Admin/SubMenu/Delete_SubMenu/<int:submenu_id>/', views.delete_submenu, name='delete_submenu'),





    path('Admin/Roles/', views.role_list, name='role_list'),

    path('Admin/Roles/Add_Role/', views.add_role, name='add_role'),

    path('Admin/Roles/Edit_Role/<int:role_id>/', views.edit_role, name='edit_role'),

    path('Admin/Roles/Delete_Role/<int:role_id>/', views.delete_role, name='delete_role'),

    path('Admin/Roles/Details/<int:role_id>/', views.role_details, name='role_details'),




    path('Admin/User/', views.user_list, name='user_list'),

    path('Admin/User/Add_User/', views.add_user, name='add_user'),

    path('Admin/User/Edit_User/<int:user_id>/', views.edit_user, name='edit_user'),

    path('Admin/User/Add_User/Delete_User/<int:user_id>/', views.delete_user, name='delete_user'),


    path('Admin/Authorization/', views.authorization, name='authorization'),

    path('Admin/View-Feed/', views.view_feed, name='view_feed'),

    path('Admin/Subscription/', views.subscription, name='subscription'),

    path('Admin/Subscription-Plan/', views.subscription_plan, name='subscription_plan'),

    path('Admin/Subscription/summary/', views.summary, name='summary'),

    path('Admin/Configuration/Cluster/', views.cluster_list, name='cluster_list'),

    path('Admin/Configuration/Cluster/Add_Cluster/', views.add_cluster, name='add_cluster'),

    path('Admin/Configuration/Cluster/Edit_Cluster/<int:cluster_id>/', views.edit_cluster, name='edit_cluster'),

    path('Admin/Configuration/Cluster/Delete_Cluster/<int:cluster_id>/', views.delete_cluster, name='delete_cluster'),

    path('Admin/Configuration/Camera/', views.camera_table, name='camera'),

    path('Admin/Configuration/Camera/Add_Camera/', views.add_camera, name='add_camera'),

    path('Admin/Configuration/Camera/Edit_Camera/<int:camera_id>/', views.edit_camera, name='edit_camera'),

    path('Admin/Configuration/Camera/Delete_Camera/<int:camera_id>/', views.delete_camera, name='delete_camera'),

    path('Admin/Configuration/Other-Config/', views.other_config, name='other_config'),

    path('logout/', views.logout_request, name='logout_request'),
]
