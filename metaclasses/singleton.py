class Singleton(type):
    """
    A metaclass for creating a singleton class .
    Ensures that only one instance of the class can be created.

    Usage: class <class name>(metaclass = Singleton):
    """

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)

        return cls._instance
