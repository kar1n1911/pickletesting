# Final Report: Stability and Correctness of Python's `pickle` Module

## Team Members and Contributions

- **Xiuyu Dong**: Lead Researcher – Designed test suite.
- **Tianzhuo Wu**: Develeoper - White-box testing code implementation and documentation.

## 1. Introduction

The `pickle` module in Python is widely used for serializing and deserializing Python objects. However, its determinism—whether identical inputs always produce identical serialized outputs—has been a topic of discussion. This report investigates the stability and correctness of `pickle`, focusing on whether identical inputs consistently yield identical serialized outputs across different environments and conditions.

According to it's own document, `pickle` module is not secure as it will execute arbitrary code during unpickling.

Durting realworld conditions, the `pickle` module would be used (by its own words) pickling and unpickling. Which is a serializing and deserializing process which is similar to what would be known as `json`, what is the difference except for the safety concerns is that after serialization, `pickle` would generate the content that is not human-readable, while the `json` would generate what human can read.

Using bandit do detect the vulnerability of the `pickle` , stats as follows.

![TestResults](./Screenshot 2025-05-22 at 10.51.48 PM.png)

![Screenshot 2025-05-22 at 10.51.38 PM](./Screenshot 2025-05-22 at 10.51.38 PM.png)

![Screenshot 2025-05-22 at 10.51.32 PM](./Screenshot 2025-05-22 at 10.51.32 PM.png)

![Screenshot 2025-05-22 at 10.51.24 PM](./Screenshot 2025-05-22 at 10.51.24 PM.png)

![Screenshot 2025-05-22 at 10.51.16 PM](./Screenshot 2025-05-22 at 10.51.16 PM.png)

## 2. Test Suite Design

### 2.1. Testing Techniques Applied

- **Equivalence Partitioning**: Categorized inputs into distinct classes to ensure comprehensive coverage.
- **Boundary Value Analysis**: Tested edge cases such as empty objects and deeply nested structures.
- **Fuzz Testing**: Introduced random variations to inputs to identify potential inconsistencies.

### 2.2. Test Cases

The test suite included the following categories:

- **Primitive Data Types**: Integers, floats, strings, booleans.

- **Collections**: Lists, tuples, sets, dictionaries.

- **Custom Classes**: User-defined classes with various attributes.

- **Recursive Structures**: Objects containing references to themselves.

- **Cross-Version Serialization**: Objects serialized in one Python version and deserialized in another.

- **Cross-Platform Serialization**: Objects serialized on one operating system and deserialized on another.

- Big Ints and long floats: Integars which bigger than the int class, float which need more precision than the float class.

  #### 3. Traceability Matrix

| Requirement ID | Test Case ID | Description                           | Status    |
| -------------- | ------------ | ------------------------------------- | --------- |
| R1             | TC1          | Serialization of integers             | Passed    |
| R2             | TC2          | Serialization of strings              | Passed    |
| R3             | TC3          | Serialization of user-defined classes | Passed(?) |
| R4             | TC4          | Serialization of recursive structures | Failed    |
| R5             | TC5          | Cross-version serialization           | Passed    |
| R6             | TC6          | Cross-platform serialization          | Passed    |
| R7             | TC7          | Same content with different types     | Failed    |
| R8             | TC8          | Empty Object                          | Passed(?) |

## 4. Findings

- **Primitive Data Types**: Serialization of basic data types (integers, strings, etc.) was deterministic and consistent across environments.
- **Recursive Structures**: Serialization of recursive structures was consistent, but issues arose when combined with custom classes.
- **Cross-Version Serialization**: Objects serialized in one Python version and deserialized in another often resulted in errors or inconsistencies due to changes in the `pickle` protocol.
- **Cross-Platform Serialization**: Serialization across different operating systems led to discrepancies, likely due to differences in object memory layouts and internal representations.
- When it comes to the Empty Object and Custom classes, it is interesting that the python output false while pickle output true.

## 5. Discussion

### 5.1. Reasons for Non-Determinism

Factors might contribute to the non-deterministic behavior of `pickle`:

- **Object Memory Addresses**: The memory address of an object can vary between sessions, affecting its serialized representation.
- **Internal State Variations**: Differences in internal states, such as reference counts or object IDs, can lead to different serialized outputs.

### 5.2. Limitations of the Test Suite

- **Scope**: The test suite focused on a subset of Python's data types and structures; other types may exhibit different behaviors.
- **Environment Variability**: Differences in hardware and Python configurations were not exhaustively tested.
- **Complexity of Objects**: Highly complex or non-standard objects were not included in the test suite.

## 6. Recommendations

- **Use Alternative Serialization Formats**: For applications requiring deterministic serialization, consider using formats like JSON or Protocol Buffers, which are designed for portability and consistency.
- **Avoid Pickling Functions**: Functions and lambdas are not reliably serializable with `pickle` and may lead to inconsistencies.

## 7. Conclusion

The `pickle` module does not guarantee deterministic serialization across different environments and conditions. While it is suitable for short-term storage and inter-process communication within controlled environments.

## 8. References

- Python 3.12.7 Documentation: pickle — Python object serialization
- Stack Overflow Discussion on Pickle Determinism

## 9. Repository

The source code for the test suite and additional documentation can be found in the following repository:

[GitHub Repository Link](https://github.com/kar1n1911/pickletesting)
