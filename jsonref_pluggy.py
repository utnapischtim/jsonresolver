import importlib
import hookspec
import pluggy

from six.moves.urllib.parse import urlsplit

from werkzeug.routing import Rule, Map

hookimpl = pluggy.HookimplMarker('jsonrefpluggy')


def route(string, host=None):
    """Register rule on decorated function."""
    def decorator(f):
        @hookimpl
        def jsonrefpluggy_loader(url_map):
            url_map.add(Rule(string, endpoint=f, host=host))
        return jsonrefpluggy_loader
    return decorator


def main(url):
    pm = pluggy.PluginManager('jsonrefpluggy')
    pm.add_hookspecs(hookspec)
    plugin = importlib.import_module('jsonref_pluggy_record')
    pm.register(plugin)
    plugin = importlib.import_module('jsonref_pluggy_test')
    pm.register(plugin)

    url_map = Map()
    pm.hook.jsonrefpluggy_loader(url_map=url_map)
    print url_map

    splitted_url = urlsplit(url)
    loader, args = url_map.bind(splitted_url.hostname).match(splitted_url.path)
    print loader(**args)


if __name__ == '__main__':
    main('http://localhost:4000/test')
    main('http://localhost:4000/record/1')
