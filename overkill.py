import itertools
from bus_station_for_bruteforce import BusStation
from driver import DriverA, DriverB
from dotenv import load_dotenv
import os
load_dotenv()
PASSENGERS_PER_WEEK = int(os.getenv("PASSENGERS_PER_WEEK"))


class BruteForce:
    def __init__(self):
        self.passengers_per_week = PASSENGERS_PER_WEEK

    def generate_all_combinations(self, station):
        driver_combinations = list(itertools.product([DriverA(), DriverB()], repeat=len(station.drivers)))
        schedule_combinations = [station.generate_schedule() for _ in range(10)]
        return driver_combinations, schedule_combinations

    def evaluate_combinations(self, driver_combinations, schedule_combinations):
        best_fitness = -float('inf')
        best_station = None

        for drivers in driver_combinations:
            for schedule in schedule_combinations:
                station_copy = station.clone()
                station_copy.drivers = list(drivers)
                station_copy.schedule = schedule
                fitness = station_copy.fitness

                if fitness > best_fitness:
                    best_fitness = fitness
                    best_station = station_copy
        return best_station

    def run(self, station):
        driver_combinations, schedule_combinations = self.generate_all_combinations(station)
        best_station = self.evaluate_combinations(driver_combinations, schedule_combinations)

        print("Лучшее расписание:")
        best_station.schedule.correct_days()
        best_station.schedule.display()
        print(f"Приспособленность лучшего расписания: {best_station.fitness}")

if __name__ == "__main__":
    station = BusStation()
    brute_force = BruteForce()
    brute_force.run(station)
