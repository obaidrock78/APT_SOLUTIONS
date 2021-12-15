$(function() {
  // $("#create-customer-model").modal('show');
  $(".dn-date").attr('type', 'text');
  $(".dn-date").on('focus', function() {
    $(this).attr('type', 'date');
  });
  $(".dn-date").on('blur change', function() {
    if(this.value == '')
      $(this).attr('type', 'text');
  });


  $("#create-customer-model input[type=radio][name=account_type]").on('change', OnConfigChange);
  $("#create-customer-model input[type=radio][name=customer_type]").on('change', OnConfigChange);

  OnConfigChange();
});

function OnConfigChange()
{
  const accountType = $("#create-customer-model input[type=radio][name=account_type]:checked").val();
  const customerType = $("#create-customer-model input[type=radio][name=customer_type]:checked").val();
  UpdateConfig(accountType, customerType);
}

function UpdateConfig(accountType, customerType)
{
  if (accountType == 'individual')
    $("#extra-fields-business").hide().find('select').attr('required', false);
  else if (accountType == 'business')
    $("#extra-fields-business").show().find('select').attr('required', true);

  if (customerType == 'lead') 
  {
    $("#client-form").hide().find('select').attr('required', false);
    $('#client-date-field').hide();
  }
  else
  {
    $("#client-form").show().find('select').attr('required', true);
    $('#client-date-field').show();

    if (accountType == 'individual')
    {
      $("#details-company").hide().find('select').attr('required', false);
      $("#details-individual").show().find('select').attr('required', true);
    }
    else {
      $("#details-individual").hide().find('select').attr('required', false);
      $("#details-company").show().find('select').attr('required', true);
    }
  }
}