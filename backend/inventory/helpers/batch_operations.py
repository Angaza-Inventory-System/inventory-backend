from django.apps import apps


def validate_ids(data, id_key):
    ids = data.get(id_key)
    if not ids or not isinstance(ids, list):
        return False
    return ids


def get_model(model_path):
    try:
        app_label, model_name = model_path.rsplit(".", 1)
        return apps.get_model(app_label, model_name)
    except ValueError:
        return None
    except LookupError:
        return None
