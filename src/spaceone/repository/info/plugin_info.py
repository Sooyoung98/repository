import functools
from spaceone.api.repository.v1 import plugin_pb2, repository_pb2
from spaceone.core import config
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils

__all__ = ['PluginInfo', 'PluginsInfo', 'VersionsInfo']


def PluginInfo(plugin_info: dict, minimal=False):
    info = {
        'plugin_id': plugin_info.get('plugin_id'),
        'name': plugin_info.get('name'),
        'state': plugin_info.get('state'),
        'image': plugin_info.get('image'),
        'service_type': plugin_info.get('service_type'),
        'registry_type': plugin_info.get('registry_type'),
        'provider': plugin_info.get('provider'),
    }
    if not minimal:
        info.update({
            'registry_config': change_struct_type(plugin_info.get('registry_config')),
            'capability': change_struct_type(plugin_info.get('capability')),
            'template': change_struct_type(plugin_info.get('template')),
            'tags': change_struct_type(plugin_info.get('tags')),
            'labels': change_list_value_type(plugin_info.get('labels')),
            'project_id': plugin_info.get('project_id'),
            'domain_id': plugin_info.get('domain_id'),
            'created_at': utils.datetime_to_iso8601(plugin_info.get('created_at')),
            'updated_at': utils.datetime_to_iso8601(plugin_info.get('updated_at'))
        })

        if 'registry_url' in plugin_info:
            info['registry_url'] = plugin_info['registry_url']
        else:
            info['registry_url'] = config.get_global('REGISTRY_URL_MAP', {}).get(plugin_info.get('registry_type'))

        if repository_info := plugin_info.get('repository_info'):
            info.update({
                'repository_info': repository_pb2.RepositoryInfo(
                    repository_id=repository_info.get('repository_id'),
                    name=repository_info.get('name'),
                    repository_type=repository_info.get('repository_type'),
                )
            })

    return plugin_pb2.PluginInfo(**info)


def PluginsInfo(plugins_info, total_count, **kwargs):
    return plugin_pb2.PluginsInfo(results=list(
        map(functools.partial(PluginInfo, **kwargs), plugins_info)), total_count=total_count)


def VersionsInfo(version_list):
    return plugin_pb2.VersionsInfo(results=version_list, total_count=len(version_list))
