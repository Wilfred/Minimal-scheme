from data_types import Cons

test_list = Cons.from_list([1,2,3])

def iterative_sum(linked_list):
    total = 0

    while linked_list:
        total += linked_list.head
        linked_list = linked_list.tail

    return total

print(iterative_sum(test_list))


def tail_recursive_sum(linked_list, sum_so_far):
    if linked_list:
        tail_recursive_sum(linked_list.tail, sum_so_far + linked_list.head)
    else:
        return sum_so_far

print(tail_recursive_sum(test_list, 0))


def iterative_continuation_sum(linked_list, continuation):
    total = 0

    while linked_list:
        total += linked_list.head
        linked_list = linked_list.tail

    return continuation(total)

iterative_continuation_sum(linked_list, print)


def tail_recursive_continuation_sum(linked_list, sum_so_far, continuation):
    if linked_list:
        tail_recursive_continuation_sum(
            linked_list.tail, sum_so_far + linked_list.head, continuation)
    else:
        continuation(sum_so_far)

tail_recursive_continuation_sum(test_list, 0, print)
