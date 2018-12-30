from boltons import queueutils as qu
from collections import deque
import random as rd

def beam_algorithm(omega,               # Dataset
                   phi,                 # Quality measure
                   eta,                 # Refinement operator
                   w,                   # Beam width
                   d,                   # Beam depth
                   b,                   # Numbers of bins n
                   q,                   # Result set size q
                   c,                   # Constraints set c
                   targets,             # Names of the features treated as targets
                   types):              # List with the Types of the features in the dataset

    # Pre-treatement of the data. Get the header names.
    names = omega[0]
    target_ind = [names.index(a) for a in targets]  # This is the names of the targets mapped to indices in the names list

    att_indices = list(range(0, len(names)))
    [att_indices.remove(i) for i in target_ind]

    candidate_q = deque([])
    candidate_q.append(set())
    result_set = qu.PriorityQueue()  # This must be a priority queue of size = result_set_size

    for i in range(0, d):

        beam = qu.PriorityQueue()  # This is a priority queue of size = w

        while bool(candidate_q):
            seed = candidate_q.popleft()
            a_set = eta(seed, omega, types, b, att_indices)  # Refinement set... eta [seed]

            for desc in a_set:
                quality = phi(desc)
                if satisfies_all(desc, c):
                    insert_with_priority(result_set, desc, quality, q)
                    insert_with_priority(beam, desc, quality, w)

        while len(beam) != 0:
            index = candidate_q.index(beam.peek())
            candidate_q.pop(index)

    return result_set


def refinement(seed, omega, types, b, att_indices):
    res = []
    used = [i[0] for i in seed]
    cp_att_indices = att_indices[:]
    [cp_att_indices.remove(i) for i in used]
    for i in cp_att_indices:
        aux = seed[:]
        if types[i] == 'numeric':
            pass
        elif types[i] == 'binary':
            local0 = aux[:]
            local0.append((i, 0))
            local1 = aux[:]
            local1.append((i, 1))
        else:
            # Get all nominal values for this attribute...
            all_values = [entry[i] for entry in omega[1:]]
            for j in all_values:
                pass



def satisfies_all(desc, c):
    return True


def insert_with_priority(queue, item, priority, max_size):
    assert isinstance(queue, qu.SortedPriorityQueue)
    if len(queue) == max_size:
        queue.pop()
        queue.add(item, priority)
    else:
        queue.add(item, priority)


