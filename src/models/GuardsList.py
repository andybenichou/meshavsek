# Copyright (c) 2023, Andy Benichou
# All rights reserved.
#
# This file is part of a software project governed by the Custom License
# for Private Use.
# Redistribution and use in source and binary forms, with or
# without modification, are not permitted for any non-commercial or
# commercial purposes without prior written permission from the owner.
#
# This software is provided "as is", without warranty of any kind,
# express or implied.
# In no event shall the authors be liable for any claim, damages,
# or other liability.
#
# For full license terms, see the LICENSE file in the project root
# or contact Andy Benichou.
#
# GuardsList file of the project Meshavshek


from copy import deepcopy
from typing import Union

from src.models.Guard import Guard


class GuardsList:
    __current_guard: Guard = None

    def __init__(self, guards: [Guard] = None):
        if guards:
            filtered_guards = [g for g in guards if g]
        else:
            filtered_guards = list()

        for g in filtered_guards:
            if not isinstance(g, Guard):
                raise TypeError("Initial guards list must be only composed of Guard objects")

        self.__guards = filtered_guards

    def __repr__(self):
        return f"GuardList(guards={self.__guards!r})"

    def __str__(self):
        return ', '.join([str(guard) for guard in self.__guards])

    def __contains__(self, guard):
        if isinstance(guard, Guard):
            return guard in self.__guards
        elif isinstance(guard, str):
            return guard in [str(g) for g in self.__guards]
        else:
            raise TypeError("Guard must be a Guard object or a string")

    def __getitem__(self, index):
        if isinstance(index, slice):
            return GuardsList(self.__guards[index])
        else:
            return self.__guards[index]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.__guards):
            result = self.__guards[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        return len(self.__guards)

    def __add__(self, other):
        if isinstance(other, GuardsList):
            return GuardsList(self.__guards + other.__guards)
        else:
            raise TypeError("Unsupported operand type for +: '{}'".format(type(other)))

    def __copy__(self):
        # We create a new GuardsList instance with a shallow copy of the guards list
        return GuardsList(self.__guards[:])

    def __deepcopy__(self, memo=None):
        # Create a new GuardsList instance with an empty list to avoid recursive deepcopy calls
        new_guards_list = GuardsList()

        # Add the new instance to the memo dictionary
        memo = memo or {}
        memo[id(self)] = new_guards_list

        # Now manually deepcopy each guard, which will handle guards' internal deep attributes
        new_guards_list.__guards = [deepcopy(guard, memo) for guard in self.__guards]

        # Deep copy any other attributes that need it
        new_guards_list.__current_guard = deepcopy(self.__current_guard, memo) if self.__current_guard else None

        return new_guards_list

    def find(self, guard: Union[Guard, str]) -> Union[Guard, None]:
        if not guard:
            return None

        if isinstance(guard, Guard) or isinstance(guard, str):
            for g in self.__guards:
                if g == guard:
                    return g
        else:
            raise TypeError("Guard must be a Guard object or a string")

        return None

    def append(self, guard: Guard):
        if not isinstance(guard, Guard):
            raise TypeError("Guard must be a Guard object")

        if guard and not self.__contains__(guard):
            self.__guards.append(guard)

    def extend(self, guards: [Guard]):
        for guard in guards:
            if not isinstance(guard, Guard):
                raise TypeError("Guard must be a Guard object")

            self.append(guard)

    def remove(self, guard):
        if isinstance(guard, Guard) or isinstance(guard, str):
            if guard in self.__guards:
                self.__guards.remove(guard)
        else:
            raise TypeError("Guard must be a Guard object or a string")

    def index(self, guard):
        if isinstance(guard, Guard) or isinstance(guard, str):
            if self.__contains__(guard):
                i = 0
                while i < len(self.__guards):
                    if self.__guards[i] == guard:
                        return i
                    i += 1
            else:
                raise ValueError("Guard not in list")
        else:
            raise TypeError("Guard must be a Guard object or a string")

    def get_current_guard(self):
        return self.__current_guard

    def set_current_guard(self, new_guard):
        self.__current_guard = new_guard

    def sort(self):
        self.__guards.sort(key=lambda guard: (guard.last_name, guard.first_name))
