__author__ = 'Vikas Saini'

def get_valid_list(app_name, model_name, requested_item):
    model = get_model(app_name, model_name)
    id_list = set(model.objects.values_list('id', flat=True))
    requested_list = set(int(item) for item in requested_item.split('*') if item)
    if 0 in requested_list:
        return list(id_list)
    return list(id_list-requested_list)