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

from horizon import tabs

from openstack_dashboard.dashboards.admin.routers.portforwardings \
    import tabs as project_tabs

from openstack_dashboard.dashboards.admin.routers.portforwardings \
    import forms as pf_forms

from openstack_dashboard.dashboards.project.routers.portforwardings \
    import views as project_views

LOG = logging.getLogger(__name__)

class AddPortForwardingView(project_views.AddPortForwardingView):
    form_class = pf_forms.AddPortForwarding
    success_url = 'horizon:admin:routers:detail'
    failure_url = 'horizon:admin:routers:detail'

class EditPortForwardingView(project_views.EditPortForwardingView):
    success_url = 'horizon:admin:routers:detail'
    failure_url = 'horizon:admin:routers:detail'

class DetailView(tabs.TabView):
    tab_group_class = project_tabs.PortForwardingDetailTabs
    template_name = 'admin/networks/ports/detail.html'
