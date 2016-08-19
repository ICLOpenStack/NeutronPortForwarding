# Copyright 2012 NEC Corporation
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

from django.utils.translation import ugettext_lazy as _

from horizon import tables
from openstack_dashboard.dashboards.project.routers.portforwardings \
    import tables as routers_tables

class AddPortForwarding(routers_tables.AddPortForwarding):
    url = "horizon:admin:routers:addportforwarding"

class EditPortForwarding(routers_tables.EditPortForwarding):
    url = "horizon:admin:routers:editportforwarding"

class RemovePortForwarding(routers_tables.RemovePortForwarding):
    failure_url = 'horizon:admin:routers:detail'

class PortForwardingsTable(routers_tables.PortForwardingsTable):
    class Meta(object):
        name = "portforwardings"
        verbose_name = _("Port Forwardings")
        table_actions = (AddPortForwarding,
                         RemovePortForwarding)
        row_actions = (EditPortForwarding, RemovePortForwarding,)
