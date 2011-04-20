def safe_len(linked_list):
    if linked_list is None:
        return 0
    return len(linked_list)

def safe_iter(linked_list):
    if linked_list is None:
        return []

    return iter(linked_list)

def get_type(internal_object):
    if hasattr(internal_object, "type"):
        return internal_object.type
    else:
        return "LIST"
