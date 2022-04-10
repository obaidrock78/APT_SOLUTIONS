from django.conf import Settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from auth_email_verify.models import TeamMember

from auth_email_verify.tokens import account_activation_token
from django.conf import settings as _settings
from .models import Client, Company, Customer, ServiceItem, Supplier

# Create your views here.


# For Index page with View
from customers.forms import CreateContactForm, CreateNoteForm, CustomerForm, ServiceItemForm, SupplierForm
from .utilities import get_company


@login_required(login_url='signin')
def home(request):
    company = get_company(request)
    # if company is None:
    print(company)
    if company is None:
        return redirect('signin')
    return render(request, "home/index.html")

# @login_required
@login_required(login_url='signin')
def customers_list(request):
    # company = get_company(request)
    # if company is None:
    #     return redirect("signin")
    # customers = Customer.objects.filter(company=company)
    customers = request.user.get_customers
    return render(request, 'customers/index.html', {'customers': customers})

@login_required(login_url='signin')
def client_list(request):
    clients = request.user.get_clients
    clients = clients.order_by("-id")
    type = request.GET.get('type', None)
    if type:
        clients = clients.filter(customer_type=type)
    return render(request, 'customers/index.html', {'customers': clients})

@login_required(login_url='signin')
def client_detail(request, id):
    client = get_object_or_404(Client, id = id)
    if client not in request.user.get_clients:
        raise Http404()

    create_contact_form = CreateContactForm()
    create_note_form = CreateNoteForm()
    context = {
        'client': client,
        'create_contact_form': create_contact_form,
        'create_note_form': create_note_form,
        }
    return render(request, 'customers/client_detail.html', context)


@login_required(login_url='signin')
def contact_create(request):
    if request.method == "POST":
        client_id = request.POST.get('client_id', None)
        create_contact_form = CreateContactForm(request.POST)
        client = get_object_or_404(Client, id = client_id)
        if create_contact_form.is_valid():
            contact = create_contact_form.save(commit=False)
            contact.parent = client
            contact.save()
        return HttpResponseRedirect(reverse("customers:client_detail", kwargs={'id': client.id}))

@login_required(login_url='signin')
def note_create(request):
    if request.method == "POST":
        client_id = request.POST.get('client_id', None)
        create_note_form = CreateNoteForm(request.POST)
        client = get_object_or_404(Client, id = client_id)
        if create_note_form.is_valid():
            note = create_note_form.save(commit=False)
            note.parent = client
            note.save()
        return HttpResponseRedirect(reverse("customers:client_detail", kwargs={'id': client.id}))

@login_required(login_url='signin')
def services(request):
    if request.method == "GET":
        # services = ServiceItem.objects.all()
        services = request.user.get_service_items
        form = ServiceItemForm()
        context = {'services': services, 'form': form}
        return render(request, 'customers/services.html', context)
    elif request.method == "POST":
        form = ServiceItemForm(request.POST)
        services = request.user.get_service_items
        if form.is_valid():
            service_item = form.save(commit=False)
            service_item.company = get_company(request)
            service_item.save()
        context = {'services': services, 'form': form}
        return render(request, 'customers/services.html', context)

@login_required(login_url='signin')
def settings(request):
    return render(request, 'customers/settings.html')


@login_required(login_url='signin')
def team_members(request):
    if request.method == "GET":
        # team_members = TeamMember.objects.all()
        team_members = request.user.get_team_members
        context = {'team_members': team_members}
        return render(request, 'customers/team_members.html', context)
    if request.method == "POST":
        invite_email = request.POST.get('invite_email', None)
        if invite_email:
            current_site = get_current_site(request)
            company = get_company(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('customers/invite_template.html', {
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(invite_email)),
                        'company': urlsafe_base64_encode(force_bytes(company.id)),
                        'token': account_activation_token.make_token(None, invite_email),
                    })
            to_email = invite_email
            from_email = _settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, [to_email])
        return redirect("customers:team_members")


# @login_required
# @login_required(login_url='signin')
# def suppliers_list(request):
#     company = get_company(request)
#     # if company is None:
#     if company is not None:
#         return redirect("signin")
#     suppliers = Supplier.objects.filter(company=company)
#     return render(request, 'suppliers/index.html', {'suppliers': suppliers})
@login_required(login_url='signin')
def suppliers_list(request):
    suppliers = request.user.get_suppliers
    # suppliers = Supplier.objects.all()
    return render(request, 'suppliers/index.html', {'suppliers': suppliers})


# @login_required
@login_required(login_url='signin')
def customers_create(request):
    company = get_company(request)
    if company is None:
        return redirect("signin")
    if request.method == "POST":
        print(request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                customer = form.save(commit=False)
                customer.company = company
                customer.save()
                return redirect('/customers')
            except:
                pass
    else:
        form = CustomerForm()
    return render(request, 'customers/new.html', {'form': form, 'company': company.id})


# @login_required
@login_required(login_url='signin')
def suppliers_create(request):
    # company = get_company(request)
    company = request.user.company
    # company = Company.objects.all().last()
    # if company is None:
    #     return redirect("signin")
    if request.method == "POST":
        form = SupplierForm(request.POST)
        # print(form.is_valid())
        # print(form.errors)
        if form.is_valid():
            try:
                supplier = form.save(commit=False)
                supplier.company = company
                supplier.save()
                return redirect('/suppliers')
            except:
                pass
    else:
        form = SupplierForm()
    return render(request, 'suppliers/new.html', {'form': form, 'company': company.id})



# @login_required
@login_required(login_url='signin')
def client_create(request):
    if request.method == "POST":
        # print(request.POST)
        contact_name = request.POST.get('contact_name', None)
        account_type = request.POST.get('account_type', None)
        customer_type = request.POST.get('customer_type', None)
        entity = request.POST.get('entity', None)
        company_name = request.POST.get('company_name', None)
        trading_name = request.POST.get('trading_name', None)
        work_email = request.POST.get('work_email', None)
        landline_number = request.POST.get('landline_number', None)
        mobile_number = request.POST.get('mobile_number', None)
        note_field = request.POST.get('note_field', None)
        financial_year_end = request.POST.get('financial_year_end', None)
        registration_number = request.POST.get('registration_number', None)
        registration_date = request.POST.get('registration_date', None)
        income_tax = request.POST.get('income_tax', None)
        vat_number = request.POST.get('vat_number', None)
        vat_month = request.POST.get('vat_month', None)
        payee_number = request.POST.get('payee_number', None)
        uif_number = request.POST.get('uif_number', None)
        coida_number = request.POST.get('coida_number', None)
        efiling_profile = request.POST.get('efiling_profile', None)
        last_financials = request.POST.get('last_financials', None)
        billing_address = request.POST.get('billing_address', None)
        billing_city = request.POST.get('billing_city', None)
        billing_state = request.POST.get('billing_state', None)
        billing_zip = request.POST.get('billing_zip', None)
        billing_country = request.POST.get('billing_country', None)
        address = request.POST.get('address', None)
        address_city = request.POST.get('address_city', None)
        address_state = request.POST.get('address_state', None)
        address_zip = request.POST.get('address_zip', None)
        address_country = request.POST.get('address_country', None)

        client_date = request.POST.get('client_date', None)
        employer = request.POST.get('employer', None)
        date_birth = request.POST.get('date_birth', None)
        marital_status = request.POST.get('marital_status', None)
        id_number = request.POST.get('id_number', None)
        occupation = request.POST.get('occupation', None)


        if not client_date:
            client_date = None

        client = Client.objects.create(
            name = contact_name,
            account_type = account_type,
            customer_type = customer_type,
            company = get_company(request),
            entity = entity,
            company_name = company_name,
            trading_name = trading_name,
            work_email = work_email,
            landline_number = landline_number,
            mobile_number = mobile_number,
            note_field = note_field,
            financial_year_end = financial_year_end,
            registration_number = registration_number,
            registration_date = registration_date,
            income_tax = income_tax,
            vat_number = vat_number,
            vat_month = vat_month,
            payee_number = payee_number,
            uif_number = uif_number,
            coida_number = coida_number,
            efiling_profile = efiling_profile,
            last_financials = last_financials,
            billing_address = billing_address,
            billing_city = billing_city,
            billing_state = billing_state,
            billing_zip = billing_zip,
            billing_country = billing_country,
            address = address,
            address_city = address_city,
            address_state = address_state,
            address_zip = address_zip,
            address_country = address_country,

            client_date=client_date,
            employer=employer,
            date_birth=date_birth,
            marital_status=marital_status,
            id_number=id_number,
            occupation=occupation
        )
        client.save()

        return HttpResponseRedirect(reverse('customers:clients_list'))
