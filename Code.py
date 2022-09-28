import json
import hashlib
class User():
    def __init__(self, *args, **kwargs):
        ptr = iter(args)
        self.__username = next(ptr, kwargs.get('username'))
        self.__name = next(ptr, kwargs.get('name'))
        self.__surname = next(ptr, kwargs.get('surname'))
        self.__age = next(ptr, kwargs.get('age'))
        self.__hash_pass = next(ptr, kwargs.get('hashpass'))
        
    @property
    def username(self):
        return self.__username
    @username.setter
    def username(self, username):
        self.__username = username
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name
    @property
    def surname(self):
        return self.__surname
    @surname.setter
    def surname(self, surname):
        self.__surname = surname
    @property
    def age(self):
        return self.__age
    @age.setter
    def age(self, age):
        self.__age = age
    @property
    def hash_pass(self):
        return self.__hash_pass
    @hash_pass.setter
    def hash_pass(self, hash_pass):
        self.__hash_pass = hash_pass
        
    def to_dict(self):
        return {self.__username : {
            "username" : self.__username,
            "name" : self.__name,
            "surname" : self.__surname,
            "age" : self.__age,
            "hashpass" : self.__hash_pass}
                }
    
class Auth():
    def register(self, data):
        #input data
        username = input("Please enter your username: ")
        while self.exist(username, data):
            username = input("This username is already taken, Please enter your username: ")
        name = input("Please enter your name: ")
        surname = input("Please enter your surname: ")
        age = 0
        while age == 0:
            try:
                age = int(input("Please enter your age: "))
            except ValueError:
                print("You input wrong age, age must be integer")
        password = input("Please enter your password :")
        confirm = input("Please confirm your password : ")
        while password != confirm :
            password = input("Your passwords are not the same. Please re-enter password")
            confirm = input("Please confirm your password : ")

        #Create user with this data, update database
        new_user = User(username, name, surname, age, self.hash_password(password))
        data.update(new_user.to_dict())
        
    def exist(self, username, data):
        return (data.get(username) is not None)
    
    def login(self, data):
        #login by username, ask to register new one
        username = input("Please enter your username: ")
        tries = 0
        while self.exist(username, data) == False: 
            tries += 1
            print("There is no user with this username")
            if tries >= 3:
                print("Are you sure you created account before? Do you want to register?")
                print("Choose:\n 0 - try to login\nAny other integer - register")
                x = 0
                while True:
                    try:
                        x = int(input())
                    except ValueError:
                        print("Please input an integer")
                        continue
                    break
                if x:
                    self.register(data)
            username = input("Please enter your username: ")

        #Create user with information from database
        account = User(**data[username])

        #Check for password validation, limit for tries count
        password = self.hash_password(input("Please enter your password: "))
        tries = 4
        while account.hash_pass != password and tries > 0:
            password = self.hash_password(input("Password is wrong, {} tries left: ".format(tries)))
            tries -= 1
        if account.hash_pass != password:
            print("You can no longer enter a password: ")
            return "guest"

        print("You've logged in successfully")
        print("Welcome back {} {}".format(account.name, account.surname))
        return username

    
    def change_password(self, data, user):
        new_password = input("Please enter new password: ")
        confirm = input("Please confirm your password : ")
        while new_password != confirm :
            new_password = input("Your passwords are not the same. Please re-enter password")
            confirm = input("Please confirm your password : ")
        data[user]["hashpass"] = self.hash_password(new_password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

def run():
    print("Welcome to Registration & Authentication System")
    user = "guest"
    auth = Auth()
    try :
        with open("JsonData.json", "r") as file:
            data = json.load(file)
    except :
        data = {}
    with open("JsonData.json", "w") as file:
        while True:
            #Option menu, interact with command line
            #different scenarios for guest and registered user
            
            if user != "guest" :
                print("You logged in as {}".format(user))
            print("Select an option:")
            print("0. Quit")
            if user == 'guest': #for guest
                print("1. Register")
                print("2. Login")
                try:
                    choice = int(input())
                except ValueError:
                    print("Input is wrong, Please input an integer")
                    continue
                if choice == 1:
                    auth.register(data)
                elif choice == 2:
                    user = auth.login(data)
                elif choice == 0:
                    break
                else :
                    print("Input correct option")

            else : #for registered user
                print("1. Change password")
                print("2. Logout")
                try:
                    choice = int(input())
                except ValueError:
                    print("Input is wrong, Please input an integer")
                    continue
                if choice == 1:
                    auth.change_password(data, user)
                elif choice == 2:
                    user = "guest"
                elif choice == 0:
                    break
                else :
                    print("Input correct option")
        #update database through json with new data
        json.dump(data, file)

#run the programm to check implemented functions
run()
