# -*- coding: utf-8 -*-
#
# This file is part of jsonresolver
# Copyright (C) 2022 Graz University of Technology.
#
# jsonresolver is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define unit tests to test core functionality."""

import importlib

from mock import patch
from pkg_resources import EntryPoint


class MockEntryPoint(EntryPoint):
    """EntryPoint mock."""

    def load(self):
        """Load module from the mocked entry point."""
        if self.name == "importfail":
            raise ImportError()
        else:
            return importlib.import_module(self.name)


def _mock_entry_points(name):
    """Mock the entry points."""
    data = {
        "espresso": [MockEntryPoint("demo.simple", "demo.simple")],
        "raising": [MockEntryPoint("demo.raising", "demo.raising")],
        "raising_hook": [MockEntryPoint("demo.raising_hook", "demo.raising_hook")],
        "someotherstuff": [],
        "doubletrouble": [
            MockEntryPoint("demo.simple", "demo.simple"),
            MockEntryPoint("demo.simple", "demo.simple"),
        ],
        "importfail": [MockEntryPoint("importfail", "test.importfail")],
    }
    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


patch("pkg_resources.iter_entry_points", _mock_entry_points)
