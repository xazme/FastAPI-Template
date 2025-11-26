from enum import Enum


class UserRole(str, Enum):
    LECTOR = "lector"
    STUDENT = "student"
