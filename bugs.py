"""
DebugArena — bugs.py
======================
The "curriculum" — a collection of buggy Python functions
with test cases. The environment randomly picks one each episode.

Each bug has:
  - buggy_code   : the broken function the agent must fix
  - correct_code : the solution (used to verify fixes)
  - tests        : list of (input, expected_output) pairs
  - category     : type of bug
  - difficulty   : easy / medium / hard
  - hint         : plain-English hint shown to the agent

Adding more bugs here = richer training data.
Judges love seeing a well-designed curriculum.
"""

BUGS = [

    # ── EASY: Logic errors ────────────────────────────────────

    {
        "id": "bug_001",
        "name": "Addition returns subtraction",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def add(a, b):
    return a - b""",
        "correct_code": """def add(a, b):
    return a + b""",
        "tests": [
            {"input": (2, 3),   "expected": 5},
            {"input": (0, 0),   "expected": 0},
            {"input": (-1, 1),  "expected": 0},
            {"input": (10, 20), "expected": 30},
        ],
        "hint": "Check the operator being used."
    },

    {
        "id": "bug_002",
        "name": "Max returns min",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def find_max(nums):
    return min(nums)""",
        "correct_code": """def find_max(nums):
    return max(nums)""",
        "tests": [
            {"input": ([1, 5, 3],),   "expected": 5},
            {"input": ([10, 2, 8],),  "expected": 10},
            {"input": ([-1, -5, -2],),"expected": -1},
        ],
        "hint": "The function name says 'max' but something else is being returned."
    },

    {
        "id": "bug_003",
        "name": "Wrong comparison operator",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def is_adult(age):
    if age < 18:
        return True
    return False""",
        "correct_code": """def is_adult(age):
    if age >= 18:
        return True
    return False""",
        "tests": [
            {"input": (18,), "expected": True},
            {"input": (17,), "expected": False},
            {"input": (25,), "expected": True},
            {"input": (0,),  "expected": False},
        ],
        "hint": "Check the comparison direction."
    },

    # ── EASY: Off-by-one errors ───────────────────────────────

    {
        "id": "bug_004",
        "name": "Range off by one",
        "category": "off_by_one",
        "difficulty": "easy",
        "buggy_code": """def sum_to_n(n):
    total = 0
    for i in range(n):
        total += i
    return total""",
        "correct_code": """def sum_to_n(n):
    total = 0
    for i in range(n + 1):
        total += i
    return total""",
        "tests": [
            {"input": (5,),  "expected": 15},
            {"input": (3,),  "expected": 6},
            {"input": (1,),  "expected": 1},
            {"input": (10,), "expected": 55},
        ],
        "hint": "range(n) goes from 0 to n-1. Should it include n?"
    },

    {
        "id": "bug_005",
        "name": "List index off by one",
        "category": "off_by_one",
        "difficulty": "easy",
        "buggy_code": """def get_last(items):
    return items[len(items)]""",
        "correct_code": """def get_last(items):
    return items[len(items) - 1]""",
        "tests": [
            {"input": ([1, 2, 3],),    "expected": 3},
            {"input": (["a", "b"],),   "expected": "b"},
            {"input": ([42],),         "expected": 42},
        ],
        "hint": "Python lists are 0-indexed. What's the index of the last element?"
    },

    # ── MEDIUM: Type errors ───────────────────────────────────

    {
        "id": "bug_006",
        "name": "String not converted to int",
        "category": "type",
        "difficulty": "medium",
        "buggy_code": """def double_number(s):
    return s * 2""",
        "correct_code": """def double_number(s):
    return int(s) * 2""",
        "tests": [
            {"input": ("5",),  "expected": 10},
            {"input": ("3",),  "expected": 6},
            {"input": ("0",),  "expected": 0},
        ],
        "hint": "The input is a string. What needs to happen before multiplying?"
    },

    {
        "id": "bug_007",
        "name": "Integer division instead of float",
        "category": "type",
        "difficulty": "medium",
        "buggy_code": """def average(nums):
    return sum(nums) // len(nums)""",
        "correct_code": """def average(nums):
    return sum(nums) / len(nums)""",
        "tests": [
            {"input": ([1, 2, 3],),    "expected": 2.0},
            {"input": ([1, 2],),       "expected": 1.5},
            {"input": ([10, 20, 30],), "expected": 20.0},
        ],
        "hint": "One operator does integer division, the other does float division."
    },

    # ── MEDIUM: Edge case bugs ────────────────────────────────

    {
        "id": "bug_008",
        "name": "No empty list handling",
        "category": "edge_case",
        "difficulty": "medium",
        "buggy_code": """def safe_divide(a, b):
    return a / b""",
        "correct_code": """def safe_divide(a, b):
    if b == 0:
        return None
    return a / b""",
        "tests": [
            {"input": (10, 2),  "expected": 5.0},
            {"input": (9, 3),   "expected": 3.0},
            {"input": (5, 0),   "expected": None},
        ],
        "hint": "What happens when the second argument is zero?"
    },

    {
        "id": "bug_009",
        "name": "Doesn't handle negative input",
        "category": "edge_case",
        "difficulty": "medium",
        "buggy_code": """def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)""",
        "correct_code": """def factorial(n):
    if n < 0:
        return None
    if n == 0:
        return 1
    return n * factorial(n - 1)""",
        "tests": [
            {"input": (5,),  "expected": 120},
            {"input": (0,),  "expected": 1},
            {"input": (3,),  "expected": 6},
            {"input": (-1,), "expected": None},
        ],
        "hint": "What should happen for negative inputs?"
    },

    # ── HARD: Logic bugs ──────────────────────────────────────

    {
        "id": "bug_010",
        "name": "Palindrome check broken",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def is_palindrome(s):
    return s == s[1:-1]""",
        "correct_code": """def is_palindrome(s):
    return s == s[::-1]""",
        "tests": [
            {"input": ("racecar",), "expected": True},
            {"input": ("hello",),  "expected": False},
            {"input": ("aba",),    "expected": True},
            {"input": ("a",),      "expected": True},
            {"input": ("ab",),     "expected": False},
        ],
        "hint": "How do you reverse a string in Python?"
    },

    {
        "id": "bug_011",
        "name": "FizzBuzz wrong order",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    elif n % 15 == 0:
        return "FizzBuzz"
    return str(n)""",
        "correct_code": """def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return str(n)""",
        "tests": [
            {"input": (15,), "expected": "FizzBuzz"},
            {"input": (3,),  "expected": "Fizz"},
            {"input": (5,),  "expected": "Buzz"},
            {"input": (7,),  "expected": "7"},
        ],
        "hint": "Order of conditions matters. Which check should come first?"
    },

    {
        "id": "bug_012",
        "name": "Binary search wrong boundary",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def binary_search(arr, target):
    left, right = 0, len(arr)
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return -1""",
        "correct_code": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
        "tests": [
            {"input": ([1,3,5,7,9], 5),  "expected": 2},
            {"input": ([1,3,5,7,9], 1),  "expected": 0},
            {"input": ([1,3,5,7,9], 9),  "expected": 4},
            {"input": ([1,3,5,7,9], 4),  "expected": -1},
        ],
        "hint": "Check the initial boundary and the loop condition."
    },

     # ── EASY: Logic ───────────────────────────────────────────
 
    {
        "id": "bug_013",
        "name": "Multiply returns addition",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def multiply(a, b):
    return a + b""",
        "correct_code": """def multiply(a, b):
    return a * b""",
        "tests": [
            {"input": (3, 4),   "expected": 12},
            {"input": (0, 5),   "expected": 0},
            {"input": (-2, 3),  "expected": -6},
            {"input": (7, 7),   "expected": 49},
        ],
        "hint": "Check the operator."
    },
 
    {
        "id": "bug_014",
        "name": "Even check uses wrong operator",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def is_even(n):
    return n % 2 == 1""",
        "correct_code": """def is_even(n):
    return n % 2 == 0""",
        "tests": [
            {"input": (4,),  "expected": True},
            {"input": (7,),  "expected": False},
            {"input": (0,),  "expected": True},
            {"input": (-2,), "expected": True},
        ],
        "hint": "What does an even number leave as remainder when divided by 2?"
    },
 
    {
        "id": "bug_015",
        "name": "Absolute value returns negative",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def absolute(n):
    if n < 0:
        return n
    return -n""",
        "correct_code": """def absolute(n):
    if n < 0:
        return -n
    return n""",
        "tests": [
            {"input": (-5,), "expected": 5},
            {"input": (3,),  "expected": 3},
            {"input": (0,),  "expected": 0},
            {"input": (-1,), "expected": 1},
        ],
        "hint": "The negation is applied to the wrong branch."
    },
 
    {
        "id": "bug_016",
        "name": "Min returns max",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def find_min(nums):
    return max(nums)""",
        "correct_code": """def find_min(nums):
    return min(nums)""",
        "tests": [
            {"input": ([3, 1, 4],),  "expected": 1},
            {"input": ([10, 2, 8],), "expected": 2},
            {"input": ([-1, -5, 0],),"expected": -5},
        ],
        "hint": "The function name says min but something else is called."
    },
 
    {
        "id": "bug_017",
        "name": "Greeting uses wrong variable",
        "category": "logic",
        "difficulty": "easy",
        "buggy_code": """def greet(name):
    greeting = "Hello"
    return greeting""",
        "correct_code": """def greet(name):
    greeting = "Hello"
    return greeting + ", " + name""",
        "tests": [
            {"input": ("Alice",), "expected": "Hello, Alice"},
            {"input": ("Bob",),   "expected": "Hello, Bob"},
            {"input": ("World",), "expected": "Hello, World"},
        ],
        "hint": "The name parameter is never used in the return."
    },
 
    # ── EASY: Off by one ─────────────────────────────────────
 
    {
        "id": "bug_018",
        "name": "Count starts at 1 instead of 0",
        "category": "off_by_one",
        "difficulty": "easy",
        "buggy_code": """def count_items(lst):
    count = 1
    for _ in lst:
        count += 1
    return count""",
        "correct_code": """def count_items(lst):
    count = 0
    for _ in lst:
        count += 1
    return count""",
        "tests": [
            {"input": ([1, 2, 3],),    "expected": 3},
            {"input": ([],),           "expected": 0},
            {"input": (["a", "b"],),   "expected": 2},
        ],
        "hint": "What should the counter start at before counting anything?"
    },
 
    {
        "id": "bug_019",
        "name": "Slice misses last element",
        "category": "off_by_one",
        "difficulty": "easy",
        "buggy_code": """def get_all_but_first(lst):
    return lst[1:len(lst)-1]""",
        "correct_code": """def get_all_but_first(lst):
    return lst[1:]""",
        "tests": [
            {"input": ([1, 2, 3, 4],), "expected": [2, 3, 4]},
            {"input": ([5, 6],),       "expected": [6]},
            {"input": ([1, 2, 3],),    "expected": [2, 3]},
        ],
        "hint": "Python slices go up to but not including the end index."
    },
 
    # ── MEDIUM: Type errors ───────────────────────────────────
 
    {
        "id": "bug_020",
        "name": "Concatenates instead of adds",
        "category": "type",
        "difficulty": "medium",
        "buggy_code": """def add_numbers(a, b):
    return str(a) + str(b)""",
        "correct_code": """def add_numbers(a, b):
    return a + b""",
        "tests": [
            {"input": (1, 2),   "expected": 3},
            {"input": (10, 20), "expected": 30},
            {"input": (0, 5),   "expected": 5},
        ],
        "hint": "Converting to string before adding joins them as text."
    },
 
    {
        "id": "bug_021",
        "name": "Returns string instead of int",
        "category": "type",
        "difficulty": "medium",
        "buggy_code": """def square(n):
    return str(n * n)""",
        "correct_code": """def square(n):
    return n * n""",
        "tests": [
            {"input": (4,),  "expected": 16},
            {"input": (3,),  "expected": 9},
            {"input": (0,),  "expected": 0},
            {"input": (-2,), "expected": 4},
        ],
        "hint": "The result should be a number, not a string."
    },
 
    {
        "id": "bug_022",
        "name": "Bool compared with wrong type",
        "category": "type",
        "difficulty": "medium",
        "buggy_code": """def is_positive(n):
    return n > "0" """,
        "correct_code": """def is_positive(n):
    return n > 0""",
        "tests": [
            {"input": (5,),  "expected": True},
            {"input": (-1,), "expected": False},
            {"input": (0,),  "expected": False},
        ],
        "hint": "Comparing a number with a string causes a TypeError."
    },
 
    # ── MEDIUM: Edge cases ────────────────────────────────────
 
    {
        "id": "bug_023",
        "name": "Empty string not handled",
        "category": "edge_case",
        "difficulty": "medium",
        "buggy_code": """def first_char(s):
    return s[0]""",
        "correct_code": """def first_char(s):
    if not s:
        return None
    return s[0]""",
        "tests": [
            {"input": ("hello",), "expected": "h"},
            {"input": ("a",),     "expected": "a"},
            {"input": ("",),      "expected": None},
        ],
        "hint": "What happens if the string is empty?"
    },
 
    {
        "id": "bug_024",
        "name": "Division ignores remainder",
        "category": "edge_case",
        "difficulty": "medium",
        "buggy_code": """def is_divisible(a, b):
    return a / b == int(a / b)""",
        "correct_code": """def is_divisible(a, b):
    if b == 0:
        return False
    return a % b == 0""",
        "tests": [
            {"input": (10, 2), "expected": True},
            {"input": (10, 3), "expected": False},
            {"input": (9, 3),  "expected": True},
            {"input": (5, 0),  "expected": False},
        ],
        "hint": "Use modulo operator. Also handle division by zero."
    },
 
    {
        "id": "bug_025",
        "name": "None input not handled",
        "category": "edge_case",
        "difficulty": "medium",
        "buggy_code": """def safe_upper(s):
    return s.upper()""",
        "correct_code": """def safe_upper(s):
    if s is None:
        return None
    return s.upper()""",
        "tests": [
            {"input": ("hello",), "expected": "HELLO"},
            {"input": ("abc",),   "expected": "ABC"},
            {"input": (None,),    "expected": None},
        ],
        "hint": "What happens when None is passed in?"
    },
 
    {
        "id": "bug_026",
        "name": "Single element list crashes",
        "category": "edge_case",
        "difficulty": "medium",
        "buggy_code": """def second_element(lst):
    return lst[1]""",
        "correct_code": """def second_element(lst):
    if len(lst) < 2:
        return None
    return lst[1]""",
        "tests": [
            {"input": ([1, 2, 3],), "expected": 2},
            {"input": ([5, 6],),    "expected": 6},
            {"input": ([1],),       "expected": None},
            {"input": ([],),        "expected": None},
        ],
        "hint": "What if the list has fewer than 2 elements?"
    },
 
    # ── MEDIUM: Logic ─────────────────────────────────────────
 
    {
        "id": "bug_027",
        "name": "AND used instead of OR",
        "category": "logic",
        "difficulty": "medium",
        "buggy_code": """def is_weekend(day):
    return day == "Saturday" and day == "Sunday" """,
        "correct_code": """def is_weekend(day):
    return day == "Saturday" or day == "Sunday" """,
        "tests": [
            {"input": ("Saturday",), "expected": True},
            {"input": ("Sunday",),   "expected": True},
            {"input": ("Monday",),   "expected": False},
            {"input": ("Friday",),   "expected": False},
        ],
        "hint": "A day cannot be both Saturday AND Sunday simultaneously."
    },
 
    {
        "id": "bug_028",
        "name": "Wrong default return value",
        "category": "logic",
        "difficulty": "medium",
        "buggy_code": """def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return True""",
        "correct_code": """def contains(lst, item):
    for x in lst:
        if x == item:
            return True
    return False""",
        "tests": [
            {"input": ([1, 2, 3], 2),  "expected": True},
            {"input": ([1, 2, 3], 5),  "expected": False},
            {"input": ([], 1),         "expected": False},
            {"input": (["a", "b"], "c"), "expected": False},
        ],
        "hint": "What should be returned when the item is not found?"
    },
 
    {
        "id": "bug_029",
        "name": "Condition is negated incorrectly",
        "category": "logic",
        "difficulty": "medium",
        "buggy_code": """def is_leap_year(year):
    return year % 4 != 0""",
        "correct_code": """def is_leap_year(year):
    return year % 4 == 0""",
        "tests": [
            {"input": (2000,), "expected": True},
            {"input": (1900,), "expected": True},
            {"input": (2023,), "expected": False},
            {"input": (2024,), "expected": True},
        ],
        "hint": "The condition is flipped. Leap years ARE divisible by 4."
    },
 
    # ── HARD: Logic ───────────────────────────────────────────
 
    {
        "id": "bug_030",
        "name": "Bubble sort never swaps",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j] = arr[j+1]
                arr[j+1] = arr[j]
    return arr""",
        "correct_code": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr""",
        "tests": [
            {"input": ([64, 34, 25, 12],), "expected": [12, 25, 34, 64]},
            {"input": ([1, 2, 3],),        "expected": [1, 2, 3]},
            {"input": ([3, 1, 2],),        "expected": [1, 2, 3]},
        ],
        "hint": "The swap overwrites a value before saving it. Use tuple swap."
    },
 
    {
        "id": "bug_031",
        "name": "String reverse uses wrong slice",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def reverse_string(s):
    return s[::2]""",
        "correct_code": """def reverse_string(s):
    return s[::-1]""",
        "tests": [
            {"input": ("hello",),   "expected": "olleh"},
            {"input": ("abcde",),   "expected": "edcba"},
            {"input": ("a",),       "expected": "a"},
            {"input": ("ab",),      "expected": "ba"},
        ],
        "hint": "The step value in the slice controls direction."
    },
 
    {
        "id": "bug_032",
        "name": "Count vowels misses uppercase",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def count_vowels(s):
    count = 0
    for c in s:
        if c in "aeiou":
            count += 1
    return count""",
        "correct_code": """def count_vowels(s):
    count = 0
    for c in s.lower():
        if c in "aeiou":
            count += 1
    return count""",
        "tests": [
            {"input": ("hello",),  "expected": 2},
            {"input": ("HELLO",),  "expected": 2},
            {"input": ("Hello",),  "expected": 2},
            {"input": ("rhythm",), "expected": 0},
        ],
        "hint": "Uppercase vowels are not being counted."
    },
 
    {
        "id": "bug_033",
        "name": "Fibonacci returns wrong base case",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 0
    return fib(n-1) + fib(n-2)""",
        "correct_code": """def fib(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)""",
        "tests": [
            {"input": (1,), "expected": 1},
            {"input": (2,), "expected": 1},
            {"input": (5,), "expected": 5},
            {"input": (7,), "expected": 13},
        ],
        "hint": "The base case for n==1 returns the wrong value."
    },
 
    {
        "id": "bug_034",
        "name": "Two sum returns wrong pair",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""",
        "correct_code": """def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []""",
        "tests": [
            {"input": ([2, 7, 11, 15], 9),  "expected": [0, 1]},
            {"input": ([3, 2, 4], 6),        "expected": [1, 2]},
            {"input": ([1, 2, 3], 10),       "expected": []},
        ],
        "hint": "j should start from i+1 to avoid using the same element twice."
    },
 
    {
        "id": "bug_035",
        "name": "List flattener only goes one level",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result""",
        "correct_code": """def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result""",
        "tests": [
            {"input": ([[1, 2], [3, 4]],),      "expected": [1, 2, 3, 4]},
            {"input": ([[1, [2, 3]], 4],),       "expected": [1, 2, 3, 4]},
            {"input": ([1, 2, 3],),              "expected": [1, 2, 3]},
        ],
        "hint": "Nested lists inside lists are not being flattened recursively."
    },
 
    # ── HARD: Algorithm bugs ──────────────────────────────────
 
    {
        "id": "bug_036",
        "name": "Prime check wrong condition",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def is_prime(n):
    if n < 2:
        return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True""",
        "correct_code": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True""",
        "tests": [
            {"input": (2,),  "expected": True},
            {"input": (7,),  "expected": True},
            {"input": (4,),  "expected": False},
            {"input": (1,),  "expected": False},
            {"input": (0,),  "expected": False},
        ],
        "hint": "Numbers less than 2 are not prime."
    },
 
    {
        "id": "bug_037",
        "name": "Stack pop on empty list crashes",
        "category": "edge_case",
        "difficulty": "hard",
        "buggy_code": """def safe_pop(stack):
    return stack.pop()""",
        "correct_code": """def safe_pop(stack):
    if not stack:
        return None
    return stack.pop()""",
        "tests": [
            {"input": ([1, 2, 3],), "expected": 3},
            {"input": ([5],),       "expected": 5},
            {"input": ([],),        "expected": None},
        ],
        "hint": "Popping from an empty list raises IndexError."
    },
 
    {
        "id": "bug_038",
        "name": "Dictionary key missing raises error",
        "category": "edge_case",
        "difficulty": "hard",
        "buggy_code": """def get_grade(grades, student):
    return grades[student]""",
        "correct_code": """def get_grade(grades, student):
    return grades.get(student, None)""",
        "tests": [
            {"input": ({"Alice": 90, "Bob": 85}, "Alice"),  "expected": 90},
            {"input": ({"Alice": 90, "Bob": 85}, "Bob"),    "expected": 85},
            {"input": ({"Alice": 90, "Bob": 85}, "Charlie"),"expected": None},
        ],
        "hint": "Direct dict access raises KeyError. Use .get() instead."
    },
 
    {
        "id": "bug_039",
        "name": "Merge sorted lists skips elements",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    return result""",
        "correct_code": """def merge_sorted(a, b):
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result""",
        "tests": [
            {"input": ([1, 3, 5], [2, 4, 6]), "expected": [1, 2, 3, 4, 5, 6]},
            {"input": ([1, 2], [3, 4]),        "expected": [1, 2, 3, 4]},
            {"input": ([], [1, 2]),            "expected": [1, 2]},
        ],
        "hint": "Remaining elements after the loop are never added."
    },
 
    {
        "id": "bug_040",
        "name": "Capitalize only first letter broken",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def capitalize_words(s):
    return s.title().lower()""",
        "correct_code": """def capitalize_words(s):
    return s.title()""",
        "tests": [
            {"input": ("hello world",),    "expected": "Hello World"},
            {"input": ("python is fun",),  "expected": "Python Is Fun"},
            {"input": ("a b c",),          "expected": "A B C"},
        ],
        "hint": "Something is undoing the capitalization after it's applied."
    },
 
    {
        "id": "bug_041",
        "name": "GCD uses subtraction instead of modulo",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def gcd(a, b):
    while b:
        a = b
        b = a - b
    return a""",
        "correct_code": """def gcd(a, b):
    while b:
        a, b = b, a % b
    return a""",
        "tests": [
            {"input": (48, 18), "expected": 6},
            {"input": (100, 75),"expected": 25},
            {"input": (7, 3),   "expected": 1},
            {"input": (12, 4),  "expected": 4},
        ],
        "hint": "GCD uses the modulo operation, not subtraction. Also watch the variable update order."
    },
 
    {
        "id": "bug_042",
        "name": "Anagram check ignores spaces",
        "category": "logic",
        "difficulty": "hard",
        "buggy_code": """def is_anagram(s1, s2):
    return sorted(s1) == sorted(s2)""",
        "correct_code": """def is_anagram(s1, s2):
    s1 = s1.replace(" ", "").lower()
    s2 = s2.replace(" ", "").lower()
    return sorted(s1) == sorted(s2)""",
        "tests": [
            {"input": ("listen", "silent"),       "expected": True},
            {"input": ("hello", "world"),         "expected": False},
            {"input": ("Astronomer", "Moon starer"), "expected": True},
            {"input": ("abc", "cab"),             "expected": True},
        ],
        "hint": "Spaces and case differences are not being handled."
    },

]


def get_bug_by_id(bug_id: str):
    for bug in BUGS:
        if bug["id"] == bug_id:
            return bug
    return None


def get_bugs_by_difficulty(difficulty: str):
    return [b for b in BUGS if b["difficulty"] == difficulty]


def get_all_ids():
    return [b["id"] for b in BUGS]
