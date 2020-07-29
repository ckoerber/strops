"""Scripts for operator module."""
from logging import getLogger
from strops.operators.models import (
    SCALES,
    KINDS,
    CONJUGATIONS,
    Field,
)

LOGGER = getLogger("strops")


def create_all_fields():
    """Creates all allowed field combinations."""
    LOGGER.info("Creating all fields")
    LOGGER.info("Fields present: %d", Field.objects.count())
    n_created = 0
    for scale, _ in SCALES:
        for kind, _ in KINDS[scale]:
            conjugations = [False]
            if CONJUGATIONS[scale][kind]:
                conjugations.append(True)

            for conjugated in conjugations:
                data = dict(scale=scale, kind=kind, conjugated=conjugated)
                LOGGER.debug(data)
                try:
                    _, created = Field.objects.get_or_create(**data)
                    if created:
                        n_created += 1
                except Exception as error:
                    LOGGER.warning("Failed to create field for data: %s", data)
                    LOGGER.exception(error)

    LOGGER.info("Created %d fields", n_created)
