from openstack_dashboard.dashboards.project.routers.portforwardings import forms as pf_forms


class AddPortForwarding(pf_forms.AddPortForwarding):
    success_url = 'horizon:admin:routers:detail'
    failure_url = 'horizon:admin:routers:detail'
