import random
from bus_station import BusStation
from driver import DriverA, DriverB
from dotenv import load_dotenv
import os
load_dotenv()
PASSENGERS_PER_WEEK = int(os.getenv("PASSENGERS_PER_WEEK"))


class GeneticAlgorithm:
    def __init__(self):
        self.population_size = 100
        self.generations = 25
        self.P_MUTATION = 0.1
        self.P_CROSSOVER = 0.9

    def initialize_population(self):
        return [BusStation() for _ in range(self.population_size)]

    def fitness_function(self, station):
        return station.fitness

    def crossover(self, child1, child2):
        cutting_point = random.randint(1, len(child1) - 2)
        child1[cutting_point:], child2[cutting_point:] = child2[cutting_point:], child1[cutting_point:]

    def mutate(self, station):
        for _ in range(len(station.drivers)):
            if random.random() < 0.05:
                index = random.randint(0, len(station.drivers) - 1)
                station.drivers[index] = DriverA() if station.drivers[index].type == "B" else DriverB()

    def tournament_selection(self, population):
        offspring = []
        for _ in range(len(population)):
            random_individuals = []
            while len(random_individuals) < 3:
                random_individual = population[random.randint(0, len(population) - 1)]
                if random_individual not in random_individuals:
                    random_individuals.append(random_individual)

            best_individual = sorted(random_individuals, key=self.fitness_function, reverse=True)[0]

            if best_individual in offspring:
                best_individual = best_individual.clone()
            offspring.append(best_individual)
        return offspring

    def run(self):
        population = self.initialize_population()
        fitness_values = [self.fitness_function(station) for station in population]
        generation = 0
        max_fitness_values = []
        best_individual = None

        while max(fitness_values) < PASSENGERS_PER_WEEK and generation < self.generations:
            generation += 1
            offspring = self.tournament_selection(population)

            elite_size = 10
            elite = sorted(population, key=self.fitness_function, reverse=True)[:elite_size]
            offspring = elite + offspring[len(elite):]

            for even_individual, odd_individual in zip(offspring[::2], offspring[1::2]):
                if random.random() <= self.P_CROSSOVER:
                    self.crossover(even_individual.drivers, odd_individual.drivers)

            for station in offspring:
                if random.random() <= self.P_MUTATION:
                    self.mutate(station)

            for station in offspring:
                station.generate_schedule()

            fitness_values = [self.fitness_function(station) for station in offspring]
            max_fitness_value = max(fitness_values)
            max_fitness_values.append(max_fitness_value)

            for station in offspring:
                if station.fitness == max_fitness_value:
                    best_individual = station

            population[:] = offspring
            print("Генерация: ", generation)
            print("Приспособленность лучшего представителя: ", best_individual.fitness, max_fitness_value)

        best_schedule = max(population, key=self.fitness_function)
        best_schedule.schedule.correct_days()
        best_schedule.schedule.display()


if __name__ == "__main__":
    ga = GeneticAlgorithm()
    ga.run()