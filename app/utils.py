import logging

_logger = logging.getLogger(__name__)
def format_string_with_dict(template: str, values: dict):
    try:
        result = template.format(**values)
        return result
    except KeyError as e:
        _logger.critical("[Programming Error]: Values does not match with the template")

def compute_margen_percentage(current_value, initial_value):
    if not initial_value:
        return "0%"
    diff_amount = current_value - initial_value
    diff_percentual = round((diff_amount / initial_value) * 100, 2)
    sign = '+' if diff_percentual > 0 else ''
    return sign + str(diff_percentual) + "%"