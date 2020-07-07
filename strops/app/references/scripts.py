"""Script utilities for references.

Downloads meta data from inspire records and populates the reference tables.
"""
from typing import Dict, Any, Tuple, List
from datetime import datetime
import requests
from logging import getLogger

from strops.app.references.models import Publication


LOGGER = getLogger("strops")


def get_inspires_meta(inspires_id: int) -> Dict[str, Any]:
    """Extracts meta data from https://inspirehep.net/api/literature/{inspires_id}."""
    url = f"https://inspirehep.net/api/literature/{inspires_id}"
    LOGGER.debug("Accessing %s", url)
    meta = requests.get(url).json().get("metadata")
    meta["inspirehep_id"] = inspires_id
    return meta


def parse_inspires_meta(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Parses inspirehep data to strops schema.

    Arguments:
        meta: get_inspires_meta output.

    Returns: Dictionary which can be used to create a publication entry.
    """
    LOGGER.debug("Parsing meta with keys %s", meta.keys())
    authors = []
    for author in meta["authors"]:
        if "full_name" in author:
            authors.append(author.get("full_name"))
    authors = "; ".join(authors)
    if "publication_info" in meta:
        journal_data = meta["publication_info"][0]
        title = journal_data.get("journal_title", "")
        volume = journal_data.get("journal_volume", "")
        year = f"({journal_data.get('year')})" if "year" in journal_data else ""
        page = journal_data.get("page_start", "")
        journal = " ".join([el for el in (title, volume, year, page) if el])
    else:
        journal = None
    publication_meta = {
        "arxiv_id": meta["arxiv_eprints"][0]["value"],
        "inspirehep_id": meta["inspirehep_id"],
        "authors": authors,
        "title": meta["titles"][0]["title"],
        "journal": journal,
        "preprint_date": datetime.strptime(meta["preprint_date"], "%Y-%m-%d").date(),
    }
    return publication_meta


def insert_inspirehep_entry(inspires_id: int) -> Tuple[Publication, bool]:
    """Inserts publication entry if not already present.

    Returns: The entry and if it was created or not.
    """
    meta = get_inspires_meta(inspires_id)
    data = parse_inspires_meta(meta)
    LOGGER.debug("Inserting %s", data)
    return Publication.objects.get_or_create(**data)


def insert_inspirehep_entries(inspires_ids: List[int]) -> int:
    """Inserts multiple inspires entries if not already present."""
    n_created = 0
    errors = []
    for iid in inspires_ids:
        try:
            _, created = insert_inspirehep_entry(iid)
            if created:
                n_created += 1
                LOGGER.debug("Entry created")
            else:
                LOGGER.debug("Entry already present")
        except Exception as error:
            errors.append(error)
    return n_created, errors
