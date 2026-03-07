from django import template

register = template.Library()


@register.simple_tag
def param_replace(request, **kwargs):
    """
    Заменяет или добавляет GET-параметры, сохраняя остальные.
    Используется для пагинации с сохранением поиска/сортировки.
    """
    d = request.GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()