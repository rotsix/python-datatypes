#!/usr/bin/env python


class AlreadyExistsError(Exception):
    pass


class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self._value = value
        self._left = left
        self._right = right

    def __contains__(self, value):
        if value < self._value:
            return self._left and value in self._left
        if value > self._value:
            return self._right and value in self._right
        return True

    def __repr__(self):
        res = ""
        if self._left:
            res += str(self._left) + ", "
        res += str(self._value)
        if self._right:
            res += ", " + str(self._right)
        return res

    def __iter__(self):
        return self

    def __next__(self):
        if self._left:
            yield from self._left
        yield self._value
        if self._right:
            yield from self._right
        raise StopIteration

    def insert(self, value):
        if self._value == value:
            raise AlreadyExistsError
        if value < self._value:
            if not self._left:
                self._left = BinaryTree(value)
            elif self._left._value < value:
                tmp = self._left
                self._left = BinaryTree(value, left=tmp)
            else:
                self._left.insert(value)
        if value > self._value:
            if not self._right:
                self._right = BinaryTree(value)
            elif self._right._value > value:
                tmp = self._right
                self._right = BinaryTree(value, right=tmp)
            else:
                self._right.insert(value)

    def remove(self, value):
        pass


if __name__ == "__main__":
    bt = BinaryTree(5)
    # insert
    bt.insert(9)
    bt.insert(3)
    bt.insert(7)
    bt.insert(2)
    bt.insert(6)
    bt.insert(4)
    bt.insert(8)
    bt.insert(1)
    bt.insert(0)
    witness = list(range(10))
    assert list(bt) == witness
