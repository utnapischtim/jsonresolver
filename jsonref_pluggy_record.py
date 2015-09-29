import jsonref_pluggy
from werkzeug.routing import Rule


@jsonref_pluggy.hookimpl
def jsonrefpluggy_loader(url_map):
    def endpoint(recid):
        from invenio_records.api import get_record
        return get_record(recid).dumps()

    url_map.add(
        Rule('/record/<recid>', endpoint=endpoint, host='http://localhost:4000')
    )
