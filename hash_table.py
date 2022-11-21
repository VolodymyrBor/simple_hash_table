from dataclasses import dataclass
from typing import Generic, TypeVar, Hashable, Iterable

_V = TypeVar('_V')  # Value type
_K = TypeVar('_K', bound=Hashable)  # Key type


@dataclass
class _Item(Generic[_K, _V]):
    key: _K
    value: _V


class HashTable(Generic[_K, _V]):

    _INITIAL_SIZE = 4  # Initial size of hash-table
    _RESIZE_MUL = 2  # Resize multiplication

    def __init__(self, initial: dict[_K, _V] | None = None):
        self._table: list[list[_Item]] = [[] for _ in range(self._INITIAL_SIZE)]
        self._count_items = 0
        if initial:  # Fill hash-table if initial
            for key, value in initial.items():
                self._update(key, value)

    def keys(self) -> Iterable[_K]:
        """Iterable of keys"""
        for items in self._table:
            for item in items:
                yield item.key

    def values(self) -> Iterable[_V]:
        """Iterable of values"""
        for items in self._table:
            for item in items:
                yield item.value

    def items(self) -> Iterable[tuple[_K, _V]]:
        """Iterable of keys and values"""
        for items in self._table:
            for item in items:
                yield item.key, item.value

    def _update(self, key: _K, value: _V, resize: bool = True):
        """Insert or set value"""
        try:
            index, sub_index = self._find(key)
            self._table[index][sub_index].value = value
        except KeyError:
            new_item = _Item(
                key=key,
                value=value,
            )
            index = self._get_index(key)
            items = self._table[index]
            items.append(new_item)
            self._count_items += 1
            if resize:
                self._resize()

    def _get(self, key: _K) -> _V:
        """Get value"""
        index, sub_index = self._find(key)
        return self._table[index][sub_index].value

    def _delete(self, key: _K):
        """Delete value"""
        index, sub_index = self._find(key)
        del self._table[index][sub_index]
        self._count_items -= 1
        self._resize()

    def _resize(self):
        """Resize hash-table.

        Increase size to reduce the probability of collision.
        Decrease size to reduce the memory usage.

        """
        expected_size = self._count_items * self._RESIZE_MUL

        if expected_size > len(self._table):
            new_size = len(self._table) * self._RESIZE_MUL
        elif expected_size * self._RESIZE_MUL < len(self._table):
            new_size = len(self._table) // self._RESIZE_MUL
        else:
            return None

        old_table = self._table
        self._table = [[] for _ in range(new_size)]
        self._count_items = 0
        for items in old_table:
            for item in items:
                self._update(item.key, item.value, resize=False)

    def _get_index(self, key: _K) -> int:
        """Get index based hash-value of key"""
        hash_value = hash(key)
        index = hash_value % len(self._table)
        return index

    def _find(self, key: _K) -> tuple[int, int]:
        """Find index and sub-index"""
        index = self._get_index(key)
        items = self._table[index]
        for sub_index, item in enumerate(items):
            if item.key == key:
                return index, sub_index
        else:
            raise KeyError

    def __setitem__(self, key: _K, value: _V):
        self._update(key, value)

    def __getitem__(self, key: _K) -> _V:
        return self._get(key)

    def __delitem__(self, key: _K):
        self._delete(key)

    def __repr__(self):
        cls_name = type(self).__name__
        items = ', '.join(
            f'{key!r}: {value!r}'
            for key, value in self.items()
        )
        return f'{cls_name}({{{items}}})'

    def __len__(self) -> int:
        return self._count_items


if __name__ == '__main__':
    hash_table = HashTable()

    hash_table['key_1'] = 'value_1'
    hash_table['key_2'] = 'value_2'

    print(hash_table)
