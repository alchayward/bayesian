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
