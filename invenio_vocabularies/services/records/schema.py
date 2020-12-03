# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Vocabulary service schema."""
from invenio_records_resources.services.records.schema import RecordSchema
from marshmallow import EXCLUDE, fields, INCLUDE


class VocabularySchema(RecordSchema):
    """Schema for records v1 in JSON."""

    class Meta:
        """Meta class to reject unknown fields."""

        unknown = INCLUDE

    vocabulary_type = fields.Integer()
