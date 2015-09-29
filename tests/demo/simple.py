import jsonresolver


@jsonresolver.route('/test', host='http://localhost:4000')
def simple():
    return {'test': 'test'}
