import uuid

from django.utils.http import int_to_base36

ID_LENGTH = 9


def id_generater() -> str:
    """Random string whose length is of `ID_LENGTH`"""
    return int_to_base36(uuid.uuid4().int)[:ID_LENGTH]
