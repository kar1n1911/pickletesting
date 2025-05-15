import pickle,platform,pytest,hashlib,random,string,csv
import time

default_test_cases = [
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
def test_pickle_round_trip():
    # Test equivalence partitioning with various data types
    test_cases = default_test_cases
    test_cases_failed=False
    hashed_data = []
    for obj in test_cases:
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        if not deserialized == obj:
            print(f"Failed for object: {obj}")
            test_cases_failed = True
        hashed_data.append(hashlib.sha256(serialized).hexdigest())
    if test_cases_failed==False:
        print("All original tests passed, Storing All Hash256 in File")
        print(hashed_data)
        system = platform.system()
        python_version = platform.python_version()
        filename = system + python_version.replace('.','0') + ".csv"
        with open(filename, 'w+', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows(hashed_data)
        
    

def test_pickle_big_values():
    test_cases = [
        100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
        1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
        10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,
        100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    ]
    test_cases_failed=False
    serialized = pickle.dumps(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    hashed_serialized = hash(serialized)
    for obj in test_cases:
        serialized_case = pickle.dumps(obj)
        hashed_case = hash(serialized_case)
        if not hashed_case == hashed_serialized:
            test_cases_failed = True
            print(f"Failed for object: {obj}")
    if test_cases_failed==False:
        print("All big int tests passed")
    else:
        print("Big int test failed, it can handle above 128bits numbers.")

def test_case_different_type():
    int_test_case = random.randint(1,100)
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
    # Test boundary values for strings and lists
    large_string = "a" * 10**6  # 1 million characters
    serialized = pickle.dumps(large_string)
    deserialized = pickle.loads(serialized)
    assert deserialized == large_string

    large_list = list(range(10**6))  # List with 1 million elements
    serialized = pickle.dumps(large_list)
    deserialized = pickle.loads(serialized)
    assert deserialized == large_list

def test_pickle_recursive_structure():
    # Test recursive data structures
    recursive_list = []
    recursive_list.append(recursive_list)
    serialized = pickle.dumps(recursive_list)
    deserialized = pickle.loads(serialized)
    assert deserialized == recursive_list
    assert deserialized[0] is deserialized  # Check recursion integrity

def test_pickle_all_def_all_uses():
    # Test all-def and all-uses for pickle
    obj = {"key": [1, 2, 3], "nested": {"a": 1, "b": 2}}
    serialized = pickle.dumps(obj)
    deserialized = pickle.loads(serialized)
    assert deserialized == obj
    assert deserialized["key"] == [1, 2, 3]
    assert deserialized["nested"]["a"] == 1
    assert deserialized["nested"]["b"] == 2

def test_pickle_based_on_time_difference():
    test_cases = default_test_cases
    hashed_serialized_cases = []
    for obj in test_cases:
        hashed_serialized_cases.append(hashlib.sha256(pickle.dumps(obj)).hexdigest())
    time.sleep(1)
    test_cases_failed = False
    for index in range(len(test_cases)):
        if hashlib.sha256(pickle.dumps(test_cases[index])).hexdigest()!=hashed_serialized_cases[index]:
            test_cases_failed = True
            print(f"failed for object {test_cases[index]}")
    if test_cases_failed == False:
        print("Time based tests passed.")

def main():
    test_pickle_round_trip()
    test_pickle_big_values()
    test_case_different_type()
    test_pickle_based_on_time_difference()
    test_pickle_boundary_values()

if  __name__=="__main__":
    main()