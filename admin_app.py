from datetime import datetime

from except_log import log_decorator
from fileManager.file_manager import JsonManager


user_manager = JsonManager('fileManager/users.json')
plane_manager = JsonManager('fileManager/planes.json')
airport_manager = JsonManager('fileManager/airports.json')
flight_manager = JsonManager('fileManager/flights.json')


class Plane:
    def __init__(self, plane_id, name, capacity):
        self.id = plane_id
        self.name: str = name
        self.capacity: int = capacity


class Airport:
    def __init__(self, name, country):
        self.name = name
        self.country = country


class Flight:
    def __init__(self, plane, from_country, to_country, flight_time, landing_time, price):
        self.plane = plane
        self.from_country = from_country
        self.to_country = to_country
        self.flight_time = str(flight_time)
        self.landing_time = str(landing_time)
        self.price = price





"""  PLANE  APP  """

def add_plane():  # create plane
    planes = plane_manager.read()

    plane_id = len(planes) + 1
    name = input("Enter plane name:  ")
    capacity = int(input("Enter capacity:  "))

    plane = Plane(plane_id, name, capacity)

    plane_manager.add_data(plane.__dict__)

    return plane_menu()

def update_plane_menu(plane):  # mavjud planeni o'zgartirish uchun menu
    print("""
        1. name
        2. capacity
        3. exit
        """)
    while True:
        choice = int(input("Select an attribute to update:  "))
        if choice == 1:
            name = input("Enter plane name:  ")
            plane['name'] = name

        elif choice == 2:
            capacity = int(input("Enter capacity:  "))
            plane['capacity'] = capacity

        else:
            return plane_menu()


def update_plane():  # mavjud planeni o'zgartirish
    planes = show_planes()
    index = int(input("Select plane:  ")) - 1  # planeni tartib raqami bo'yicha tanlanadi

    print(planes[index])
    update_plane_menu(planes[index])  # tanlangan plane update_plane_menu() da update qilinadi

    plane_manager.write(planes)

    return plane_menu()


def delete_plane():  # mavjud planeni o'chirish
    planes = show_planes()
    index = int(input("Select plane:  ")) - 1  # planeni tartib raqami bo'yicha tanlanadi

    planes.pop(index)
    plane_manager.write(planes)

    return plane_menu()


def show_planes():  # barcha samolyotlar ro'yxatini chop etadi va qaytaradi
    planes = plane_manager.read()
    count = 1
    for plane in planes:
        print(f"{count}.\n{plane}\n")
        count += 1

    return planes










"""  AIRPORT  APP  """

def add_airport():  # create airport
    name = input("Enter airport name:  ")
    country = input("Enter country:  ")

    airport = Airport(name, country)

    airport_manager.add_data(airport.__dict__)

    return airport_menu()


def update_airport_menu(airport):  # mavjud airportni o'zgartirish uchun menu
    print("""
        1. name
        2. country
        3. exit
        """)
    while True:
        choice = int(input("Select an attribute to update:  "))
        if choice == 1:
            name = input("Enter airport name:  ")
            airport['name'] = name

        elif choice == 2:
            country = input("Enter country:  ")
            airport['country'] = country

        else:
            return airport_menu()


def update_airport():  # mavjud airportni o'zgartirish
    airports = show_airports()
    index = int(input("Select airport:  ")) - 1  # airportni tartib raqami bo'yicha tanlanadi

    print(airports[index])
    update_airport_menu(airports[index])  # tanlangan airport update_airport_menu() da update qilinadi

    airport_manager.write(airports)

    return airport_menu()


def delete_airport():  # mavjud airportni o'chirish
    airports = show_airports()
    index = int(input("Select airport:  ")) - 1  # airportni tartib raqami bo'yicha tanlanadi

    airports.pop(index)
    airport_manager.write(airports)

    return airport_menu()


def show_airports():  # barcha airportlar ro'yxatini chop etadi va qaytaradi
    airports = airport_manager.read()
    count = 1
    for airport in airports:
        print(f"{count}.\n{airport}\n")
        count += 1

    return airports







"""  FLIGHT  APP  """

def add_flight():  # yangi reys yaratish
    planes = show_planes()
    index = int(input("Select plane:  ")) - 1  # samalyot tartib raqami bo'yicha tanlanadi
    plane = Plane(planes[index]['id'], planes[index]['name'], planes[index]['capacity'])

    airports = show_airports()
    index = int(input("Select airport for flight:  ")) - 1  # jo'nab ketish ayroporti tartib raqami bo'yicha tanlanadi
    flight_place = Airport(airports[index]['name'], airports[index]['country'])

    index = int(input("Select airport for landing:  ")) - 1  # qo'nish ayroporti tartib raqami bo'yicha tanlanadi
    landing_place = Airport(airports[index]['name'], airports[index]['country'])

    print("Enter flight time:\n")
    year = int(input("Year: "))
    month = int(input("Month: "))
    day = int(input("Day: "))
    hour = int(input("Hour: "))
    minute = int(input("Minute: "))
    flight_time = datetime(year, month, day, hour, minute)

    print("\nEnter landing time:\n")
    year = int(input("Year: "))
    month = int(input("Month: "))
    day = int(input("Day: "))
    hour = int(input("Hour: "))
    minute = int(input("Minute: "))
    landing_time = datetime(year, month, day, hour, minute)

    price = input("\nEnter price:  ")

    flight = Flight(None, None, None, flight_time, landing_time, price)
    flight = flight.__dict__
    flight['plane'] = plane.__dict__
    flight['from_country'] = flight_place.__dict__
    flight['to_country'] = landing_place.__dict__

    flight_manager.add_data(flight)

    return flight_menu()


def update_flight_menu(flight):  # mavjud reysni o'zgartirish uchun menu
    print("""
        1. plane
        2. from_country
        3. to_country
        4. flight_time
        5. landing_time
        6. price
        7. exit
        """)
    while True:
        choice = int(input("Select an attribute to update:  "))
        if choice == 1:
            planes = show_planes()
            index = int(input("Select plane:  ")) - 1  # samalyot tartib raqami bo'yicha tanlanadi
            plane = Plane(planes[index]['id'], planes[index]['name'], planes[index]['capacity'])

            flight['plane'] = plane.__dict__

        elif choice == 2:
            airports = show_airports()
            index = int(input("Select airport for flight:  ")) - 1  # jo'nab ketish ayroporti tartib raqami bo'yicha tanlanadi
            flight_place = Airport(airports[index]['name'], airports[index]['country'])

            flight['from_country'] = flight_place.__dict__

        elif choice == 3:
            airports = show_airports()
            index = int(input("Select airport for landing:  ")) - 1  # qo'nish ayroporti tartib raqami bo'yicha tanlanadi
            landing_place = Airport(airports[index]['name'], airports[index]['country'])

            flight['to_country'] = landing_place.__dict__

        elif choice == 4:
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))
            hour = int(input("Hour: "))
            minute = int(input("Minute: "))
            time = datetime(year, month, day, hour, minute)
            flight['flight_time'] = time

        elif choice == 5:
            year = int(input("Year: "))
            month = int(input("Month: "))
            day = int(input("Day: "))
            hour = int(input("Hour: "))
            minute = int(input("Minute: "))
            time = datetime(year, month, day, hour, minute)
            flight['landing_time'] = time

        elif choice == 6:
            price = float(input("Enter price:  "))
            flight['price'] = price

        else:
            return flight_menu()

def update_flight():  # mavjud reysni o'zgartirish
    flights = show_flights()
    index = int(input("Select flight:  ")) - 1  # reysni tartib raqami bo'yicha tanlanadi

    print(flights[index])
    update_flight_menu(flights[index])  # tanlangan reys update_flight_menu() da update qilinadi

    flight_manager.write(flights)

    return flight_menu()


def delete_flight():  # mavjud reysni o'chirish
    flights = show_flights()
    index = int(input("Select flight:  ")) - 1  # reysni tartib raqami bo'yicha tanlanadi

    flights.pop(index)
    flight_manager.write(flights)

    return flight_menu()


def show_flights():  # barcha reyslar ro'yxatini chop etadi va qaytaradi
    flights = flight_manager.read()
    count = 1  # ro'yxat uchun tartib raqam
    for flight in flights:
        print(f"{count}.\n{flight}\n")
        count += 1

    return flights






"""  ADMIN  APP  """

@log_decorator
def logout(phone):  # admin uchun logout function
    users = user_manager.read()
    for user in users:
        if user['phone'] == phone:
            user['is_login'] = False
            break

    user_manager.write(users)

    return True

@log_decorator
def plane_menu():  # samalyotlar bo'limi menusi
    print("""
    1. Add plane
    2. Update plane info
    3. Delete plane
    4. Show all planes
    5. Exit
    """)

    choice = int(input("Enter your choice:  "))
    if choice == 1:
        add_plane()
    elif choice == 2:
        update_plane()
    elif choice == 3:
        delete_plane()
    elif choice == 4:
        show_planes()
        plane_menu()
    else:
        admin_menu()


@log_decorator
def airport_menu():  # airportlar bo'limi menusi
    print("""
    1. Add airport
    2. Update airport info
    3. Delete airport
    4. Show all airports
    5. Exit
    """)

    choice = int(input("Enter your choice:  "))
    if choice == 1:
        add_airport()
    elif choice == 2:
        update_airport()
    elif choice == 3:
        delete_airport()
    elif choice == 4:
        show_airports()
        airport_menu()
    else:
        admin_menu()


@log_decorator
def flight_menu():  # reyslar bo'limi menusi
    print("""
    1. Add flight
    2. Update flight info
    3. Delete flight
    4. Show all flights
    5. Exit
    """)

    choice = int(input("Enter your choice:  "))
    if choice == 1:
        add_flight()
    elif choice == 2:
        update_flight()
    elif choice == 3:
        delete_flight()
    elif choice == 4:
        show_flights()
        flight_menu()
    else:
        admin_menu()


@log_decorator
def admin_menu(phone):
    print("""
    1. Planes
    2. Airports
    3. Flights
    4. Logout
    """)

    choice = int(input("Enter your choice:  "))
    if choice == 1:
        plane_menu()
    elif choice == 2:
        airport_menu()
    elif choice == 3:
        flight_menu()
    else:
        logout(phone)
