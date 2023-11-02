from Guard import Guard


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
        return ', '.join([guard.name for guard in self.__guards])

    def __contains__(self, guard):
        if isinstance(guard, Guard):
            guard_name = guard.name
        elif isinstance(guard, str):
            guard_name = guard
        else:
            raise TypeError("Guard must be a Guard object or a string")

        return guard_name in [g.name for g in self.__guards]

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

    def find(self, guard):
        if not guard:
            return None

        if isinstance(guard, Guard):
            guard_name = guard.name
        elif isinstance(guard, str):
            guard_name = guard
        else:
            raise TypeError("Guard must be a Guard object or a string")

        for g in self.__guards:
            if g.name == guard_name:
                return g
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
        if isinstance(guard, Guard):
            guard_name = guard.name
        elif isinstance(guard, str):
            guard_name = guard
        else:
            raise TypeError("Guard must be a Guard object or a string")

        guard_obj = None
        for g in self.__guards:
            if g.name == guard_name:
                guard_obj = g

        if not guard_obj:
            return

        self.__guards.remove(guard_obj)

    def index(self, guard):
        if isinstance(guard, Guard):
            guard_name = guard.name
        elif isinstance(guard, str):
            guard_name = guard
        else:
            raise TypeError("Guard must be a Guard object or a string")

        if self.__contains__(guard_name):
            i = 0
            while i < len(self.__guards):
                if self.__guards[i].name == guard_name:
                    return i
                i += 1
        else:
            raise ValueError("Guard not in list")

    def get_current_guard(self):
        return self.__current_guard

    def set_current_guard(self, new_guard):
        self.__current_guard = new_guard

    def sort(self):
        self.__guards.sort(key=lambda guard: guard.name)
