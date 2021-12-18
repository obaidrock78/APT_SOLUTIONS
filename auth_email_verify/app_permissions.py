import dataclasses
from functools import reduce

@dataclasses.dataclass(frozen=True)
class AppPermission:
    slug: str
    title: str
    desc: str

@dataclasses.dataclass(frozen=True)
class PermCategory: 
    name: str 
    perms: list[AppPermission]


__categorized_permissions = [
    PermCategory('Home', [
        AppPermission(slug='admin_tab', title='Admin Tab', 
            desc='View the admin tab, including information on client referrals, contact growth, and workload.')
    ]),
    PermCategory("Work", [
        AppPermission(slug='generic_tasks', title='Generic Tasks', desc='View generic tasks the user has access to.'),
        AppPermission(slug='work_export', title='Export Work', 
            desc='Export all work on the tasks list to a CSV, including generic tasks, client requests, eSignature requests, and notices. Export tax organizers.'),
    ])
]

__all_permissions = list(reduce(lambda a, b: a + b, map(lambda catd_perm: catd_perm.perms, __categorized_permissions), []))

def all_permissions():
    return __all_permissions

def find_permission_obj(slug: str):
    return next((item for item in __all_permissions if item.slug == slug), None)
    