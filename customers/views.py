from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Client, Company, Customer, Supplier#, User

# Create your views here.


# For Index page with View
from customers.forms import CustomerForm, SupplierForm#, UserForm
from .utilities import get_company


@login_required(login_url='signin')
def home(request):
    company = get_company(request)
    # if company is None:
    if company is not None:
        return redirect('signin')
    return render(request, "home/index.html")

# @login_required
@login_required(login_url='signin')
def customers_list(request):
    company = get_company(request)
    if company is None:
        return redirect("signin")
    customers = Customer.objects.filter(company=company)
    return render(request, 'customers/index.html', {'customers': customers})

@login_required(login_url='signin')
def client_list(request):
    clients = None
    type = request.GET.get('type', None)
    if type:
        clients = Client.objects.filter(customer_type=type)
    else:
        clients = Client.objects.all()
    return render(request, 'customers/index.html', {'customers': clients})


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
    suppliers = Supplier.objects.all()
    return render(request, 'suppliers/index.html', {'suppliers': suppliers})


# @login_required
@login_required(login_url='signin')
def customers_create(request):
    company = get_company(request)
    if company is None:
        return redirect("signin")
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/customers')
            except:
                pass
    else:
        form = CustomerForm()
    return render(request, 'customers/new.html', {'form': form, 'company': company.id})


# @login_required
@login_required(login_url='signin')
def suppliers_create(request):
    company = get_company(request)
    company = Company.objects.order_by("id").last()
    # if company is None:
    #     return redirect("signin")
    if request.method == "POST":
        form = SupplierForm(request.POST)
        # print(form.is_valid())
        # print(form.errors)
        if form.is_valid():
            try:
                form.save()
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


        client = Client.objects.create(
            account_type = account_type,
            customer_type = customer_type,
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
