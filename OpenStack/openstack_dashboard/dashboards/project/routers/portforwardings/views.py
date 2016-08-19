# Copyright 2012,  Nachi Ueno,  NTT MCL,  Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.project.routers.portforwardings \
    import forms as project_forms
from openstack_dashboard.dashboards.project.routers.portforwardings \
    import tabs as project_tabs

LOG = logging.getLogger(__name__)


class AddPortForwardingView(forms.ModalFormView):
    form_class = project_forms.AddPortForwarding
    template_name = 'project/routers/portforwardings/create.html'
    success_url = 'horizon:project:routers:detail'
    failure_url = 'horizon:project:routers:detail'
    page_title = _("Add Port Forwarding")

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['router_id'],))

    @memoized.memoized_method
    def get_object(self):
        router_id = self.kwargs["router_id"]
        try:
            return api.neutron.router_get(self.request, router_id)
        except Exception:
            redirect = reverse(self.failure_url, args=[router_id])
            msg = _("Unable to retrieve router.")
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(AddPortForwardingView, self).get_context_data(**kwargs)
        context['router'] = self.get_object()
        return context

    def get_initial(self):
        router = self.get_object()
        return {"router_id": self.kwargs['router_id'],
                "router_name": router.name}

class EditPortForwardingView(forms.ModalFormView):
    form_class = project_forms.AddPortForwarding
    template_name = 'project/routers/portforwardings/edit.html'
    success_url = 'horizon:project:routers:detail'
    failure_url = 'horizon:project:routers:detail'
    page_title = _("Edit Port Forwarding")

    def get_success_url(self):
        return reverse(self.success_url,
                       args=(self.kwargs['router_id'],))

    @memoized.memoized_method
    def get_object(self):
        router_id = self.kwargs["router_id"]
        try:
            return api.neutron.router_get(self.request, router_id)
        except Exception:
            redirect = reverse(self.failure_url, args=[router_id])
            msg = _("Unable to retrieve router.")
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_context_data(self, **kwargs):
        context = super(EditPortForwardingView, self).get_context_data(**kwargs)
        context['router'] = self.get_object()
        context['portforwarding_id'] = self.kwargs['id']
        return context

    def get_initial(self):
        router = self.get_object()
        protocol, outside_port, inside_addr, inside_port = self.kwargs['id'].split('_')
        outside_port, inside_port = int(outside_port), int(inside_port)
        return {"router_id": self.kwargs['router_id'],
                "portforwarding_id": self.kwargs['id'],
                'protocol':protocol,
                'outside_port':outside_port,
                'inside_addr':inside_addr,
                'inside_port':inside_port
                }
