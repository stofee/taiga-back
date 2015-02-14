# Copyright (C) 2015 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2015 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2015 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.utils.translation import ugettext_lazy as _

from taiga.base.api import ModelCrudViewSet
from taiga.base.api.viewsets import ModelViewSet
from taiga.base import exceptions as exc
from taiga.base import filters
from taiga.base import response

from taiga.projects.mixins.ordering import BulkUpdateOrderMixin
from taiga.projects.history.mixins import HistoryResourceMixin
from taiga.projects.occ.mixins import OCCResourceMixin

from . import models
from . import serializers
from . import permissions
from . import services


######################################################
# Custom Attribute ViewSets
#######################################################

class UserStoryCustomAttributeViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.UserStoryCustomAttribute
    serializer_class = serializers.UserStoryCustomAttributeSerializer
    permission_classes = (permissions.UserStoryCustomAttributePermission,)
    filter_backends = (filters.CanViewProjectFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_userstory_custom_attributes"
    bulk_update_perm = "change_userstory_custom_attributes"
    bulk_update_order_action = services.bulk_update_userstory_custom_attribute_order


class TaskCustomAttributeViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.TaskCustomAttribute
    serializer_class = serializers.TaskCustomAttributeSerializer
    permission_classes = (permissions.TaskCustomAttributePermission,)
    filter_backends = (filters.CanViewProjectFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_task_custom_attributes"
    bulk_update_perm = "change_task_custom_attributes"
    bulk_update_order_action = services.bulk_update_task_custom_attribute_order


class IssueCustomAttributeViewSet(ModelCrudViewSet, BulkUpdateOrderMixin):
    model = models.IssueCustomAttribute
    serializer_class = serializers.IssueCustomAttributeSerializer
    permission_classes = (permissions.IssueCustomAttributePermission,)
    filter_backends = (filters.CanViewProjectFilterBackend,)
    filter_fields = ("project",)
    bulk_update_param = "bulk_issue_custom_attributes"
    bulk_update_perm = "change_issue_custom_attributes"
    bulk_update_order_action = services.bulk_update_issue_custom_attribute_order


######################################################
# Custom Attributes Values ViewSets
#######################################################

class BaseCustomAttributesValuesViewSet(OCCResourceMixin, HistoryResourceMixin,  ModelViewSet):
    def list(self, request, *args, **kwargs):
        return response.NotFound()

    def post_delete(self, obj):
        # NOTE: When destroy a custom attributes values object, the
        #       content_object change after and not before
        self.persist_history_snapshot(obj, delete=True)
        super().pre_delete(obj)

    def get_object_for_snapshot(self, obj):
        return getattr(obj, self.content_object)


class UserStoryCustomAttributesValuesViewSet(BaseCustomAttributesValuesViewSet):
    model = models.UserStoryCustomAttributesValues
    serializer_class = serializers.UserStoryCustomAttributesValuesSerializer
    permission_classes = (permissions.UserStoryCustomAttributesValuesPermission,)
    lookup_field = "user_story_id"
    content_object = "user_story"


class TaskCustomAttributesValuesViewSet(BaseCustomAttributesValuesViewSet):
    model = models.TaskCustomAttributesValues
    serializer_class = serializers.TaskCustomAttributesValuesSerializer
    permission_classes = (permissions.TaskCustomAttributesValuesPermission,)
    lockup_fields = "task_id"
    content_object = "task"


class IssueCustomAttributesValuesViewSet(BaseCustomAttributesValuesViewSet):
    model = models.IssueCustomAttributesValues
    serializer_class = serializers.IssueCustomAttributesValuesSerializer
    permission_classes = (permissions.IssueCustomAttributesValuesPermission,)
    lockup_fields = "issue_id"
    content_object = "issue"
