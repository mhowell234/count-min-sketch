import hashlib
from typing import Any, List

from src.me.mhowell.prob.count_min_sketch import CountMinSketch


class CountMinSketchImpl(CountMinSketch):
    def __init__(self, width: int, depth: int) -> None:
        self.hash_functions: List[Any] = self._determine_hash_functions(depth)

        self.width = width
        self.depth = depth

        self.sketch: List[List[int]] = [[0 for _ in range(width)] for _ in range(depth)]

    def add(self, item):
        indices: List[int] = self._compute_indices(item)

        for i in range(self.depth):
            self.sketch[i][indices[i]] += 1

    def estimate(self, item):
        indices: List[int] = self._compute_indices(item)

        return min([self.sketch[i][indices[i]] for i in range(self.depth)])

    def remove(self, item: Any, times: int = 1) -> None:
        indices: List[int] = self._compute_indices(item)

        for i in range(self.depth):
            self.sketch[i][indices[i]] -= times

    def _compute_indices(self, item) -> List[int]:
        return [int(hash_value % self.width) for hash_value in self._compute_hashes(item)]

    def _compute_hashes(self, item) -> List[int]:
        return [int(result.hexdigest(), 16) for result in [hash_function(item.encode()) for hash_function in
                                                           self.hash_functions]]

    @staticmethod
    def _determine_hash_functions(num: int) -> List[Any]:
        hash_functions: List[Any] = CountMinSketchImpl._hash_methods()

        num_hashes_available: int = len(hash_functions)

        if num > num_hashes_available:
            raise Exception(
                f"Not enough hashes available for a depth of {num}. Specify a smaller depth of {num_hashes_available} or less")

        return hash_functions[:num]

    @staticmethod
    def _hash_methods() -> List[Any]:
        return [hashlib.md5, hashlib.sha1, hashlib.sha3_224, hashlib.sha3_256, hashlib.sha3_384, hashlib.sha3_512,
                hashlib.blake2b, hashlib.blake2s, hashlib.sha512, hashlib.sha384, hashlib.sha256, hashlib.sha224]


if __name__ == '__main__':
    import random
    import string

    count_min_sketch = CountMinSketchImpl(100, 10)

    iterations = 100000
    string_len = 7

    for i in range(iterations):
        count_min_sketch.add(''.join(random.choices(string.ascii_uppercase + string.digits, k=string_len)))
