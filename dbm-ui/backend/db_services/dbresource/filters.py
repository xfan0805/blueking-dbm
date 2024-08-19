# -*- coding:utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters

from backend.db_meta.enums import ClusterType
from backend.db_meta.models.spec import Spec


class SpecListFilter(filters.FilterSet):
    spec_name = filters.CharFilter(field_name="spec_name", lookup_expr="icontains", label=_("规格名称"))
    desc = filters.CharFilter(field_name="desc", lookup_expr="icontains", label=_("描述"))
    spec_cluster_type = filters.CharFilter(field_name="spec_cluster_type", lookup_expr="exact", label=_("规格集群类型"))
    spec_machine_type = filters.CharFilter(field_name="spec_machine_type", lookup_expr="exact", label=_("规格机器类型"))
    spec_db_type = filters.CharFilter(field_name="spec_db_type", method="filter_spec_db_type", label=_("规格组件类型"))
    spec_ids = filters.CharFilter(field_name="spec_ids", method="filter_spec_ids", label=_("ID过滤(逗号分隔)"))
    update_at = filters.BooleanFilter(field_name="update_at", method="filter_update_at", label=_("根据时间正序/逆序"))
    enable = filters.BooleanFilter(field_name="enable", label=_("过滤启用/禁用的规格"))

    def filter_update_at(self, queryset, name, value):
        time_field = "update_at" if value else "-update_at"
        return queryset.order_by(time_field)

    def filter_spec_db_type(self, queryset, name, value):
        cluster_types = ClusterType.db_type_to_cluster_types(value)
        return queryset.filter(spec_cluster_type__in=cluster_types)

    def filter_spec_ids(self, queryset, name, value):
        ids = value.split(",")
        return queryset.filter(spec_id__in=ids)

    class Meta:
        model = Spec
        fields = [
            "spec_name",
            "spec_cluster_type",
            "spec_machine_type",
            "desc",
            "update_at",
            "spec_db_type",
            "spec_ids",
        ]
