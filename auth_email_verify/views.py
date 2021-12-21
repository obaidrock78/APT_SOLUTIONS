import json
import uuid

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponse

from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail

from .actions import user_allow_admin
from .forms import SignUpForm, SignInForm
from .models import AuthRole, Profile

from .app_permissions import categorized_permissions, find_permission_obj

def send_email_after_registration(email, token):
    subject = 'Verify Email'
    message = f'Click on the link to verify your account http://infinityapp.pythonanywhere.com/account_verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

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
            messages.success(request, 'Your Account Created Successful, To Verify Your Account Check Your Email')
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

def make_role_info(role: AuthRole):

    can_delete = not (
        role.label in ('admin_regular', 'admin_no_bill') 
    )

    return {
        'role': role,
        'can_delete': can_delete
    }

@user_passes_test(user_allow_admin)
def manage_roles(request):
    roles_infos = [make_role_info(role) for role in AuthRole.objects.all()]

    return render(request, 'auth_email_verify/list_roles.html', context={
        'all_roles_infos': roles_infos
    })

@user_passes_test(user_allow_admin)
def edit_role(request, role_id):
    role = get_object_or_404(AuthRole, pk=role_id)

    can_change = not (
        role.label in ('admin_regular', 'admin_no_bill') 
    )

    categories = categorized_permissions()
    role_perms_cats = []

    for category in categories:
        role_perms = []
        active_count = 0
        for p in category.perms:
            permission_active = role.has_permission(p.slug)
            # permission_active = bool(random.getrandbits(1))
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

    role = get_object_or_404(AuthRole, pk=role_id)

    role_delta_json = request.POST.get('role_delta_json', None)

    try:
        if role_delta_json is None:
            raise Exception
        deltas = json.loads(role_delta_json)
    except:
        messages.error(request, 'Invalid input')
        return redirect(reverse('edit_role', args=[role_id]))

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

    if len(deltas) == 0:
        messages.warning(request, "No changes made")
    else:    
        messages.success(request, "Changes applied successfully")
        
    return redirect(reverse('manage_roles'))
