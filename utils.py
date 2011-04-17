def safe_len(linked_list):
    if linked_list is None:
        return 0
    return len(linked_list)

def safe_iter(linked_list):
    if linked_list is None:
        return []

    return iter(linked_list)
