import hashlib

from except_log import log_decorator
from fileManager.file_manager import JsonManager
from admin_app import admin_menu
from passenger_app import passenger_menu


admin_phone = '777'
admin_password = '777'

user_manager = JsonManager('fileManager/users.json')



class User:
    def __init__(self, first_name, last_name, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.password = password
        self.is_login = False

    def check_password(self, confirm_password):
        return self.password == confirm_password

    def hash_password(self):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()

    @property
    def user_type(self):
        if self.phone == admin_phone:
            return 'admin'
        else:
            return 'passenger'



@log_decorator
def register():
    first_name = input("Enter your first name:  ")
    last_name = input("Enter your last name:  ")
    phone = input("Enter your phone:  ")
    password = input("Enter password:  ")
    confirm_password = input("Confirm password:  ")

    user = User(first_name, last_name, phone, password)
    if not user.check_password(confirm_password):
        print("Passwords do not match.")
        register()

    user.hash_password()
    user_manager.add_data(user.__dict__)
    return auth_menu()


@log_decorator
def login():
    phone = input("Enter your phone:  ")
    password = input("Enter your password:  ")

    users = user_manager.read()
    index = 0
    while index < len(users):
        if users[index]['phone'] == phone and users[index]['password'] == hashlib.sha256(password.encode()).hexdigest():
            users[index]['is_login'] = True
            user_manager.write(users)

            user = User(
                users[index]['first_name'], users[index]['last_name'], users[index]['phone'], users[index]['password']
            )
            if user.user_type == 'admin':
                return admin_menu(phone)  # admin yoki passenger login qilgan vaqtda logout qilish yoki boshqa kerakli
            else:                                   # operatsiyalarni bajarish uchun ularning phone i
                return passenger_menu(phone)        # shu yerda uzatib yuboriladi
        index += 1

    print("Phone or password is incorrect. Try again.")
    return login()


@log_decorator
def auth_menu():
    print("""
    1. Register
    2. Login
    3. Exit    
    """)
    choice = int(input("Enter your choice:  "))
    if choice == 1:
        register()
    elif choice == 2:
        login()
    else:
        return


if __name__ == '__main__':
    auth_menu()
