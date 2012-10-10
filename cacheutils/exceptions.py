class ServeStaleContentException(Exception):
    """
    Raise this exception in a view to force cached to serve stale content.
    """
    pass
