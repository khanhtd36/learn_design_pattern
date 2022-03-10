import abc
from typing import List


class Observable:

    def __init__(self):
        self._observers: List[Observer] = []
        self._changed = False

    def register_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data=None):
        if self._changed:
            for observer in self._observers:
                observer.update(self, data=data)
            self._changed = False

    def set_changed(self):
        self._changed = True

    def clear_changed(self):
        self._changed = False

    def has_changed(self):
        return self._changed


class Observer(abc.ABC):

    @abc.abstractmethod
    def update(self, observable: Observable, data=None):
        pass


class WeatherData(Observable):

    def __init__(self):
        super().__init__()
        self._temperature = -1
        self._humidity = -1
        self._pressure = -1

    def measurement_changed(self):
        self.set_changed()
        self.notify_observers()

    def set_measurements(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure

        self.measurement_changed()

    def get_temperature(self):
        return self._temperature

    def get_humidity(self):
        return self._humidity

    def get_pressure(self):
        return self._pressure


class DisplayElement(abc.ABC):

    @abc.abstractmethod
    def display(self):
        pass


class CurrentConditionDisplay(Observer, DisplayElement):

    def __init__(self, weather_data: WeatherData):
        self._temperature = -1
        self._humidity = -1

        self._weather_data = weather_data
        weather_data.register_observer(self)

    def update(self, observable, data=None):
        if isinstance(observable, WeatherData):
            self._temperature = observable.get_temperature()
            self._humidity = observable.get_humidity()
            self.display()

    def display(self):
        print(f'Current conditions: '
              f'{self._temperature}F degrees and {self._humidity} humidity')


class ForecastDisplay(Observer):

    def __init__(self, weather_data: WeatherData):
        self._current_pressure = 29.92
        self._last_pressure = -1
        self._forecast_pressure = -1

        self._weather_data = weather_data
        weather_data.register_observer(self)

    def update(self, observable, data=None):
        if isinstance(observable, WeatherData):
            self._last_pressure = self._current_pressure
            self._current_pressure = observable.get_pressure()
            self.forecast_next_pressure()
            self.display()

    def forecast_next_pressure(self):
        self._forecast_pressure = self._current_pressure + (self._current_pressure - self._last_pressure)

    def display(self):
        print(f'Forecast pressure: {self._forecast_pressure}')


if __name__ == '__main__':
    _weather_data = WeatherData()

    _current_condition_display = CurrentConditionDisplay(_weather_data)
    _forecast_display = ForecastDisplay(_weather_data)

    _weather_data.set_measurements(80, 50, 30)
    _weather_data.set_measurements(80, 40, 30)
    _weather_data.set_measurements(70, 50, 60)
