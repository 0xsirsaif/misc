import inspect
from pprint import pprint
import argparse
import os
import sys
import datetime
from typing import List, Dict, Optional, Any


# Module-level annotations
global_var: int
another_global: List[str] = []


# Define a sample class with various members
class SampleClass:
    class_variable = "I'm a class variable"

    def __init__(self):
        self.instance_variable = "I'm an instance variable"

    def instance_method(self):
        return "I'm an instance method"

    @classmethod
    def class_method(cls):
        return "I'm a class method"

    @staticmethod
    def static_method():
        return "I'm a static method"

    @property
    def property_method(self):
        return "I'm a property"


class DescriptorExample:
    def __get__(self, obj, objtype=None):
        return "Descriptor __get__ called"


class StaticExample:
    class_var = "I'm a class variable"
    instance_var = "I'm an instance variable"
    descriptor = DescriptorExample()

    @property
    def prop(self):
        return "I'm a property"

    def method(self):
        return "I'm a method"


def explore_getmembers():
    sample_instance = SampleClass()

    print("Class members:")
    pprint(inspect.getmembers(SampleClass))

    print("\nInstance members:")
    pprint(inspect.getmembers(sample_instance))

    print("\nMethods of the instance:")
    pprint(inspect.getmembers(sample_instance, predicate=inspect.ismethod))

    print("\nFunctions of the class:")
    pprint(inspect.getmembers(SampleClass, predicate=inspect.isfunction))

    print("\nGet a specific member:")
    print(
        inspect.getmembers(
            sample_instance,
            lambda x: x.__name__ == "instance_method"
            if hasattr(x, "__name__")
            else False,
        )
    )

    print("\nMembers of a built-in type (list):")
    pprint(inspect.getmembers(list, predicate=inspect.isbuiltin))


def explore_getmembers_static():
    static_instance = StaticExample()

    print("\nUsing getmembers() on the class:")
    pprint(inspect.getmembers(StaticExample))

    print("\nUsing getmembers_static() on the class:")
    pprint(inspect.getmembers_static(StaticExample))

    print("\nUsing getmembers() on the instance:")
    pprint(inspect.getmembers(static_instance))

    print("\nUsing getmembers_static() on the instance:")
    pprint(inspect.getmembers_static(static_instance))

    print("\nAccessing descriptor directly:")
    print(static_instance.descriptor)

    print("\nDescriptor via getmembers():")
    descriptor_via_getmembers = dict(inspect.getmembers(static_instance))["descriptor"]
    print(descriptor_via_getmembers)

    print("\nDescriptor via getmembers_static():")
    descriptor_via_static = dict(inspect.getmembers_static(static_instance))[
        "descriptor"
    ]
    print(descriptor_via_static)


def explore_getmodulename():
    file_paths = [
        "/home/user/projects/myproject/module.py",
        "/home/user/projects/myproject/__init__.py",
        "/home/user/projects/myproject/subpackage/__init__.py",
        "/home/user/projects/myproject/module.pyc",
        "/home/user/projects/myproject/script",
        "/home/user/projects/myproject/module.pyw",
        "/home/user/projects/myproject/.hidden_module.py",
    ]

    print("\nGetting module names from file paths:")
    for path in file_paths:
        module_name = inspect.getmodulename(path)
        print(f"Path: {path}")
        print(f"Module name: {module_name}")
        print()

    print("\nGetting module names from imported modules:")
    for module in [os, sys, datetime]:
        if hasattr(module, "__file__"):
            module_name = inspect.getmodulename(module.__file__)
            print(f"Module: {module.__name__}")
            print(f"File: {module.__file__}")
            print(f"getmodulename result: {module_name}")
        else:
            print(f"Module: {module.__name__}")
            print(
                "This module doesn't have a __file__ attribute (it's likely a built-in module)"
            )
            print(f"getmodulename result: {inspect.getmodulename(module.__name__)}")
        print()

    print("\nGetting module name of the current file:")
    current_file = __file__
    print(f"Current file: {current_file}")
    print(f"Module name: {inspect.getmodulename(current_file)}")


def explore_all_is():
    def is_is(x):
        return hasattr(x, "__call__") and x.__name__.startswith("is")

    all_is = [k for k, v in inspect.getmembers(inspect, predicate=is_is)]
    pprint(all_is)


def explore_signature():
    def example_function(a, b: int, c="default", *args, d, e=None, **kwargs):
        pass

    sig = inspect.signature(example_function)

    print("Function signature:")
    print(sig)

    print("\nParameters:")
    for name, param in sig.parameters.items():
        print(f"{name}:")
        print(f"  - kind: {param.kind}")
        print(
            f"  - default: {param.default if param.default is not param.empty else 'No default'}"
        )
        print(
            f"  - annotation: {param.annotation if param.annotation is not param.empty else 'No annotation'}"
        )

    print("\nBinding arguments:")
    try:
        bound_args = sig.bind(1, 2, 3, 4, 5, d=6, e=7, f=8)
        print("Bound arguments:")
        pprint(bound_args.arguments)
    except TypeError as e:
        print(f"Error binding arguments: {e}")

    print("\nBinding with too few arguments:")
    try:
        bound_args = sig.bind(1)
        print("Bound arguments:")
        pprint(bound_args.arguments)
    except TypeError as e:
        print(f"Error binding arguments: {e}")

    class ExampleClass:
        def __init__(self, x, y=10):
            pass

        def method(self, a, b=20):
            pass

    print("\nClass __init__ signature:")
    print(inspect.signature(ExampleClass))

    print("\nMethod signature:")
    print(inspect.signature(ExampleClass.method))


def explore_get_annotations():
    print("Exploring inspect.get_annotations()")

    # Function with various annotations
    def annotated_function(a: int, b: str, c: List[float] = []) -> Dict[str, Any]:
        return {"result": a + len(b) + len(c)}

    print("\n1. Function annotations:")
    pprint(inspect.get_annotations(annotated_function))

    # Class with annotated attributes and methods
    class AnnotatedClass:
        class_attr: str = "class attribute"

        def __init__(self, x: int, y: Optional[float] = None):
            self.x: int = x
            self.y: Optional[float] = y

        def method(self, z: List[str]) -> bool:
            return len(z) > 0

    print("\n2. Class annotations:")
    pprint(inspect.get_annotations(AnnotatedClass))

    print("\n3. Method annotations:")
    pprint(inspect.get_annotations(AnnotatedClass.method))

    print("\n4. Module-level annotations:")
    pprint(inspect.get_annotations(sys.modules[__name__]))

    # Demonstrate eval_str parameter
    def func_with_string_annotations(a: "int", b: "List[str]") -> "Dict[str, Any]":
        pass

    print("\n5. String annotations (eval_str=True):")
    pprint(inspect.get_annotations(func_with_string_annotations, eval_str=True))

    print("\n6. String annotations (eval_str=False):")
    pprint(inspect.get_annotations(func_with_string_annotations, eval_str=False))

    # Demonstrate getting annotations from an instance
    instance = AnnotatedClass(10)
    print("\n7. Instance method annotations:")
    pprint(inspect.get_annotations(instance.method))

    # Demonstrate behavior with no annotations
    def no_annotations(a, b, c):
        pass

    print("\n8. Function with no annotations:")
    pprint(inspect.get_annotations(no_annotations))


def main():
    parser = argparse.ArgumentParser(
        description="Explore different areas of Python's inspect module"
    )
    parser.add_argument(
        "area",
        choices=[
            "getmembers",
            "getmembers_static",
            "getmodulename",
            "isis",
            "signature",
            "annotations",
        ],
        help="The area of inspect to explore",
    )

    args = parser.parse_args()

    if args.area == "getmembers":
        explore_getmembers()
    elif args.area == "getmembers_static":
        explore_getmembers_static()
    elif args.area == "getmodulename":
        explore_getmodulename()
    elif args.area == "isis":
        explore_all_is()
    elif args.area == "signature":
        explore_signature()
    elif args.area == "annotations":
        explore_get_annotations()


if __name__ == "__main__":
    main()
