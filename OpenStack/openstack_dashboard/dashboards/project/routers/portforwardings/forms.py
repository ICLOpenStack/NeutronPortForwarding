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
from horizon import messages
from openstack_dashboard import api

LOG = logging.getLogger(__name__)


class AddPortForwarding(forms.SelfHandlingForm):
    router_id = forms.CharField(widget=forms.HiddenInput())
    portforwarding_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    protocol = forms.ChoiceField(label=_("Protocol"))
    outside_port = forms.IntegerField(label=_("Outside Port"), max_value=65535, min_value=1)
    inside_port = forms.IntegerField(label=_("Inside Port"), max_value=65535, min_value=1)
    inside_addr = forms.IPField(label=_("IP Address"), version=forms.IPv4, mask=False)
    failure_url = 'horizon:project:routers:detail'

    def __init__(self, request, *args, **kwargs):
        super(AddPortForwarding, self).__init__(request, *args, **kwargs)
        self.fields['protocol'].choices = [('tcp','tcp'),('udp','udp')]

    def handle(self, request, data):
        router_id = data['router_id']
        del data['router_id']
        try:
            router = api.neutron.router_get(request, router_id)
            portforwardings = router['portforwardings']
            portforwarding_id = data.pop('portforwarding_id', None)
            if portforwarding_id:
                old_portforwarding = None
                for pf in portforwardings:
                    if portforwarding_id == '%s_%s_%s_%s' % (pf['protocol'], pf['outside_port'], pf['inside_addr'], pf['inside_port']):
                        old_portforwarding = pf
                        break
                portforwardings.remove(old_portforwarding)
            portforwardings.append(data)
            api.neutron.router_update(request, router_id, portforwardings=portforwardings)
            msg = _('Port forwarding saved')
            LOG.debug(msg)
            messages.success(request, msg)
            return True
        except Exception as e:
            msg = _('Failed to save port forwarding %s') % e
            LOG.info(msg)
            redirect = reverse(self.failure_url, args=[router_id])
            exceptions.handle(request, msg, redirect=redirect)
