# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Vocabulary resource."""
from invenio_records_resources.resources import RecordResource, \
    RecordResourceConfig

from invenio_vocabularies.records.schema import VocabularyLinksSchema, \
    SearchLinksSchema


class VocabularyResourceConfig(RecordResourceConfig):
    """Custom record resource configuration."""

    list_route = "/vocabularies"
    item_route = f"{list_route}/<pid_value>"

    links_config = {
        "record": VocabularyLinksSchema,
        "search": SearchLinksSchema,
    }


class VocabularyResource(RecordResource):
    """Custom record resource"."""

    default_config = VocabularyResourceConfig
