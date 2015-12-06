import logging

from status import people


def handle_sunrise():

    if people.is_person_home('brad'):
        trigger_simple_sunrise()
        return "Sunrise Triggered", 200
    return "Sunrise not Triggered", 200


def trigger_simple_sunrise():
    logging.debug("Would trigger sunrise shortcut")