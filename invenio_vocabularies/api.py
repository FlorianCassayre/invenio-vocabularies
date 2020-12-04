# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Vocabulary API."""

from babel import default_locale
from flask_babelex import lazy_gettext as _
from flask_principal import Identity
from invenio_access import any_user

from invenio_vocabularies.records.api import Vocabulary
from invenio_vocabularies.services.records.service import Service


class VocabularyItem(dict):
    """A wrapper for a single vocabulary item."""

    def _get_l10n(self, prop, locale):
        """Collapses an internationalized field into a localized one."""
        messages = self.get(prop, {})
        return messages.get(locale) or messages.get(default_locale())

    def get_description(self, locale):
        """Localized description."""
        return self._get_l10n("description", locale)

    def get_title(self, locale):
        """Localized title."""
        return self._get_l10n("title", locale)

    def dump(self, locale):
        """Returns a localized copy of this object."""
        return {
            **self,
            "description": self.get_description(locale),
            "title": self.get_title(locale),
        }


class VocabularyBackend:
    """A backend implementation for a vocabulary type."""

    def get(self, identifier):
        """Returns the vocabulary item matching this identifier."""
        return VocabularyItem(
            self.record_cls.pid.resolve(identifier)
        )

    def get_all(self, vocabulary_type):
        """Returns all the vocabulary of this type. Potentially costly."""
        # TODO: any alternative to this?
        service = Service()
        identity = Identity(1)
        identity.provides.add(any_user)
        max_results_count = 10000
        result = service.search(
            identity,
            q=f"vocabulary_type:{vocabulary_type}",
            size=max_results_count
        ).to_dict()["hits"]
        hits = result["hits"]
        if len(hits) < result["total"]:
            raise Exception("Too many items, can't retrieve all of them")
        return list(map(lambda obj: VocabularyItem(obj['metadata']), hits))

    def __init__(self, record_cls):
        """Constructs a new backend instance."""
        super().__init__()
        self.record_cls = record_cls


class ResourceTypeVocabulary:
    """An API for a vocabulary type."""

    title = _("Resource Type")
    backend = VocabularyBackend(Vocabulary)

    def get(self, identifier):
        """Returns the vocabulary item matching this identifier."""
        return self.backend.get(identifier)

    def get_all(self):
        """Returns all the vocabulary of this type."""
        return self.backend.get_all(self.vocabulary_type)

    def dump_all(self):
        """Dumps all the vocabulary of this type."""
        return list(map(lambda v: v.dump(), self.get_all()))

    def __init__(self, vocabulary_type):
        """Constructs a new vocabulary type."""
        super().__init__()
        self.vocabulary_type = vocabulary_type


class VocabularyRegistry:
    """A registry of all the vocabulary type."""

    @staticmethod
    def get(vocabulary_type):
        """Get an instance of a vocabulary type."""
        return ResourceTypeVocabulary(vocabulary_type)
