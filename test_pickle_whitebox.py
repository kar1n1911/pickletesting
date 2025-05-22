import pickle
import io


# 自定义类用于测试 memo 和对象标识
class TestObject:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, TestObject) and self.value == other.value


# 测试 Pickler 的 memo 行为：同一对象两次序列化应复用 memo 引用
def test_memo_behavior():
    print("Test: memo behavior")
    obj = TestObject(123)
    data1 = pickle.dumps([obj, obj])  # 两次引用，应共享 memo
    data2 = pickle.dumps([TestObject(123), TestObject(123)])  # 两个值一样但非同一个引用

    print("Same instance size:", len(data1))
    print("Different instance size:", len(data2))
    assert len(data1) < len(data2), "Memoization should reduce size"


# 测试递归结构处理（Unpickler 栈是否正常清空）
def test_recursive_structure():
    print("\nTest: recursive structure")
    x = []
    x.append(x)
    try:
        data = pickle.dumps(x)
        result = pickle.loads(data)
        assert result[0] is result, "Recursive structure restored incorrectly"
        print("Recursive test passed")
    except Exception as e:
        print("Recursive test failed:", e)


# 测试大量不同对象（触发 memo 扩容）
def test_large_unique_objects():
    print("\nTest: large number of unique objects")
    try:
        data = pickle.dumps([TestObject(i) for i in range(10000)])
        print("Large object list serialized successfully")
    except Exception as e:
        print("Serialization failed:", e)


# 嵌套结构测试 Unpickler 栈的使用是否正确
def test_nested_structure():
    print("\nTest: nested structure")
    obj = {'a': [1, 2, {'b': TestObject(99)}]}
    data = pickle.dumps(obj)
    restored = pickle.loads(data)
    assert restored['a'][2]['b'].value == 99
    print("Nested structure restored successfully")


# 测试函数和 lambda 是否报错（pickle 不支持）
def test_pickle_function_lambda():
    print("\nTest: pickling function or lambda")
    def f(): return 1
    try:
        pickle.dumps(f)
        print("Function pickled (unexpected)")
    except Exception as e:
        print("Function pickling failed as expected")

    try:
        pickle.dumps(lambda x: x + 1)
        print("Lambda pickled (unexpected)")
    except Exception as e:
        print("Lambda pickling failed as expected")


# 执行所有测试
def run_all():
    test_memo_behavior()
    test_recursive_structure()
    test_large_unique_objects()
    test_nested_structure()
    test_pickle_function_lambda()


run_all()
