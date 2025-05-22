#this file is for you to compare according to OS difference and python difference.
#until now no difference is raised on macos and windows, but you can test that also on linux.
#Test passed on centos on python 3.9.21
import pickle
import platform
import hashlib
import csv


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


def file_read(system_version, python_version):
    """Read hash data from a CSV file based on system and Python version."""
    filename = ""
    if system_version.lower() == "windows":
        filename = "Windows"
    elif system_version.lower() in ("macos", "mac"):
        filename = "Darwin"
    elif system_version.lower() == "linux":
        filename = "Linux"
    filename += python_version.replace('.', '') + ".csv"
    print(filename)
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        file_data = []
        for row in csv_reader:
            row_data = "".join(row)
            file_data.append(row_data)
    return file_data


def test_pickle_round_trip():
    """Test pickle serialization/deserialization and compare hash values."""
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
        filename = system + python_version.replace('.', '') + ".csv"
        with open(filename, 'w+', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows([[h] for h in hashed_data])
        print("Compare the file if you want, system version and python version.\n")
        print("For instance, input windows first, press enter, then input 3.12.3 .")
        print("If you don't want to do that, input QUIT. All uppercase.")
        system_version = input()
        print(system_version)
        if system_version == "QUIT":
            return
        python_version = input()
        print(python_version)
        if python_version == "QUIT":
            return
        file_data = file_read(system_version, python_version)
        test_cases_failed = False
        for index in range(len(file_data)):
            if file_data[index] != hashed_data[index]:
                test_cases_failed = True
                print(f"Failed for object: {test_cases[index]}")
        if not test_cases_failed:
            print("Test passed for object on different systems and different python versions.")


def main():
    test_pickle_round_trip()


if __name__ == "__main__":
    main()

