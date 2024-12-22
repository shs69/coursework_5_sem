import random
from dotenv import load_dotenv
from driver import DriverA, DriverB, Status
import os, ast
from bus_schedule import BusSchedule
load_dotenv()

class BusStation:
    def __init__(self):
        self.fitness = 0
        self.num_buses = int(os.getenv("NUM_BUSES"))
        self.pass_count = int(os.getenv("PASSENGERS_PER_WEEK"))
        self.route_time = int(os.getenv("ROUTE_TIME"))
        self.bus_capacity = int(os.getenv("BUS_CAPACITY"))
        self.peak_hours = ast.literal_eval(os.getenv("PEAK_HOURS"))
        self.drivers = [random.choice([DriverA(), DriverB()]) for _ in range(self.num_buses)]
        self.pass_default = self.pass_count // (17 * 70) * 3
        self.pass_peak = self.pass_count // (4 * 70) * 7
        self.schedule = BusSchedule()
        self.generate_schedule()

    def clone(self):
        new_station = BusStation()
        new_station.fitness = self.fitness
        new_station.num_buses = self.num_buses
        new_station.pass_count = self.pass_count
        new_station.route_time = self.route_time
        new_station.bus_capacity = self.bus_capacity
        new_station.peak_hours = self.peak_hours[:]
        new_station.drivers = [driver.clone() for driver in self.drivers]
        new_station.pass_default = self.pass_default
        new_station.pass_peak = self.pass_peak
        new_station.generate_schedule()
        return new_station

    def assign_driver(self):
        for driver in self.drivers:
            if driver.get_status() in [Status.PENDING, Status.REST]:
                if driver.get_status() == Status.REST:
                    driver.start_work()
                    if driver.get_status() == Status.REST:
                        continue
                    else:
                        return driver
                else:
                    return driver
        return None

    def change_to_pending(self, drivers):
        for driver in drivers:
            driver.status = Status.PENDING

    def update_driver_work_time(self):
        for driver in self.drivers:
            if driver.get_status() != Status.REST:
                driver.add_route_time()

    def generate_work_day_schedule(self, day):
        current_time = 6 * 60
        end_of_day = (24 + 3) * 60
        while current_time + self.route_time + 10 < end_of_day:
            is_peak = any(start <= current_time < end for start, end in self.peak_hours)
            passengers = self.pass_peak if is_peak else self.pass_default
            num_buses = min(self.num_buses, passengers // self.bus_capacity)
            working_drivers = []

            for bus in range(num_buses):
                if passengers < self.bus_capacity * 0.2:
                    break

                driver = self.assign_driver()
                if not driver:
                    continue
                else:
                    working_drivers.append(driver)
                if driver.type == "A":
                    driver.is_peak = is_peak

                driver.status = Status.IN_WORK
                current_time += random.randint(0, 10)
                current_passengers = int(self.bus_capacity * (0.9 + (random.randint(0, 5) / 100)))

                self.schedule.add_entry(f"{driver.driver_id} {driver.type}", driver.driver_id, current_time, current_passengers, day)
                passengers -= current_passengers
                self.fitness += current_passengers
            current_time += self.route_time
            self.change_to_pending(working_drivers)
            self.update_driver_work_time()
        for driver in self.drivers:
            if driver.type == "B":
                if driver.days_from_last_work != 2:
                    continue
            driver.end_work()

    def generate_weekend_schedule(self, day):
        current_time = 6 * 60
        end_of_day = (24 + 3) * 60
        while current_time + self.route_time + 10 < end_of_day:
            passengers = self.pass_count // 7 / 21
            num_buses = min(self.num_buses, int(passengers // self.bus_capacity))
            working_drivers = []
            for bus in range(num_buses):
                if passengers < 2:
                    break
                driver = self.assign_driver()
                if not driver:
                    continue
                else:
                    working_drivers.append(driver)

                driver.status = Status.IN_WORK
                current_time += random.randint(0, 10)
                current_passengers = int(self.bus_capacity * (0.9 + (random.randint(0, 5) / 100)))

                self.schedule.add_entry(f"{driver.driver_id} {driver.type}", driver.driver_id, current_time, current_passengers, day)
                passengers -= current_passengers
                self.fitness += current_passengers
            current_time += self.route_time
            self.change_to_pending(working_drivers)
            self.update_driver_work_time()
        for driver in self.drivers:
            if driver.type == "B":
                if driver.days_from_last_work != 2:
                    continue
            driver.end_work()

    def generate_schedule(self):
        self.fitness = 0
        self.schedule = BusSchedule()
        for driver in self.drivers:
            driver.reset()

        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        for day in range(len(days) - 2):
            self.generate_work_day_schedule(days[day])
            for driver in self.drivers:
                if driver.type == "B":
                    driver.increment_rest_days()
        self.generate_weekend_schedule(days[-2])

        for driver in self.drivers:
            if driver.type == "B":
                driver.increment_rest_days()

        self.generate_weekend_schedule(days[-1])

