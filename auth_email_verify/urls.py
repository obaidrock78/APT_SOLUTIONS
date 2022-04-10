from django.urls import path
from . import views
from . views import SignUpView, SignInView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('account_verify/<slug:token>', views.account_verify, name='account_verify'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', views.logout_view, name='logout'),

    path('roles/manage', views.manage_roles, name='manage_roles'),
    path('roles/<int:role_id>/edit', views.edit_role, name='edit_role'),
    path('roles/apply-edit', views.apply_role_changes, name='apply_edit'),
    path('roles/delete-role', views.delete_role, name='delete_role'),
    path('roles/create-role', views.create_role, name='create_role'),
    path('user/list-permissions', views.user_permissions, name='user_permissions'),
    path('invite-accept/<slug:email>/<slug:company>/<slug:token>/', views.invite_accept, name='invite_accept'),
]