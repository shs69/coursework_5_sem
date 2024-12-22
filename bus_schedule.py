from dotenv import load_dotenv
import os
load_dotenv()
ROUTE_TIME = int(os.getenv("ROUTE_TIME"))


class BusSchedule:
    def __init__(self):
        self.schedule = {'Понедельник':[], 'Вторник':[], 'Среда':[], 'Четверг':[],
                         'Пятница':[], 'Суббота':[], 'Воскресенье':[]}

    def clone(self):
        new_schedule = BusSchedule()
        new_schedule.schedule = self.schedule
        return new_schedule

    def add_entry(self, driver, bus, start_time, passengers, day):
        self.schedule[day].append({
            "Driver": driver,
            "Bus": bus,
            "Start Time": str(start_time // 60) + ":" + str(start_time % 60),
            "End Time": str((start_time + ROUTE_TIME) // 60) + ":" + str((start_time + ROUTE_TIME) % 60),
            "Passengers": passengers
        })

    def get_next_day(self, current_day):
        days_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        current_day_index = days_order.index(current_day)
        next_day_index = (current_day_index + 1) % len(days_order)
        return days_order[next_day_index]

    def correct_days(self):
        MINUTES_IN_A_DAY = 1440

        for day, routes in self.schedule.items():
            for route in routes:

                start_time = route['Start Time']
                start_time_minutes = int(start_time.split(":")[0]) * 60 + int(start_time.split(":")[1])

                if start_time_minutes >= MINUTES_IN_A_DAY:
                    next_day = self.get_next_day(day)
                    start_time_minutes -= MINUTES_IN_A_DAY

                    new_start_time = f"{start_time_minutes // 60:02}:{start_time_minutes % 60:02}"

                    route['Start Time'] = new_start_time
                    route['End Time'] = f"{(start_time_minutes + ROUTE_TIME) // 60:02}:{(start_time_minutes + ROUTE_TIME) % 60:02}"

                    self.schedule[next_day].append(route)
                    routes.remove(route)

    def display(self):
        for day, routes in self.schedule.items():
            print(f"День: {day}")
            for route in routes:
                print(f"  Водитель: {route['Driver']}, Автобус: {route['Bus']}, "
                      f"Начальное время: {route['Start Time']}, "
                      f"Время окончания: {route['End Time']}, Количество пассажиров: {route['Passengers']}")

    def add_another_day(self, day_schedule, day):
        self.schedule[day] = day_schedule