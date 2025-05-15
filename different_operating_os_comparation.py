#this file is for you to compare according to OS difference and python difference.
#until now no difference is raised on macos and windows, but you can test that also on linux.
import pickle,platform,pytest,hashlib,random,string,csv

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
        filename = system + python_version.replace('.','') + ".csv"
        with open(filename, 'w+', newline='', encoding='utf-8') as file:
            csv.writer(file).writerows(hashed_data)
        print("Compare the file if you want, system version and python version.\n")
        print("For instance, input windows first and then input 3.12.3 .")
        print("If you don't want to do that, input QUIT. All uppercase.")
        system_version = ""
        python_version = ""
        system_version = input()
        print(system_version)
        if system_version=="QUIT":
            return
        python_version = input()
        print(python_version)
        if python_version=="QUIT":
            return
        file_data = file_read(system_version,python_version)
        test_cases_failed = False
        for index in range(len(file_data)):
            if file_data[index]!=hashed_data[index]:
                test_cases_failed = True
                print(f"Failed for object: {test_cases[index]}")
        if test_cases_failed == False:
            print("Test passed for object on different systems and different python versions.")
        
        
def file_read(system_version,python_version):
    #this is to compare the file you want with your computer version.
    #also you can write your own to compare what you like. No restraint, feel free to do so.
    Filename = ""
    if system_version=="Windows" or system_version == "windows":
        Filename = "Windows"
    elif system_version == "macos" or system_version == "mac" or system_version == "Macos":
        Filename = "Darwin"
    elif system_version == "Linux" or system_version == "linux" :#add your own linux version if you want, centos etc.
        Filename = "Linux"
    Filename = Filename + python_version.replace('.','') + ".csv"
    print(Filename)
    csv_reader = csv.reader(open(Filename))
    file_data = []
    for row in csv_reader:
        row_data = ""
        for bits in row:
            row_data = row_data + bits
        file_data.append(row_data)
    return file_data

def main():
    test_pickle_round_trip()


if __name__=="__main__":
    main()