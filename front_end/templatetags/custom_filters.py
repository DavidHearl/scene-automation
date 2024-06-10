from django import template

register = template.Library()

@register.filter
def sort_with_zero_first(value, arg):
    return sorted(value, key=lambda x: (-1 if x.contract_number == 0 else 1, -x.contract_number))


@register.filter
def status_to_class(status):
    if status == "Queued":
        return "queued"
    elif status == "WIP":
        return "wip"
    elif status == "Not Required":
        return "not-required"
    elif status == "Hold":
        return "hold"
    elif status == "Minor Fail":
        return "minor-fail"
    elif status == "Major Fail":
        return "major-fail"
    elif status == "Critical Fail":
        return "critical-fail"
    else:
        return "complete"