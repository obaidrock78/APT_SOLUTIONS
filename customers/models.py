from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=250, blank=False)
    sub_domain = models.SlugField(max_length=200, blank=False)

    def __str__(self):
        return self.name
        

class Customer(models.Model):

    CATEGORY_CHOICES = (
        ('1', "One"),
        ('2', "Two"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default='2', null=True, blank=True)
    credit_limit = models.FloatField(default=0.00, null=True, blank=True)
    cash_sale_customer = models.BooleanField(default=False, null=True, blank=True)
    customer_vat_number = models.CharField(max_length=200, null=True, blank=True)
    sales_rep = models.CharField(max_length=200, null=True, blank=True)
    opening_balance = models.FloatField(default=0.00, null=True, blank=True)
    opening_balance_as_at = models.DateField(auto_now=True, null=True, blank=True)
    accept_electronic_invoices = models.BooleanField(default=False, null=True, blank=True)

    postal_address_line_one = models.CharField(max_length=200, null=True, blank=True)
    postal_address_line_two = models.CharField(max_length=200, null=True, blank=True)
    postal_address_line_three = models.CharField(max_length=200, null=True, blank=True)
    postal_address_line_four = models.CharField(max_length=200, null=True, blank=True)
    postal_address_postal_code = models.CharField(max_length=200, null=True, blank=True)

    delivery_address_line_one = models.CharField(max_length=200, null=True, blank=True)
    delivery_address_line_two = models.CharField(max_length=200, null=True, blank=True)
    delivery_address_line_three = models.CharField(max_length=200, null=True, blank=True)
    delivery_address_line_four = models.CharField(max_length=200, null=True, blank=True)
    delivery_address_postal_code = models.CharField(max_length=200, null=True, blank=True)

    contact_details_name = models.CharField(max_length=200, null=True, blank=True)
    contact_details_email = models.EmailField(max_length=200, null=True, blank=True)
    contact_details_telephone = models.CharField(max_length=200, null=True, blank=True)
    contact_details_mobile = models.CharField(max_length=200, null=True, blank=True)
    contact_details_fax = models.CharField(max_length=200, null=True, blank=True)
    contact_details_web_address = models.CharField(max_length=200, null=True, blank=True)

    default_settings_discount = models.FloatField(default=0.00, blank=True, null=True)
    default_settings_vat = models.CharField(max_length=100, null=True, blank=True)
    default_settings_statement_distribution = models.CharField(max_length=100, null=True, blank=True)
    default_settings_vat_type = models.CharField(max_length=100, null=True, blank=True)
    default_settings_due_date_for_payments = models.DateField(auto_now=True)

    def __str__(self):
        return f'Company - {self.company} | Customer Name - {self.customer_name}'


class Supplier(models.Model):

    CATEGORY_CHOICES = (
        ('1', "One"),
        ('2', "Two"),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default='1', null=True, blank=True)
    credit_limit = models.FloatField(default=0.00, null=True, blank=True)
    opening_balance = models.FloatField(default=0.00, null=True, blank=True)
    opening_balance_as_at = models.DateField(auto_now=True)
    vat_reference = models.CharField(max_length=200, null=True, blank=True)
    auto_allocate_payments_to_old_invoices = models.BooleanField(default=False)

    postal_address_line_one = models.CharField(max_length=200, null=True, blank=True)
    postal_address_line_two = models.CharField(max_length=200, null=True, blank=True)
    postal_address_line_three = models.CharField(max_length=200, null=True, blank=True)
    postal_address_line_four = models.CharField(max_length=200, null=True, blank=True)
    postal_address_postal_code = models.CharField(max_length=200, null=True, blank=True)

    physical_address_line_one = models.CharField(max_length=200, null=True, blank=True)
    physical_address_line_two = models.CharField(max_length=200, null=True, blank=True)
    physical_address_line_three = models.CharField(max_length=200, null=True, blank=True)
    physical_address_line_four = models.CharField(max_length=200, null=True, blank=True)
    physical_address_postal_code = models.CharField(max_length=200, null=True, blank=True)

    contact_details_name = models.CharField(max_length=200, null=True, blank=True)
    contact_details_email = models.EmailField(max_length=200, null=True, blank=True)
    contact_details_telephone = models.CharField(max_length=200, null=True, blank=True)
    contact_details_mobile = models.CharField(max_length=200, null=True, blank=True)
    contact_details_fax = models.CharField(max_length=200, null=True, blank=True)
    contact_details_web_address = models.CharField(max_length=200, null=True, blank=True)

    default_settings_discount = models.FloatField(null=True, blank=True)
    default_settings_vat = models.CharField(max_length=100, null=True, blank=True)
    default_settings_due_date_for_payments = models.DateField(auto_now=True)

    def __str__(self):
        return f'Company - {self.company} | Suppliers Name - {self.supplier_name}'


class Client(models.Model):
    ACCOUNT_TYPES = (
        ('individual', "Individual"),
        ('business', "Business"),
    )

    CUSTOMER_TYPES = (
        ('client', "Client"),
        ('lead', "Lead"),
    )

    ENTITY_CHOICES = (
        ("cc-member", "CC MEMBER"),
        ("close-corporation", "CLOSE CORPORATION"),
        ("director", "DIRECTOR"),
        ("individual", "INDIVIDUAL"),
        ("non-profit", "NON-PROFIT"),
        ("plc", "PLC"),
        ("pty-ltd", "PTY LTD"),
        ("sole-prop", "SOLE PROP"),
    )

    VAT_CHOICES = (
        ("monthly", "Monthly"),
        ("even", "Even"),
        ("odd", "Odd"),
    )

    account_type        = models.CharField(max_length=300, choices=ACCOUNT_TYPES, null=True)
    customer_type       = models.CharField(max_length=300, choices=CUSTOMER_TYPES, null=True)
    entity              = models.CharField(max_length=300, choices=ENTITY_CHOICES, null=True)
    company_name        = models.CharField(max_length=300, null=True)
    trading_name        = models.CharField(max_length=300, null=True)
    work_email          = models.CharField(max_length=300, null=True)
    landline_number     = models.CharField(max_length=300, null=True)
    mobile_number       = models.CharField(max_length=300, null=True)
    note_field          = models.CharField(max_length=300, null=True)
    financial_year_end  = models.CharField(max_length=300, null=True)
    registration_number = models.CharField(max_length=300, null=True)
    registration_date   = models.CharField(max_length=300, null=True)
    income_tax          = models.CharField(max_length=300, null=True)
    vat_number          = models.CharField(max_length=300, null=True)
    vat_month           = models.CharField(max_length=300, choices=VAT_CHOICES, null=True)
    payee_number        = models.CharField(max_length=300, null=True)
    uif_number          = models.CharField(max_length=300, null=True)
    coida_number        = models.CharField(max_length=300, null=True)
    efiling_profile     = models.CharField(max_length=300, null=True)
    last_financials     = models.CharField(max_length=300, null=True)
    billing_address     = models.CharField(max_length=300, null=True)
    billing_city        = models.CharField(max_length=300, null=True)
    billing_state       = models.CharField(max_length=300, null=True)
    billing_zip         = models.CharField(max_length=300, null=True)
    billing_country     = models.CharField(max_length=300, null=True)
    address             = models.CharField(max_length=300, null=True)
    address_city        = models.CharField(max_length=300, null=True)
    address_state       = models.CharField(max_length=300, null=True)
    address_zip         = models.CharField(max_length=300, null=True)
    address_country     = models.CharField(max_length=300, null=True)

    client_date         = models.CharField(max_length=300, null=True)
    employer            = models.CharField(max_length=300, null=True)
    date_birth          = models.CharField(max_length=300, null=True)
    marital_status      = models.CharField(max_length=300, null=True)
    id_number           = models.CharField(max_length=300, null=True)
    occupation          = models.CharField(max_length=300, null=True)

    def __str__(self):
        return f"{self.trading_name} ({self.customer_type}) ---- ({self.account_type})"