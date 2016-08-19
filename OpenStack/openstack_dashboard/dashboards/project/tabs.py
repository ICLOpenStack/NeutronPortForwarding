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

from django.utils.translation import ugettext_lazy as _

from horizon import tabs

from openstack_dashboard.dashboards.project.routers.extensions.routerrules\
    import tabs as rr_tabs
from openstack_dashboard.dashboards.project.routers.ports import tables as ptbl
from openstack_dashboard.dashboards.project.routers.portforwardings import tables as portforwardings_tables
from openstack_dashboard.api import neutron

LOG = logging.getLogger(__name__)

class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = "project/routers/_detail_overview.html"

    def get_context_data(self, request):
        return {"router": self.tab_group.kwargs['router']}


class InterfacesTab(tabs.TableTab):
    table_classes = (ptbl.PortsTable,)
    name = _("Interfaces")
    slug = "interfaces"
    template_name = "horizon/common/_detail_table.html"

    def get_interfaces_data(self):
        return self.tab_group.kwargs['ports']

class PortForwardingsTab(tabs.TableTab):
    table_classes = (portforwardings_tables.PortForwardingsTable,)
    name = _("Port Forwardings")
    slug = "portforwardings"
    template_name = "horizon/common/_detail_table.html"

    def get_portforwardings_data(self):
        return [neutron.RouterPortForwarding(item) for item in self.tab_group.kwargs['router']['portforwardings']]


class RouterDetailTabs(tabs.TabGroup):
    slug = "router_details"
    tabs = (OverviewTab, InterfacesTab, PortForwardingsTab, rr_tabs.RulesGridTab,
            rr_tabs.RouterRulesTab)
    sticky = True
