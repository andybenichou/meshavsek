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
# Room file of the project Meshavshek


from datetime import datetime
from functools import reduce

from src.models.GuardsList import GuardsList


class Room:
    def __init__(self, number, guards: GuardsList, can_be_toran=True,
                 can_be_kitat_konenout=True):
        self.number = number
        self.__guards = guards
        self.can_be_toran = can_be_toran
        self.can_be_kitat_konenout = can_be_kitat_konenout

    def __repr__(self):
        return f"Room(number={self.number!r})"

    def __str__(self):
        return f"Room number {self.number}, with guards: {self.__guards}"

    def __eq__(self, other):
        if isinstance(other, Room):
            return self.number == other.number

        return False

    def __contains__(self, guard):
        return guard in self.__guards

    def __getitem__(self, index):
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

    def get_available_guards_number(self, watch_list, date: datetime):
        return reduce(lambda acc,
                      guard: acc + (1 if guard.is_available(watch_list, date,
                                                            delays_prop=[0])
                                    else 0),
                      self.__guards, 0)
