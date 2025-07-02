from logging import Filter, LogRecord


class LevelFilter(Filter):
    """Filter to records with matching level."""

    def __init__(self, level: int, name: str = None):
        """Filter to records with matching level.

        Args:
            level (int): The logging level to filter by.
            name (str, optional): The name of the filter. Defaults to None.
        """
        if name is None:
            name = f"LevelFilter-{level}"
        super().__init__(name)
        self.level = level

    def filter(self, record: LogRecord) -> bool:
        """Filter to records with matching level.

        Args:
            record (LogRecord): The log record to filter.

        Returns:
            bool: True if the record's level matches the filter's level, False otherwise.
        """
        return True if record.levelno == self.level else False


class RangeFilter(Filter):
    """Filter to records within a specified level range."""

    def __init__(self, min_level: int, max_level: int, name: str = None):
        """Filter to records within a specified level range.

        Args:
            min_level (int): The minimum logging level.
            max_level (int): The maximum logging level.
            name (str, optional): The name of the filter. Defaults to None.
        """
        self.high_level = max(min_level, max_level)
        self.low_level = min(min_level, max_level)
        if name is None:
            name = f"RangeFilter-{self.low_level}-{self.high_level}"
        super().__init__(name)

    def filter(self, record: LogRecord) -> bool:
        """Filter to records within the specified level range.

        Args:
            record (LogRecord): The log record to filter.

        Returns:
            bool: True if the record's level is within the range, False otherwise.
        """
        return True if self.low_level <= record.levelno <= self.high_level else False


class AnyFilter(Filter):
    """Filter to records matching any of the specified filters."""

    def __init__(self, *filters: Filter, name: str = None):
        """Filter to records matching any of the specified filters.

        Args:
            *filters (Filter): The filters to combine.
            name (str, optional): The name of the filter. Defaults to None.
        """
        self.filters = filters
        if name is None:
            filter_name_list = [f.name for f in filters if f.name]
            name = f"AnyFilter-({', '.join(filter_name_list)})"
        super().__init__(name)

    def filter(self, record: LogRecord) -> bool:
        """Filter to records matching any of the specified filters.

        Args:
            record (LogRecord): The log record to filter.

        Returns:
            bool: True if any filter matches the record, False otherwise.
        """
        return any(f.filter(record) for f in self.filters)
