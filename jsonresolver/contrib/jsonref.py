# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2015 CERN.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Module that implements ``JsonLoader`` factory using ``JSONResolver``.

Use ``json_loader_factory`` if you want to take advantage of default
``JsonLoader.get_remote_json`` method for URIs that are not handled
by your ``JSONResolver`` instance.

Example:
.. code-block:: python

   >>> from jsonref import JsonRef
   >>> from jsonresolver import JSONResolver
   >>> from jsonresolver.contrib.jsonref import json_loader_factory
   >>> schema = {'$ref': 'http://localhost:4000/schema/authors.json#'}
   >>> json_resolver = JSONResolver(plugins=['tests.demo.schema'])
   >>> loader_cls = json_loader_factory(json_resolver)
   >>> loader = loader_cls(cache_results=False)
   >>> dict(JsonRef.replace_refs(schema, loader=loader))
   {'type': 'array'}

   # if you do not want default fallback:
   >>> dict(JsonRef.replace_refs(schema, loader=json_resolver.resolve))
   {'type': 'array'}

"""
from collections.abc import MutableMapping
from urllib import parse as urlparse

from werkzeug.exceptions import NotFound


class _URIDict(MutableMapping):
    """Dictionary which uses normalized URIs as keys."""

    def normalize(self, uri):
        """Normalize."""
        return urlparse.urlsplit(uri).geturl()

    def __init__(self, *args, **kwargs):
        """Construct."""
        self.store = dict()
        self.store.update(*args, **kwargs)

    def __getitem__(self, uri):
        """GetItem."""
        return self.store[self.normalize(uri)]

    def __setitem__(self, uri, value):
        """SetItem."""
        self.store[self.normalize(uri)] = value

    def __delitem__(self, uri):
        """DelItem."""
        del self.store[self.normalize(uri)]

    def __iter__(self):
        """Iterate."""
        return iter(self.store)

    def __len__(self):
        """Len."""
        return len(self.store)

    def __repr__(self):
        """Repr."""
        return repr(self.store)


class _JsonLoader:
    """Provides a callable.

    This means it takes a URI, and returns the loaded JSON referred
    to by that URI. Uses :mod:`requests` if available for HTTP URIs, and falls
    back to :mod:`urllib`. By default it keeps a cache of previously loaded
    documents.

    :param store: A pre-populated dictionary matching URIs to loaded JSON
        documents
    :param cache_results: If this is set to false, the internal cache of
        loaded JSON documents is not used
    """

    def __init__(self, store=(), cache_results=True):
        """Construct."""
        self.store = _URIDict(store)
        self.cache_results = cache_results

    def __call__(self, uri, **kwargs):
        """Return the loaded JSON referred to by `uri`.

        :param uri: The URI of the JSON document to load
        :param kwargs: Keyword arguments passed to :func:`json.loads`
        """
        if uri in self.store:
            return self.store[uri]
        else:
            result = self.get_remote_json(uri, **kwargs)
            if self.cache_results:
                self.store[uri] = result
            return result


def json_loader_factory(resolver):
    """Generate new ``JsonLoader`` class that uses given resolver."""

    class JsonLoader(_JsonLoader):
        """Implement custom remote reference resolver."""

        def get_remote_json(self, uri, **kwargs):
            """Resolve remove uri using given resolver."""
            try:
                return resolver.resolve(uri)
            except NotFound:
                return super(JsonLoader, self).get_remote_json(uri, **kwargs)

    return JsonLoader
