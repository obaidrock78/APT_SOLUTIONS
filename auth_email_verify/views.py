import json
import uuid

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import HttpResponse

from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .actions import user_allow_admin, send_email_after_registration
from .forms import SignUpForm, SignInForm
from .models import AuthRole, Profile, User, RolePermission

from .app_permissions import categorized_permissions, find_permission_obj, find_permission_objs_many

# Account Verification
def account_verify(request, token):
    # print(token)
    pf = Profile.objects.filter(token=token).first()
    # print(pf)
    pf.verify = True
    pf.save()
    messages.success(request, 'Your Account Has Been Verified, You Can Login')
    return redirect('signin')

#Sign Up View
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'auth_email_verify/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        # print(form)
        if form.is_valid():
            new_user = form.save()
            # print(new_user)
            uid = uuid.uuid4()
            # print(uid)
            pro_obj = Profile(user=new_user, token=uid)
            pro_obj.save()

            send_email_after_registration(new_user.email, uid)
            messages.success(request, 'Your account has been created successfully. To verify your account check your email')
            return redirect('signup')
        return render(request, 'auth_email_verify/signup.html', {'form': form})


# Login View
class SignInView(View):
    def get(self, request):
        # if not request.user.is_authenticated:
            # user = authenticate(username="PaulS", password="Jordyn16$")
            # login(request, user)        
        # return redirect('customers:clients_list')

        form = SignInForm()
        return render(request, 'auth_email_verify/signin.html', {'form': form})

    def post(self, request):
        form = SignInForm(request, data=request.POST)

        # print(form)
        if form.is_valid():
            # print(form)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print(username, password)

            # user = User.objects.get(username=username)
            # print(user)
            user = authenticate(username=username,  password=password)

            pro = Profile.objects.get(user=user)
            # print(pro)
            if pro.verify:
                # print("Ok")
                login(request, user)
                return redirect('customers:home')
            else:
                messages.success(request, 'Your Account Is Not Verified, Check Your Email To Verify Your Account ')
                return redirect('signin')

        messages.error(request, 'Invalid username or password')
        return render(request, 'auth_email_verify/signin.html', { 'form': form })


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("signin")

def role_unlocked(role: AuthRole):
    return not (
        role.label in ('admin_regular', 'admin_no_bill') 
    )


def make_role_info(role: AuthRole):
    user_count = User.objects.filter(role=role).count()
    can_delete = user_count == 0 and role_unlocked(role)

    return {
        'role': role,
        'can_delete': can_delete,
        'assigned_user_count': user_count
    }

@user_passes_test(user_allow_admin)
def manage_roles(request):
    roles_infos = [make_role_info(role) for role in AuthRole.objects.all()]

    return render(request, 'auth_email_verify/list_roles.html', context={
        'all_roles_infos': roles_infos
    })

def can_edit_role(role: AuthRole):
    return role.rltype == AuthRole.RlType.USER_DEFINED and role_unlocked(role)

@user_passes_test(user_allow_admin)
def edit_role(request, role_id):
    role = get_object_or_404(AuthRole, pk=role_id)

    can_change = can_edit_role(role)

    categories = categorized_permissions()
    role_perms_cats = []

    for category in categories:
        role_perms = []
        active_count = 0
        for p in category.perms:
            permission_active = role.has_permission(p.slug)
            active_count += int(permission_active)

            role_perms.append({
                **p.__dict__,
                'active': permission_active
            })

        role_perms_cats.append({
            'name': category.name,
            'full': active_count == len(category.perms),
            'perms': role_perms
        })

    return render(request, 'auth_email_verify/edit_role.html', context={
        'role': role,
        'can_change': can_change,
        'perm_cats': role_perms_cats
    })

@require_http_methods(['POST'])
@user_passes_test(user_allow_admin)
def apply_role_changes(request):
    role_id = request.POST.get('role_id', 0)
    role_name = request.POST.get('role_name', '').strip()
    role = get_object_or_404(AuthRole, pk=role_id)

    role_delta_json = request.POST.get('role_delta_json', None)

    if not can_edit_role(role):
        messages.error(request, 'You cannot modify this role')
        return redirect(reverse('manage_roles'))

    try:
        if role_name == '':
            raise Exception
    
        if role_delta_json is None:
            raise Exception
        deltas = json.loads(role_delta_json)
    except:
        messages.error(request, 'Invalid input')
        return redirect(reverse('edit_role', args=[role_id]))

    role.name = role_name
    role.save()

    for d in map(str, deltas):
        change_sign = d[0]
        perm_slug = d[1:]

        permission = find_permission_obj(perm_slug)
        if permission is None:
            continue

        if change_sign == '+':
            role.give_permission(permission)
        elif change_sign == '-':
            role.remove_permission(permission)

    messages.success(request, "Changes applied successfully.")
    if len(deltas) == 0:
        messages.warning(request, "No changes made to permissions.")
        
    return redirect(reverse('manage_roles'))


@require_http_methods(['POST'])
@user_passes_test(user_allow_admin)
def create_role(request):
    role_id = request.POST.get('source_role_id', 0)

    # Check if the user wants to create a new role or duplicate an existing one
    if role_id == '__create_new__':
        new_role = AuthRole.objects.create(
            name=f"New Role",
            label='other',
            rltype=AuthRole.RlType.USER_DEFINED,
        )
    else:
        # Get the role and create a duplicate
        role = get_object_or_404(AuthRole, pk=role_id)
        new_role = AuthRole.objects.create(
            name=f"{role.name} (Copy)",
            label='other',
            rltype=AuthRole.RlType.USER_DEFINED,
        )

        # Copy over the permissions
        app_permissions = map(find_permission_obj, role.flat_permissions_list())
        db_permissions = [
            new_role.wrap_permission_object(p) 
            for p in app_permissions
            if p is not None
        ]
        RolePermission.objects.bulk_create(db_permissions)

    return redirect(reverse('edit_role', args=[new_role.id]))    


@require_http_methods(['POST'])
@user_passes_test(user_allow_admin)
def delete_role(request):
    role_id = request.POST.get('role_id', 0)
    role = get_object_or_404(AuthRole, pk=role_id)

    active_users_exists = User.objects.filter(role=role).exists()
    can_delete = not active_users_exists and role_unlocked(role)

    if not can_delete:
        messages.error(request, "This role cannot be deleted.")
    else:
        role.permission_objs.all().delete()
        role.delete()
        messages.success(request, "Role deleted successfully")

    return redirect(reverse('manage_roles'))

@login_required
def user_permissions(request):
    current_user: User = request.user
    perm_objs = find_permission_objs_many(*current_user.role.flat_permissions_list())
    return render(request, 'auth_email_verify/user_permissions.html', context={
        'perm_objs': perm_objs    
    })