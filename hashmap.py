#!/usr/bin/env python

from linkedlist import LinkedList


class HashMap:
    def __init__(self, **kwargs):
        self._occupied = self._old_occupied = 0
        self._size = 2
        self._store = [None] * self._size
        self._load_factor = 0.75
        self._resizing = False

        # used to increase capacity
        self._old_size = None
        self._old_store = None
        # how many to transfer at a time
        self._resize_factor = 5

        for (k, v) in kwargs:
            self[k] = v

    def __getitem__(self, key):
        def lookup(store, size):
            index = hash(key) % size
            for (k, v) in store[index]:
                if key == k:
                    return v

        if value := lookup(self._store, self._size):
            return value
        if value := lookup(self._old_store, self._old_size):
            return value
        raise KeyError

    def __setitem__(self, key, value, transfer=False):
        if (
            self._occupied >= self._load_factor * self._size
            and not self._resizing  # already resizing
            and not transfer  # during transfer
        ):
            # resizing:
            self._occupied = 0
            # - copy the actual store
            self._old_store = self._store
            self._old_size = self._size
            # - allocate a bigger one
            self._size *= 2
            self._store = [None] * self._size
            # - start transfering
            self._resizing = True

        if not transfer:
            self._transfer()

        self._occupied += 1
        index = hash(key) % self._size
        if self._store[index]:
            for (k, v) in self._store[index]:
                if k == key:
                    self._store[index].remove((k, v))
            self._store[index].append((key, value))
        else:
            self._store[index] = LinkedList((key, value))

    def __delitem__(self, key):
        def rm(store, size):
            try:
                index = hash(key) % size
                if not store[index]:
                    return
                for (k, v) in store[index]:
                    if k == key:
                        store[index].remove((k, v))
            except ValueError:
                raise IndexError

        if self._resizing:
            rm(self._old_store, self._old_size)
        rm(self._store, self._size)
        self._occupied -= 1

    def __iter__(self):
        # TODO
        return self

    def __repr__(self):
        values = []
        if self._resizing:
            for ll in filter(bool, self._old_store):
                values += [f"{k}: {v}" for (k, v) in ll]
        for ll in filter(bool, self._store):
            values += [f"{k}: {v}" for (k, v) in ll]
        values = map(str, values)
        return "{" + ", ".join(values) + "}"

    def __contains__(self, key):
        def search(store):
            for ll in filter(bool, store):
                for (k, v) in ll:
                    if k == key:
                        return True

        return (self._old_store and search(self._old_store)) or search(self._store)

    def _transfer(self):
        if not self._resizing:
            return
        remaining = self._resize_factor
        for index, ll in enumerate(filter(bool, self._old_store)):
            if remaining == 0:
                return
            remaining -= 1
            self._old_store[index] = None
            for (k, v) in ll:
                self._occupied += 1
                index = hash(k)
                self.__setitem__(k, v, transfer=True)
        else:
            # all None, we're done transfering
            self._resizing = False
            self._old_store = None
            self._old_size = 0


if __name__ == "__main__":
    hm = HashMap()
    # add
    for i in range(7):
        hm[i] = i
    witness = {i: i for i in range(7)}
    assert dict(hm) == witness

    # update
    for i in range(5):
        hm[i] = 2 * i
    witness = {i: 2 * i for i in range(7)}
    assert dict(hm) == witness

    # remove
    for i in range(0, 7, 2):
        del hm[i]
    witness = {i: 2 * i for i in range(0, 7, 2)}
    assert dict(hm) == witness

    # contains
    assert 1 in hm
    assert 666 not in hm
