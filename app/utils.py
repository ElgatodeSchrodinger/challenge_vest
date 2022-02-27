import logging

_logger = logging.getLogger(__name__)
def format_string_with_dict(template: str, values: dict):
    try:
        result = template.format(**values)
        return result
    except KeyError as e:
        _logger.critical("[Programming Error]: Values does not match with the template")
        