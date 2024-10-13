from typing import List
import dis
import timeit


def compare_the_triple(a: List[int], b: List[int]) -> List[int]:
    """
    Doctests: pytest --doctest-modules -vvs <filename>.py
    >>> compare_the_triple([1, 2, 3], [3, 2, 1])
    [1, 1]
    >>> compare_the_triple([5, 6, 7], [3, 6, 10])
    [1, 1]
    >>> compare_the_triple([17, 28, 30], [99, 16, 8])
    [2, 1]
    """
    alice: int = 0
    bob: int = 0
    for i in range(3):
        if a[i] > b[i]:
            alice += 1
        elif a[i] < b[i]:
            bob += 1
    return [alice, bob]


def compare_the_triple_2(a: List[int], b: List[int]) -> List[int]:
    """
    Doctests: pytest --doctest-modules -vvs <filename>.py
    >>> compare_the_triple_2([1, 2, 3], [3, 2, 1])
    [1, 1]
    >>> compare_the_triple_2([5, 6, 7], [3, 6, 10])
    [1, 1]
    >>> compare_the_triple_2([17, 28, 30], [99, 16, 8])
    [2, 1]
    """
    # alice: int = sum([1 for i in zip(a, b) if a[i] > b[i]])
    # bob: int = sum([1 for i in zip(a, b) if a[i] < b[i]])
    result = [1 if x > y else -1 if x < y else 0 for x, y in zip(a, b)]
    return [result.count(1), result.count(-1)]


def compare_the_triple_3(a: List[int], b: List[int]) -> List[int]:
    """
    Doctests: pytest --doctest-modules -vvs <filename>.py
    >>> compare_the_triple_3([1, 2, 3], [3, 2, 1])
    [1, 1]
    >>> compare_the_triple_3([5, 6, 7], [3, 6, 10])
    [1, 1]
    >>> compare_the_triple_3([17, 28, 30], [99, 16, 8])
    [2, 1]
    """
    alice: int = sum([1 for x, y in zip(a, b) if x > y])
    bob: int = sum([1 for x, y in zip(a, b) if y > x])
    return [alice, bob]


# print(compare_the_triple([1, 2, 3], [3, 2, 1]))
# print(compare_the_triple_2([1, 2, 3], [3, 2, 1]))
# print(compare_the_triple_3([1, 2, 3], [3, 2, 1]))


# print(dis.dis(compare_the_triple))
# print("--------------------------------------------------")
# print(dis.dis(compare_the_triple_2))
# print("--------------------------------------------------")
# print(dis.dis(compare_the_triple_3))


# Test inputs
# a = [1, 2, 3]
# b = [3, 2, 1]

# Compare the performance of the functions using timeit
# iterations = 1000000

# time_1 = timeit.timeit(lambda: compare_the_triple(a, b), number=iterations)
# time_2 = timeit.timeit(lambda: compare_the_triple_2(a, b), number=iterations)
# time_3 = timeit.timeit(lambda: compare_the_triple_3(a, b), number=iterations)
#
# print("Time taken by compare_the_triple:", time_1)
# print("Time taken by compare_the_triple_2:", time_2)
# print("Time taken by compare_the_triple_3:", time_3)


def equal(arr: List[int]) -> int:
    """
    Calculates the minimum number of steps required to make all elements of the given array equal.
    Algorithm Explanation:
    - subtracting from one = adding to the other persons except; +1 (to all except the 4th) = -1 (from the th 4th)
    - You can get to any number, as you could add 1 (or minus 1) as many times as you want
    - We should aim for the min number, minimun does not mean the optimal, but it's between the min and min - 4
    >>> equal([2, 3, 7])
    2
    >>> equal([2, 3, 7])
    2
    >>> equal([4, 4, 4, 4])
    0
    >>> equal([1, 1, 1, 1, 1, 1])
    0
    """
    # Store all the possibilities
    possibilities = [0] * 4

    # Start with the minimum element
    minimum = min(arr)

    # range(0, 5) = [0, 1, 2, 3, 4] = (min - 0, min - 1, min - 2, min - 3, min - 4)
    for i in range(len(possibilities)):
        for k in arr:
            diff = k - minimum
            steps_required = diff // 5 + (diff % 5) // 2 + ((diff % 5) % 2) // 1
            possibilities[i] += steps_required
        minimum -= 1

    return min(possibilities)

print(equal([2, 2, 3, 7]))


def equal_2(arr: List[int]) -> int:
    """
    Calculates the minimum number of steps required to make all elements of the given array equal.
    >>> equal([2, 3, 7])
    2
    >>> equal([2, 3, 7])
    2
    >>> equal([4, 4, 4, 4])
    0
    >>> equal([1, 1, 1, 1, 1, 1])
    0
    >>> equal([9, 8, 7, 6, 5])
    5
    >>> equal([1, 2, 3, 4, 5, 6, 7, 8, 9])
    6
    >>> equal([])
    0
    """
    minimum = min(arr)

    # Calculate the difference between each element and the minimum
    # [4,3,2,1,0]
    differences = [k - minimum for k in arr]

    # Calculate the number of steps required for each possible value
    # [2, 2, 1, 1, 0]
    possibilities = [diff // 5 + (diff % 5) // 2 + (diff % 5) % 2 for diff in differences]

    # Return the minimum number of steps required
    return min(possibilities)


def cat_and_mouse(cat_a_pos: int, cat_b_pos: int, mouse_pos: int) -> str:
    """
    Determines the outcome of the cat and mouse chase.

    >>> cat_and_mouse(1, 3, 2)
    'Mouse C'
    >>> cat_and_mouse(1, 4, 2)
    'Cat A'
    >>> cat_and_mouse(4, 2, 2)
    'Cat B'
    >>> cat_and_mouse(1, 5, 5)
    'Cat B'
    >>> cat_and_mouse(2, 2, 2)
    'Mouse C'
    """
    cat_a_distance = abs(cat_a_pos - mouse_pos)
    cat_b_distance = abs(cat_b_pos - mouse_pos)

    if cat_a_distance < cat_b_distance:
        return "Cat A"
    elif cat_a_distance > cat_b_distance:
        return "Cat B"
    else:
        return "Mouse C"


def bonAppetit(bill, k, b):
    """

    """
    annaBill = sum(it for idx, it in enumerate(bill) if idx != k)

    if annaBill // 2 == b:
        print("Bon Appetit")
    else:
        print(b - annaBill // 2)

# bonAppetit([3, 10, 2, 9], 1, 12)
# bonAppetit([3, 10, 2, 9], 1, 7)
# bonAppetit([3, 10, 2, 9], 3, 10)
def compareTriplets(a, b):
    """
    a: List[int]
    b: List[int]
    return type: -> List[int]

    running Doctests using pytest: pytest --doctest-modules -vvs <filename>.py
    >>> compareTriplets([1, 2, 3], [3, 2, 1])
    [1, 1]
    >>> compareTriplets([5, 6, 7], [3, 6, 10])
    [1, 1]
    >>> compareTriplets([17, 28, 30], [99, 16, 8])
    [2, 1]
    """
    alice_total_score: int = 0
    bob_total_score: int = 0
    # zipping the two lists to produce an iterator of tuples, each contains the corrosponding elements
    # of the two lists `a` and `b`
    for alice_score, bob_score in zip(a, b):
        if alice_score > bob_score:
            alice_total_score += 1
        elif alice_score < bob_score:
            bob_total_score += 1
    return [alice_total_score, bob_total_score]

