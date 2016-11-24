# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
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

from nailgun import extensions
from nailgun import objects
from nailgun.orchestrator.deployment_serializers import \
    get_serializer_for_cluster
from nailgun import utils


logger = logging.getLogger(__name__)


class ConvertPreLCMtoLCM(extensions.BasePipeline):

    @classmethod
    def pre_process_data_for_cluster(cls, cluster, data, **kwargs):
        return data

    @classmethod
    def post_process_data_for_cluster(cls, cluster, data, **kwargs):
        return data

    @classmethod
    def pre_process_data_for_node(cls, node, data, **kwargs):
        return data

    @classmethod
    def post_process_data_for_node(cls, node, data, **kwargs):
        return data

    @classmethod
    def serialize_cluster(cls, cluster, data, **kwargs):
        if objects.Release.is_lcm_supported(cluster.release):
            return data
        else:
            serializer = get_serializer_for_cluster(cluster)()
            serializer.initialize(cluster)
            common_attrs = serializer.get_common_attrs(cluster)
            if cluster.replaced_deployment_info:
                # patch common attributes with custom deployment info
                utils.dict_update(
                    common_attrs, cluster.replaced_deployment_info
                )
            return common_attrs

    @classmethod
    def serialize_node(cls, node, data, **kwargs):
        if objects.Release.is_lcm_supported(node.cluster.release):
            return data
        else:
            serializer = get_serializer_for_cluster(node.cluster)()
            serializer.initialize(node.cluster)
            role = objects.Node.all_roles(node)[0]
            real_data = serializer.serialize_node(node, role)
            return real_data

    @classmethod
    def process_deployment_for_cluster(cls, cluster, data, **kwargs):
        pre_processed_data = cls.pre_process_data_for_cluster(cluster, data,
                                                              **kwargs)
        real_data = cls.serialize_cluster(cluster, pre_processed_data,
                                          **kwargs)

        post_processed_data = cls.post_process_data_for_cluster(
            cluster, real_data, **kwargs)
        # copypaste cluster specific values from LCM serializer.
        # This is needed for tasks paramters interpolation like CLUSTER_ID
        cluster_data = data['cluster']
        post_processed_data['cluster'] = cluster_data
        return post_processed_data

    @classmethod
    def process_deployment_for_node(cls, node, node_data, **kwargs):
        pre_processed_data = cls.pre_process_data_for_node(node,
                                                           node_data, **kwargs)
        real_data = cls.serialize_node(node, pre_processed_data, **kwargs)

        post_processed_data = cls.post_process_data_for_node(node, real_data,
                                                             **kwargs)
        return post_processed_data


class ConvertedSerializersExtension(extensions.BaseExtension):
    name = 'converted_serializers'
    version = '0.0.1'
    description = "Serializers Conversion extension"
    weight = 100

    data_pipelines = [
        ConvertPreLCMtoLCM,
    ]
