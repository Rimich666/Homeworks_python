"""
создайте класс `Car`, наследник `Vehicle`
"""
#from base import Vehicle
import homework_02.base


class Car(homework_02.base.Vehicle):
    __engine = None

    def __init__(self, *args):
        super().__init__(*args)

    def set_engine(self, engine):
        self.__engine = engine

    def get_engine(self):
        return self.__engine

    engine = property(get_engine, set_engine)
