"""Fixture slice. First import refuses an existing destination."""


def copy_allowed(destination_exists, readopt):
    if destination_exists and not readopt:
        return False
    return True
