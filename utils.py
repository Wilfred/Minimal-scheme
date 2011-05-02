def get_type(internal_object):
    if hasattr(internal_object, "type"):
        return internal_object.type
    else:
        return "LIST"
