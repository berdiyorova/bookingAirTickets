from except_log import log_decorator
from fileManager.file_manager import JsonManager


user_manager = JsonManager('fileManager/users.json')
plane_manager = JsonManager('fileManager/planes.json')
airport_manager = JsonManager('fileManager/airports.json')
flight_manager = JsonManager('fileManager/flights.json')
booked_flight = JsonManager('fileManager/booked_flights.json')


def countries():  # davlatlar nomi 1 martadan qatnashgan listni qaytaradi
    airports = airport_manager.read()

    ctrs = []
    for airport in airports:
        if airport['country'] not in ctrs:
            ctrs.append(airport['country'])

    count = 1
    for country in ctrs:
        print(f"{count}. {country}")
        count += 1

    return ctrs


def search_flights():  # tanlangan davlatlar asosida reyslarni topib beradi
    all_flights = flight_manager.read()
    ctrs = countries()

    print("\nSelect countries from the list:")  # ro'yxatdagi tartib raqam bo'yicha davlat tanlanadi va uning indexi tartib raqamidan 1 taga kichik
    index1 = int(input("From:  ")) - 1
    index2 = int(input("To:  ")) - 1

    from_country = ctrs[index1]
    to_country = ctrs[index2]

    count = 1
    flights = []  # qidirilayotgan reyslar shu listda hosil qilinadi
    for flight in all_flights:
        if flight['from_country']['country'] == from_country and flight['to_country']['country'] == to_country:
            if flight['plane']['capacity'] > 0:
                print(f"{count}. {flight}")
                flights.append(flight)
                count += 1

    return flights


def select_flight():  # topilgan reyslardan birini tanlash
    results = search_flights()
    index = int(input("\nSelect a flight from the list:  ")) - 1
    flight = results[index]

    all_flights = flight_manager.read()

    for fl in all_flights:
        if fl == flight:
            fl['plane']['capacity'] -= 1  # tanlangan reys uchun samolyotning sig'imi bittaga kamaytiriladi
            break

    return flight


def buy_ticket(phone):
    passport = input("Enter your passport seria&number:  ")
    email = input("Enter your email:  ")
    flight = select_flight()
    ticket = {
        'passenger': {
            'passport': passport,
            'email': email,
            'phone': phone
        },
        'plain': flight['plane']['name'],
        'from_country': flight['from_country']['country'],
        'to_country': flight['to_country']['country'],
        'flight_time': flight['flight_time'],
        'landing_time': flight['landing_time'],
        'price': flight['price']
    }
    booked_flight.add_data(ticket)
    return passenger_menu(phone)

@log_decorator
def ticket_menu(phone):
    print("""
    1. Buy ticket
    2. Back
    """)

    choice = int(input("Enter your choice:  "))
    if choice == 1:
        buy_ticket(phone)
    else:
        return passenger_menu(phone)


def my_booked_flights(phone):
    my_flights = booked_flight.read()
    count = 1
    for ticket in my_flights:
        if ticket['passenger']['phone'] == phone:
            print(f"{count}.\n{ticket}")
            count += 1

    return passenger_menu(phone)


@log_decorator
def logout(phone):
    users = user_manager.read()
    for user in users:
        if user['phone'] == phone:
            user['is_login'] = False
            break

    user_manager.write(users)
    return True


@log_decorator
def passenger_menu(phone):
    print("""
        1. Search flights
        2. My booked flights
        3. Logout
        """)

    choice = int(input("Enter your choice:  "))
    if choice == 1:
        ticket_menu(phone)
    elif choice == 2:
        my_booked_flights(phone)
    else:
        logout(phone)
