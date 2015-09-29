import pluggy

hookspec = pluggy.HookspecMarker('jsonrefpluggy')


@hookspec
def jsonrefpluggy_loader(url_map):
    """Retrieve JSON document."""
    pass
