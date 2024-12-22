from enum import Enum, unique
import random, string
from bus_schedule import ROUTE_TIME


@unique
class Status(Enum):
    PENDING = 0
    IN_WORK = 1
    LUNCH = 2
    REST = 3

@unique
class Lunch(Enum):
    BEFORE_LUNCH = 0
    DURING_LUNCH = 1
    AFTER_LUNCH = 2


class Driver:
    def __init__(self, driver_type):
        self.driver_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(3, 4)))
        self.status = Status.REST
        self.type = driver_type


class DriverA(Driver):
    def __init__(self, is_peak=False):
        super().__init__("A")
        self._work_time = 0
        self._lunch = Lunch.BEFORE_LUNCH
        self._start_lunch = 0
        self.lunch_time = 60
        self._is_peak = is_peak

    def clone(self):
        copy_driver = DriverA()
        copy_driver.driver_id = self.driver_id
        copy_driver.status = self.status
        copy_driver.type = self.type
        copy_driver._work_time = self._work_time
        copy_driver._lunch = self._lunch
        copy_driver._start_lunch = self._start_lunch
        copy_driver.lunch_time = self.lunch_time
        copy_driver._is_peak = self._is_peak
        return copy_driver

    def reset(self):
        self._work_time = 0
        self._lunch = Lunch.BEFORE_LUNCH
        self._start_lunch = 0
        self.status = Status.REST

    @property
    def is_peak(self):
        return self._is_peak

    @is_peak.setter
    def is_peak(self, value):
        self._is_peak = value

    def start_work(self):
        if self._work_time + ROUTE_TIME < 480:
            self.status = Status.PENDING

    def end_work(self):
        self.status = Status.REST
        self._work_time = 0

    @property
    def lunch(self):
        return self._lunch

    @lunch.setter
    def lunch(self, value):
        self._lunch = value

    @property
    def work_time(self):
        return self._work_time

    @work_time.setter
    def work_time(self, value):
        if self.status != Status.REST:
            self._work_time = value
            if (self._work_time >= 240 and self.status == Status.PENDING
                    and self.lunch == Lunch.BEFORE_LUNCH and self.is_peak == False):
                self._start_lunch = self._work_time
                self.lunch = Lunch.DURING_LUNCH
                self.status = Status.LUNCH
            elif (self._work_time - self._start_lunch >= self.lunch_time and self.work_time < 480
                  and self.status == Status.LUNCH):
                self.status = Status.PENDING
                self.lunch = Lunch.AFTER_LUNCH
            elif self._work_time >= 480:
                self.status = Status.REST

    def add_route_time(self):
        self.work_time += 70

    def get_status(self):
        return self.status

    def get_lunch_status(self):
        return self.lunch


class DriverB(Driver):
    def __init__(self):
        super().__init__("B")
        self._work_time = 0
        self._lunch = Lunch.BEFORE_LUNCH
        self._start_lunch = 0
        self.lunch_time = 15
        self.count_lunch = 2
        self.days_from_last_work = 2
        self.first_lunch, self.second_lunch = random.choice([120, 240]), random.choice([240, 360])

    def clone(self):
        copy_driver = DriverB()
        copy_driver.driver_id = self.driver_id
        copy_driver.status = self.status
        copy_driver.type = self.type
        copy_driver._work_time = self._work_time
        copy_driver._lunch = self._lunch
        copy_driver._start_lunch = self._start_lunch
        copy_driver.lunch_time = self.lunch_time
        copy_driver.count_lunch = self.count_lunch
        copy_driver.days_from_last_work = self.days_from_last_work
        copy_driver.first_lunch = self.first_lunch
        copy_driver.second_lunch = self.second_lunch
        return copy_driver

    def reset(self):
        self._work_time = 0
        self._lunch = Lunch.BEFORE_LUNCH
        self._start_lunch = 0
        self.status = Status.REST
        self.count_lunch = 2
        self.days_from_last_work = 2

    def start_work(self):
        if self.days_from_last_work == 2:
            self.status = Status.PENDING
        else:
            self.status = Status.REST

    def end_work(self):
        self.status = Status.REST
        self.days_from_last_work = 0
        self._work_time = 0

    def increment_rest_days(self):
        self.days_from_last_work += 1

    @property
    def work_time(self):
        return self._work_time

    @work_time.setter
    def work_time(self, value):
        if self.status != Status.REST:
            self._work_time = value
            if (self._work_time >= self.first_lunch and self.status == Status.PENDING
                    and self.count_lunch > 0):
                self._start_lunch = self._work_time
                self._lunch = Lunch.DURING_LUNCH
                self.status = Status.LUNCH
                self.count_lunch -= 1
            elif (self._work_time >= (21 * 60 - self.second_lunch)
                  and self.status == Status.PENDING and self.count_lunch > 0):
                self._start_lunch = self._work_time
                self._lunch = Lunch.DURING_LUNCH
                self.status = Status.LUNCH
                self.count_lunch -= 1
            elif self._work_time - self._start_lunch >= self.lunch_time and self.status == Status.LUNCH:
                self.status = Status.PENDING
                self._lunch = Lunch.AFTER_LUNCH

    def add_route_time(self):
        self.work_time += 70

    def get_status(self):
        return self.status

    def get_lunch_status(self):
        return self._lunch
