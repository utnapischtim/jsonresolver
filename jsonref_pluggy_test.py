import jsonref_pluggy


@jsonref_pluggy.route('/test', host='http://localhost:4000')
def jsonrefpluggy_loader():
    return {'test': 'test'}
