from .models import Company


def get_host_name(request):
    return request.get_host().split(":")[0].lower()


# def get_company(request):
#     host_name = get_host_name(request)
#     sub_domain = host_name.split(".")[0]
#     return Company.objects.filter(sub_domain=sub_domain).first()
def get_company(request):
    return request.user.company
    # return Company.objects.filter(sub_domain=sub_domain).first()
