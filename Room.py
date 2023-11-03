from functools import reduce

from GuardsList import GuardsList


class Room:
    def __init__(self, number, guards: GuardsList):
        self.number = number
        self.__guards = guards

    def __repr__(self):
        return f"Room(number={self.number!r}, guards={self.__guards!r})"

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

    # Helper function to check if a guard is available
    def get_available_guards_number(self, watch_list, day, hour, days):
        return reduce(lambda acc,
                      guard: acc + (1 if guard.is_available(watch_list, day,
                                                            hour, days)
                                    else 0),
                      self.__guards, 0)
