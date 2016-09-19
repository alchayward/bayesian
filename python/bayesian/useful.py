import collections
import multiprocessing


def unique_pairs(l, equ_fn=(lambda x, y: x == y)):
    # type: (iterable, (object, object) -> bool ) -> list

    pairs = []

    def pair_cmp(p1, p2):
        return (equ_fn(p1[0], p2[0]) and equ_fn(p1[1], p2[1])) or \
               (equ_fn(p1[0], p2[1]) and equ_fn(p1[1], p2[0]))

    for p in l:
        if not any(map(lambda x: pair_cmp(x, p), pairs)):
            pairs.append(p)
    return pairs


def parfun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        q_out.put((i, f(x)))


def parmap(f, x, n_procs=multiprocessing.cpu_count()):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [multiprocessing.Process(target=parfun, args=(f, q_in, q_out)) for _ in range(n_procs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(x)]
    [q_in.put((None, None)) for _ in range(n_procs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


def really_iterable(x):
    return not isinstance(x, basestring) and isinstance(x, collections.Iterable)


def string_iterable(x):
    # type: (object) -> bool
    if isinstance(x, basestring):
        return not x.__len__() == 1
    else:
        return isinstance(x, collections.Iterable)


def flatten(l, iter_check_fn=really_iterable):
    # type: (iterable, (object -> bool) ) -> iterator
    """returns a generator which flattens out list of sublists, or any sub iterator.
        should work for all types of iterators, except for strings.
        it's recursive, so can blow out the stack if a deep structure is passed in"""
    if not iter_check_fn(l):
        yield l
        raise StopIteration
    else:
        it = iter(l)
        g = flatten(it.next(), iter_check_fn=iter_check_fn)
        while True:
            try:
                yield g.next()
            except StopIteration:
                g = flatten(it.next(), iter_check_fn=iter_check_fn)
