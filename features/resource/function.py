from os.path import dirname
from features.resource import anchor


def projpath():
    return dirname(dirname(dirname(anchor.__file__)))