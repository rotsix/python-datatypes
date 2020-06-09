#!/usr/bin/env python


class Cell:
    def __init__(self, value, prev=None, next=None):
        self._value = value
        self._prev = prev
        self._next = next


class LinkedList:
    def __init__(self, *values):
        self._head = self._tail = None
        list(map(self.append, values))

    def __iter__(self):
        self._current = self._head
        return self

    def __next__(self):
        if self._current == None:
            raise StopIteration
        tmp = self._current
        self._current = self._current._next
        return tmp._value

    def __repr__(self):
        values = []
        tmp = self._head
        while tmp:
            values.append(str(tmp._value))
            tmp = tmp._next
        return "[" + ", ".join(values) + "]"

    def __len__(self):
        res = 0
        i = self._head
        while i:
            res += 1
            i = i._next
        return res

    def append(self, value):
        if self._head == None:
            self._head = Cell(value)
            self._tail = self._head
            return

        tmp = Cell(value, prev=self._tail)
        self._tail._next = tmp
        self._tail = tmp

    def pop(self, index=None):
        if index == None:
            index = len(self) - 1

        if self._head == None:
            raise IndexError

        if index == 0:
            if self._head._next:
                self._head._prev = None
            self._head = self._head._next

        tmp = self._head
        for i in range(index):
            tmp = tmp._next
            if tmp == None:
                raise IndexError

        if tmp and tmp._prev:
            tmp._prev._next = tmp._next
        if tmp and tmp._next:
            tmp._next._prev = tmp._prev

    def remove(self, value):
        tmp = self._head
        while tmp:
            if tmp._value != value:
                tmp = tmp._next
                continue
            if tmp and tmp._prev:
                tmp._prev._next = tmp._next
            if tmp and tmp._next:
                tmp._next._prev = tmp._prev
            if tmp == self._head:
                self._head = self._head._next
            if tmp == self._tail:
                self._tail = self._tail._prev
            return
        else:
            raise ValueError

    def insert(self, index, value):
        if index == len(ll):
            self.append(value)
            return

        if index == 0:
            tmp = Cell(value, next=self._head)
            if self._head:
                self._head._prev = tmp
            self._head = tmp

        tmp = self._head
        for i in range(index):
            tmp = tmp._next
            if tmp == None:
                raise IndexError
        cell = Cell(value, prev=tmp._prev, next=tmp)
        if tmp and tmp._prev:
            tmp._prev._next = cell
        tmp._prev = cell


if __name__ == "__main__":
    ll = LinkedList()

    # append
    list(map(ll.append, range(5)))
    witness = list(range(5))
    assert list(ll) == witness
    print("append - OK")

    # insert
    ll.insert(3, 2.5)
    ll.insert(0, -1)
    ll.insert(len(ll), 5)
    try:
        ll.insert(666, 42)
    except IndexError:
        pass
    witness.insert(3, 2.5)
    witness.insert(0, -1)
    witness.insert(len(witness), 5)
    assert list(ll) == witness
    print("insert - OK")

    # pop
    ll.pop(4)
    ll.pop(0)
    ll.pop()
    witness.pop(4)
    witness.pop(0)
    witness.pop()
    assert list(ll) == witness
    print("pop - OK")

    # remove
    ll.remove(4)
    ll.remove(0)
    witness.remove(4)
    witness.remove(0)
    assert list(ll) == witness
    print("remove - OK")
