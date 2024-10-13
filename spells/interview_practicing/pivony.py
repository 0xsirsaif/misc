from typing import Dict, Optional
from collections import Counter


def binary_search(nums: list[int], target: int) -> int:
    """
    - O(log n) time complexity

    to run the doctest: pytest --doctest-modules -vvs <filename.py>

    >>> binary_search([1,2,3,,4,5,6,7,8,9,10], 5)
    4
    >>> binary_search([1,2,3,,4,5,6,7,8,9,10], 11)
    -1
    >>> binary_search([1,2,3,,4,5,6,7,8,9,10], 1)
    0
    >>> binary_search([1,2,3,,4,5,6,7,8,9,10], 10)
    9
    """
    left: int = 0
    right: int = len(nums) - 1

    while left <= right:
        mid: int = (right + left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def recursive_binary_search(nums: list[int], target: int, left: int, right: int) -> int:
    if left > right:
        return -1

    mid = (left + right) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        return recursive_binary_search(nums, target, mid + 1, right)
    else:
        return recursive_binary_search(nums, target, left, mid - 1)


def is_anagram(s: str, t: str) -> bool:
    """
    The key solution is counting frequencies of letters in both strings.
    method 1: create a counting dict for each string by looping over them.
    method 2: using the Counter class from collections.
    """
    if len(s) != len(t):
        return False

    s_dict: Dict[str, int] = {}
    t_dict: Dict[str: int] = {}

    for s_char in s:
        s_dict[s_char] = s_dict.get(s_char, 0) + 1

    for t_char in t:
        t_dict[t_char] = t_dict.get(t_char, 0) + 1

    return True if s_dict == t_dict else False


def is_anagram_2(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    s_counter = Counter(s)
    t_counter = Counter(t)

    return True if s_counter == t_counter else False


def invert_binary_tree_recursively(tree: list):
    if not tree:
        return []

    tree[1], tree[2] = tree[2], tree[1]

    invert_binary_tree_recursively(tree[1])
    invert_binary_tree_recursively(tree[2])


def invert_binary_tree_iterative(tree: list) -> list:
    """
    if we represent the binary tree as a 1-d list, then for each node at index i,
    its childs would reside at (2*i+1) and (2*i+2)
    """
    # empty tree
    if not tree:
        return []

    for idx in range(len(tree) // 2):
        left_child_idx = 2 * idx + 1
        right_child_idx = 2 * idx + 2
        tree[left_child_idx], tree[right_child_idx] = tree[right_child_idx], tree[left_child_idx]

    return tree


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __iter__(self):
        _list = [self.val]
        if self.left:
            _list.extend(self.left.__iter__())
        if self.right:
            _list.extend(self.right.__iter__())
        yield _list


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root:
            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
            return root
        # base condition
        return None


def is_palindrome(s: str) -> bool:
    cleaned_s: str = "".join([char.lower() for char in s if char.isalnum()])
    return cleaned_s == cleaned_s[::-1]


def find_max_profit(prices):
    if not prices:
        return 0

    max_profit = 0
    buy_price = prices[0]

    for sell_price in prices[1:]:
        if sell_price > buy_price:
            profit = sell_price - buy_price
            max_profit = max(max_profit, profit)
        else:
            buy_price = sell_price

    return max_profit


def can_construct(ransomNote: str, magazine: str) -> bool:
    if len(ransomNote) > len(magazine):
        return False

    ransom_note_counter = Counter(ransomNote)
    magazine_counter = Counter(magazine)

    for char, count in ransom_note_counter.items():
        if magazine_counter[char] < count:
            return False

    return True



if __name__ == "__main__":
    print("Hello!")

