from abc import ABC
from homework_02.exceptions import NotEnoughFuel, LowFuelError

WEIGHT_D = 1500
STARTED_D = False
FUEL_D = 70
FUEL_CONSUMPTION_D = 20


class Vehicle(ABC):

    __weight = WEIGHT_D
    __started = STARTED_D
    __fuel = FUEL_D
    __fuel_consumption = FUEL_CONSUMPTION_D

    def __init__(self, weight, fuel, fuel_consumption):
        self.__weight = weight
        self.__fuel = fuel
        self.__fuel_consumption = fuel_consumption

    def start(self):
        if not self.__started:
            if not self.__fuel > 0:
                raise LowFuelError('"No kerosene - No start"')
            self.__started = True

    #            if self.__fuel > 0:
    #                self.__started = True
    #            else:
    #                raise LowFuelError("LowFuelError")

    def move(self, distance):
        need_fuel = self.__fuel_consumption * distance
        if need_fuel > self.__fuel:
            raise NotEnoughFuel()
        else:
            self.__fuel -= need_fuel

    def set_weight(self, weight):
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def set_fuel(self, fuel):
        self.__fuel = fuel

    def get_fuel(self):
        return self.__fuel

    def set_fuel_consumption(self, fuel_consumption):
        self.__fuel_consumption = fuel_consumption

    def get_fuel_consumption(self):
        return self.__fuel_consumption

    def set_started(self, started):
        self.__started = started

    def get_started(self):
        return self.__started

    weight = property(get_weight, set_weight)
    fuel = property(get_fuel, set_fuel)
    fuel_consumption = property(get_fuel_consumption, set_fuel_consumption)
    started = property(get_started, set_started)
