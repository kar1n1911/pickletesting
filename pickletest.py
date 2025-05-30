import csv
import hashlib
import pickle
import platform
import random
import time

import pickle_module_function1



DEFAULT_TEST_CASES = [
    42,  # Integer
    3.14,  # Float
    "hello",  # String
    "42",
    [1, 2, 3],  # List
    {"key": "value"},  # Dictionary
    (1, 2, 3),  # Tuple
    {1, 2, 3},  # Set
    None,  # NoneType
    True,  # Boolean
]


class CustomClass:
    pass


def test_pickle_round_trip():
    """Test equivalence partitioning with various data types."""
    test_cases = DEFAULT_TEST_CASES
    test_cases_failed = False
    hashed_data = []
    for obj in test_cases:
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        if deserialized != obj:
            print(f"Failed for object: {obj}")
            test_cases_failed = True
        hashed_data.append(hashlib.sha256(serialized).hexdigest())
    if not test_cases_failed:
        print("All original tests passed, Storing All Hash256 in File")
        print(hashed_data)
        system = platform.system()
        python_version = platform.python_version()
        filename = f"{system}{python_version.replace('.', '')}.csv"
        with open(filename, 'w+', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows([[h] for h in hashed_data])


def test_pickle_float_values():
    test_cases = [
        3.10000000000000000000004,
        3.100000000000000000000004,
        3.1000000000000000000000004,
        3.10000000000000000000000004
    ]
    test_cases_failed = []
    serialized = pickle.dumps(3.1)
    hashed_serialized = hashlib.sha256(serialized).hexdigest()
    for obj in test_cases:
        serialized_case = pickle.dumps(obj)
        hashed_case = hashlib.sha256(serialized_case).hexdigest()
        if hashed_case != hashed_serialized:
            test_cases_failed.append(obj)
            print(f"Failed for object: {obj}")
    if not test_cases_failed:
        print("All float tests passed")
        zeros_determination()
    else:
        print("Float test failed, it can handle these numbers.")


def zeros_determination():
    """Determine how many zeros would affect the outcome of the dump."""
    serialized = pickle.dumps(3.1)
    test_case = 3.104
    hashed_serialized = hashlib.sha256(serialized).hexdigest()
    zeros = "0"
    while hashed_serialized != hashlib.sha256(pickle.dumps(test_case)).hexdigest():
        zeros += "0"
        test_case = float("3.1" + zeros + "4")
    print(
        f"test passed with {len(zeros)} zeros, it can't handle more due to the precision problem of float class."
    )


def test_pickle_big_values():
    test_cases = [
        10**98,
        10**99,
        10**100,
        10**101
    ]
    test_cases_failed = False
    serialized = pickle.dumps(10**97)
    hashed_serialized = hash(serialized)
    for obj in test_cases:
        serialized_case = pickle.dumps(obj)
        hashed_case = hash(serialized_case)
        if hashed_case != hashed_serialized:
            test_cases_failed = True
            print(f"Failed for object: {obj}")
    if not test_cases_failed:
        print("All big int tests passed")
    else:
        print("Big int test failed, it can handle above 128bits numbers.")


def test_case_different_type():
    int_test_case = random.randint(1, 100)
    str_test_case = str(int_test_case)
    serialized_int = pickle.dumps(int_test_case)
    serialized_str = pickle.dumps(str_test_case)
    hashed_int = hashlib.sha256(serialized_int).hexdigest()
    hashed_str = hashlib.sha256(serialized_str).hexdigest()
    if hashed_int != hashed_str:
        print("Different types value different")
        print(hashed_int)
        print(hashed_str)
    else:
        print("Different types value same")


def test_pickle_boundary_values():
    """Test boundary values for strings and lists."""
    large_string = "a" * 10**6  # 1 million characters
    serialized = pickle.dumps(large_string)
    deserialized = pickle.loads(serialized)
    assert deserialized == large_string

    large_list = list(range(10**6))  # List with 1 million elements
    serialized = pickle.dumps(large_list)
    deserialized = pickle.loads(serialized)
    assert deserialized == large_list


def test_pickle_recursive_structure():
    """Test recursive data structures."""
    recursive_list = []
    recursive_list.append(recursive_list)
    serialized = pickle.dumps(recursive_list)
    deserialized = pickle.loads(serialized)
    assert deserialized == recursive_list
    assert deserialized[0] is deserialized  # Check recursion integrity


def test_pickle_all_def_all_uses():
    """Test all-def and all-uses for pickle."""
    obj = {"key": [1, 2, 3], "nested": {"a": 1, "b": 2}}
    serialized = pickle.dumps(obj)
    deserialized = pickle.loads(serialized)
    assert deserialized == obj
    assert deserialized["key"] == [1, 2, 3]
    assert deserialized["nested"]["a"] == 1
    assert deserialized["nested"]["b"] == 2


def test_pickle_based_on_time_difference():
    test_cases = DEFAULT_TEST_CASES
    hashed_serialized_cases = [
        hashlib.sha256(pickle.dumps(obj)).hexdigest() for obj in test_cases
    ]
    time.sleep(1)
    test_cases_failed = False
    for index, obj in enumerate(test_cases):
        if hashlib.sha256(pickle.dumps(obj)).hexdigest() != hashed_serialized_cases[index]:
            test_cases_failed = True
            print(f"failed for object {obj}")
    if not test_cases_failed:
        print("Time based tests passed.")


def test_function1():
    print("helloworld")


def test_function2():
    print("helloworld")


def test_pickle_function_values():
    hash_function_1 = hashlib.sha256(pickle.dumps(test_function1)).hexdigest()
    hash_function_2 = hashlib.sha256(pickle.dumps(test_function2)).hexdigest()
    time.sleep(1)
    hash_delayed_function_1 = hashlib.sha256(pickle.dumps(test_function1)).hexdigest()
    hash_delayed_function_2 = hashlib.sha256(pickle.dumps(test_function2)).hexdigest()
    if hash_function_1 != hash_function_2:
        print("Test failed with functions with different names and the same content")
    if hash_function_1 != hash_delayed_function_1 or hash_function_2 != hash_delayed_function_2:
        print("Test failed with functions with different time")
    # no output is the ideal output!


def test_pickle_function_different_class_same_name_same_content_different_package():
    hash_function_1 = hashlib.sha256(pickle.dumps(test_function1)).hexdigest()
    hash_function_2 = hashlib.sha256(
        pickle.dumps(pickle_module_function1.test_function1)
    ).hexdigest()
    if hash_function_1 != hash_function_2:
        print("Test failed with functions with same names and the same content but different packages")


def test_pickle_function_empty_objects():
    a = object()
    b = object()
    hash_1 = hashlib.sha256(pickle.dumps(a)).hexdigest()
    hash_2 = hashlib.sha256(pickle.dumps(a)).hexdigest()
    print(a == b)
    if hash_1 != hash_2:
        print("Test Failed")
    else:
        print("test passed")
    # The hash would be the same while a==b output False.


def test_pickle_function_custom_classes():
    a = CustomClass()
    b = CustomClass()
    a.x = 1
    b.y = 2
    a.y = 2
    b.x = 1
    hash_1 = hashlib.sha256(pickle.dumps(a)).hexdigest()
    hash_2 = hashlib.sha256(pickle.dumps(a)).hexdigest()
    print(a == b)
    if hash_1 != hash_2:
        print("Test Failed")
    else:
        print("test passed")
    # which is also a test passed.


def main(): 
    test_pickle_round_trip()
    test_pickle_float_values()
    test_pickle_big_values()
    test_case_different_type()
    test_pickle_boundary_values()
    test_pickle_based_on_time_difference()
    test_pickle_function_values()
    test_pickle_function_different_class_same_name_same_content_different_package()
    test_pickle_function_empty_objects()
    test_pickle_function_custom_classes()


if __name__ == "__main__":
    main()

