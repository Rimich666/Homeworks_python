"""
создайте класс `Plane`, наследник `Vehicle`
"""
from homework_02.base import Vehicle
from homework_02.exceptions import CargoOverload


class Plane(Vehicle):

    __cargo = 0

    def __init__(self, weight, fuel, fuel_consumption, max_cargo):
        self.__max_cargo = max_cargo
        super().__init__(weight, fuel, fuel_consumption)

    def load_cargo(self, loading):
        if (self.__cargo + loading) > self.__max_cargo:
            raise CargoOverload()
        else:
            self.__cargo += loading

    def remove_all_cargo(self):
        returnable = self.__cargo
        self.__cargo = 0
        return returnable

    def set_cargo(self, cargo):
        self.__cargo = cargo

    def get_cargo(self):
        return self.__cargo

    @property
    def max_cargo(self):
        return self.__max_cargo
    cargo = property(get_cargo, set_cargo)