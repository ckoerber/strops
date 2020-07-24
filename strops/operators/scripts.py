"""Scripts for operator module."""
from strops.operators.models import SCALES, KINDS, CONJUGATIONS, Field


def create_all_fields():
    """Creates all allowed field combinations."""
    for scale, _ in SCALES:
        for kind, _ in KINDS[scale]:
            Field.objects.get_or_create(scale=scale, kind=kind, conjugated=False)
            if CONJUGATIONS[scale][kind]:
                Field.objects.get_or_create(scale=scale, kind=kind, conjugated=True)


def main():
    """Runs all operators scripts.

    Execution order:
    1. create_all_fields
    """
    create_all_fields()


if __name__ == "__main__":
    main()
