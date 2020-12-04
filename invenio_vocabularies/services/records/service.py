# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Example service."""
from elasticsearch_dsl import AttrDict
from invenio_records_resources.services import RecordService, \
    RecordServiceConfig
from invenio_records_resources.services.records.search import terms_filter

from ...records.api import Vocabulary
from .components import VocabularyTypeComponent
from .permissions import PermissionPolicy
from .schema import VocabularySchema


class ServiceConfig(RecordServiceConfig):
    """Mock service configuration."""

    permission_policy_cls = PermissionPolicy
    record_cls = Vocabulary
    schema = VocabularySchema
    search_facets_options = {
        "aggs": {
            "vocabulary_type": {
                "terms": {"field": "vocabulary_type"},
            }
        },
        "post_filters": {
            "vocabulary_type": terms_filter("vocabulary_type"),
        },
    }

    components = RecordServiceConfig.components + [
        VocabularyTypeComponent,
    ]


class Service(RecordService):
    """Mock service."""

    default_config = ServiceConfig

    def search(self, identity, params=None, links_config=None,
               es_preference=None, **kwargs):
        """Search for records matching the vocabulary type."""
        self.require_permission(identity, "search")

        params = params or {}
        params.update(kwargs)

        # Create a Elasticsearch DSL
        search = self.search_request(
            identity, params, self.record_cls, preference=es_preference)

        # Run components
        for component in self.components:
            if hasattr(component, 'search'):
                search = component.search(identity, search, params)

        # Execute the search
        search_result = search.scan()
        hits = []
        for hit in search_result:
            record = hit.to_dict()
            hits.append(self.schema.dump(
                identity,
                record,
                pid=hit.pid,
                record=record
            ))

        return AttrDict(dict(hits=dict(hits=hits, total=len(hits))))
