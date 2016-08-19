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
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import tables
from openstack_dashboard import api
from openstack_dashboard import policy

LOG = logging.getLogger(__name__)


class AddPortForwarding(policy.PolicyTargetMixin, tables.LinkAction):
    name = "create"
    verbose_name = _("Add Port Forwarding")
    url = "horizon:project:routers:addportforwarding"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "add_router_portforwarding"),)

    def get_link_url(self, datum=None):
        router_id = self.table.kwargs['router_id']
        return reverse(self.url, args=(router_id,))

class EditPortForwarding(policy.PolicyTargetMixin, tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Port Forwarding")
    url = "horizon:project:routers:editportforwarding"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "edit_router_portforwarding"),)

    def get_link_url(self, datum=None):
        router_id = self.table.kwargs['router_id']
        id = datum.get('id')
        return reverse(self.url, args=(router_id, id))


class RemovePortForwarding(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Port Forwarding",
            u"Delete Port Forwardings",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Port Forwarding",
            u"Deleted Port Forwardings",
            count
        )

    failure_url = 'horizon:project:routers:detail'
    policy_rules = (("network", "remove_router_portforwarding"),)

    def delete(self, request, obj_id):
        try:
            router_id = self.table.kwargs['router_id']
            router = api.neutron.router_get(request, router_id)
            protocol, outside_port, inside_addr, inside_port = obj_id.split('_')
            outside_port, inside_port = int(outside_port), int(inside_port)
            portforwardings = router['portforwardings']
            portforwarding = None
            for pf in portforwardings:
                if pf['protocol'] == protocol and pf['outside_port'] == outside_port and \
                   pf['inside_addr'] == inside_addr and pf['inside_port'] == inside_port:
                    portforwarding = pf
                    break
            if portforwarding:
                portforwardings.remove(portforwarding)
                api.neutron.router_update(request, router_id, portforwardings=portforwardings)
        except Exception:
            msg = _('Failed to delete port forwarding %s') % obj_id
            LOG.info(msg)
            router_id = self.table.kwargs['router_id']
            redirect = reverse(self.failure_url, args=[router_id])
            exceptions.handle(request, msg, redirect=redirect)

class PortForwardingsTable(tables.DataTable):
    protocol = tables.Column("protocol",
                           verbose_name=_("Protocol"),
                           display_choices=(('tcp','tcp'),('udp','udp')))
    outside_port = tables.Column("outside_port",
                         verbose_name=_("Outside Port"))
    inside_port = tables.Column("inside_port",
                         verbose_name=_("Inside Port"))
    inside_addr = tables.Column("inside_addr",
                         verbose_name=_("Inside Address"))

    def get_object_display(self, portforwarding):
        return portforwarding.id

    class Meta(object):
        name = "portforwardings"
        verbose_name = _("Port Forwardings")
        table_actions = (AddPortForwarding, RemovePortForwarding)
        row_actions = (EditPortForwarding, RemovePortForwarding, )
