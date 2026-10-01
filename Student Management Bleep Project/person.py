"""person.py - Abstract base class for the Student Management System.

Covers: Abstraction (abc module) and Encapsulation (private attributes
with validated getters/setters).
"""

from abc import ABC, abstractmethod

MIN_AGE = 15
MAX_AGE = 60


class InvalidDataError(ValueError):
    """Raised when a name, age or course value is not valid."""


def validate_name(value):
    """Return a cleaned name or raise InvalidDataError."""
    value = " ".join(str(value).split())
    if not value:
        raise InvalidDataError("Name cannot be empty.")
    if not all(ch.isalpha() or ch in " .'-" for ch in value):
        raise InvalidDataError(
            "Name can only contain letters, spaces, dots, hyphens and apostrophes.")
    return value


def validate_age(value):
    """Return age as an int or raise InvalidDataError."""
    try:
        age = int(str(value).strip())
    except ValueError:
        raise InvalidDataError("Age must be a whole number.")
    if not MIN_AGE <= age <= MAX_AGE:
        raise InvalidDataError(f"Age must be between {MIN_AGE} and {MAX_AGE}.")
    return age


class Person(ABC):
    """Abstract base class: anything with a name and an age."""

    def __init__(self, name, age):
        # Private attributes (encapsulation); setters validate the values.
        self.__name = None
        self.__age = None
        self.name = name
        self.age = age

    # ---------- getters / setters ----------
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = validate_name(value)

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = validate_age(value)

    # ---------- abstract method ----------
    @abstractmethod
    def get_details(self):
        """Return a one-line description of the person."""

    def __str__(self):
        return self.get_details()
