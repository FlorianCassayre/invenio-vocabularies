# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Commands to create and manage vocabulary."""

import json

import click
from flask.cli import with_appcontext
from invenio_db import db

from invenio_vocabularies.records.api import Vocabulary
from invenio_vocabularies.records.models import VocabularyType


@click.group()
def vocabulary():
    """Vocabulary CLI."""
    pass


@vocabulary.group()
def index():
    """Index vocabularies in Elasticsearch."""
    pass


@index.command(name="json")
@click.option("--force", is_flag=True)
@click.argument("type_name")
@click.argument("filename")
@with_appcontext
def index_json(type_name, filename, force):
    """Index JSON-based vocabularies in Elasticsearch."""
    if not force:
        click.confirm(
            "Are you sure you want to index the vocabularies?", abort=True
        )
    source = "json"

    click.echo("indexing vocabularies in {}...".format(filename))
    items = load_vocabulary(type_name, source, filename)
    indexer = None  # TODO
    with click.progressbar(items) as bar:
        for item in bar:
            indexer.index(item)
    click.echo("indexed vocabulary")


def load_vocabulary(type_name, source, filename, *args, **kwargs):
    """Load vocabulary items from a vocabulary source."""
    assert source == "json"
    records = []
    with db.session.being_nested():
        vocabulary_type = VocabularyType(name=args[0])
        db.session.add(vocabulary_type)
        with open(filename) as json_file:
            json_array = json.load(json_file)
            for item_data in json_array:
                vocabulary_item = Vocabulary.create(
                    {"type": type_name, **item_data}
                )
                records.append(vocabulary_item)
    db.session.commit()
    return records
