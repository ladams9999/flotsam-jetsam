from typing import Any
from collections.abc import Collection
from functools import reduce


def coalesce(*values: Any) -> Any:
    """Return the first non-None value from the given arguments, or None if all are None.

    Args:
        *values (Any): A variable number of values to check.

    Returns:
        Any: The first non-None value or None if all are None.
    """
    return next((value for value in values if value is not None), None)

def safe_get(collection: Collection, key: str, default: Any = None) -> Any:
    """Safely get a value from a collection.

    Args:
        collection (Collection): The collection to retrieve the value from.
        key (str): The key to look up in the collection.
        default (Any, optional): The default value to return if the key is not found. Defaults to None.

    Returns:
        Any: The value from the collection or the default value.
    """
    try:
        return collection.get(key, default)
    except (AttributeError, TypeError):
        pass

    try:
        return collection[key]
    except (IndexError, TypeError):
        pass

    return default

def safe_cast(value: Any, as_type: type, default: Any = None) -> Any:
    """Safely cast a value to a specified type.

    Args:
        value (Any): The value to cast.
        as_type (type): The type to cast the value to.
        default (Any, optional): The default value to return if the cast fails. Defaults to None.

    Returns:
        Any: The cast value or the default value.
    """
    try:
        return as_type(value)
    except (ValueError, TypeError):
        return default

def dig(collection: Collection, *keys: str, default: Any = None) -> Any:
    """Safely dig into a nested collection using a sequence of keys.

    Args:
        collection (Collection): The collection to dig into.
        keys (str): The keys to follow in the collection.
        default (Any, optional): The default value to return if the keys are not found. Defaults to None.

    Returns:
        Any: The value found at the specified keys or the default value.
    """
    return reduce(lambda x, y: safe_get(x, y, default), keys, collection)

