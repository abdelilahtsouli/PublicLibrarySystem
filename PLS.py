import json
import csv
import random
import string
import time
class Person():
    def __init__(self, ):
        pass
    def username_check(username):
        with open("all_usernames.json", "r") as usernames_json:
            data = json.load(usernames_json)
        for item in data:
            if username.lower() == item["username"].lower():
                return True 
        return False
class Librarian(Person):
    def __init__(self):
        self.Password = "admin"

    def Book_id_generator(self):
        letters = string.ascii_uppercase
        Book_id = ''.join(random.choice(letters) for i in range(8))
        return Book_id
    def AddBook(self, BookObject): 
        with open('all_books.json', 'r') as books_json:
            FileData = json.load(books_json)
        BookData = {
            "available_limit": BookObject.BookItems,
            "author": BookObject.Author, 
            "id": BookObject.ID,
            "country": BookObject.Country,
            "imageLink": BookObject.ImageLink,
            "language": BookObject.Language,
            "link": BookObject.WikiLink + "\n",
            "pages": BookObject.Pages,
            "title": BookObject.Title,
            "year": BookObject.Year,
            "borrower" : BookObject.Borrower
        }
        UpdatedData = FileData
        UpdatedData.append(BookData)
        books_json.close()
        with open('all_books.json', 'w') as NewFile:
            NewFile.write("")
            NewFile.write(json.dumps(UpdatedData, indent=4, sort_keys=True))
    def RemoveBook(self, BookTitle): 
        with open('all_books.json', 'r') as books_json:
            data = json.load(books_json)
            bookFound = False
            for i in range(len(data)):
                if data[i]["title"] == BookTitle:
                    del data[i]
                    bookFound = True
                    print(f"You have successfully removed the book [{BookTitle}]!")
                    break
            if not bookFound:
                print(f"Book [{BookTitle}] could not be found!")
            with open('all_books.json', 'w') as NewFile:
                NewFile.write("")
                NewFile.write(json.dumps(data, indent=4, sort_keys=True))

class Catalog():
    def __init__(self):
        pass
    def SearchBook(self, SearchCriteria):
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
        
        string = ""
        SearchCriteriaLowerCase = SearchCriteria.lower()
        for item in books:
            book_string = str(item).lower()
            SplitCriteria = SearchCriteriaLowerCase.split()
            for values in SplitCriteria:
                if values in book_string:
                    s = "\tTitle : " + item["title"] + "\n\tAuthor : " + item["author"] + "\n\tAvailable : " + str(item["available_limit"]) + "\n\tCountry : " + item["country"] + "\n\tImage : " + item["imageLink"] + "\n\tLanguage : " + item["language"] + "\n\tLink : " + item["link"] + "\tPages : " + str(item["pages"]) + "\n\tYear : " + str(item["year"]) + "\n\tBookID : " + item["id"] + "\n\n" 
                    if s in string:
                        continue
                    else:
                        string += s
        if len(string) > 1:
            print("\nSearch results: \n")
            print(string)
        else:
            print("\nNo search results. Try again with different criteria.\n")



class LoanAdministration(Librarian):
    def __init__(self):
        pass
    def CheckLoaned(self, LoanItem):
        book_title = LoanItem.lower()
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
        for book in books:
            if book_title == book["title"].lower():
                if book["available_limit"] > 0:
                    return True
                else:
                    return False
    def LoanBook(self, book_title, username): 
        AlreadyLoaned = False
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
        for book in books:
            BookAvailability = self.CheckLoaned(book_title)
            if book_title.lower() == book["title"].lower():
                if username not in book["borrower"]:
                    if BookAvailability:
                        book["available_limit"] -= 1
                        book["borrower"].append(username)
                        code = book["id"]
                        Success = True
                        break
                    else:
                        Success = False
                else:
                    AlreadyLoaned = True
        with open("all_books.json", "w") as books_json:
            books_json.write(json.dumps(books, indent=4, sort_keys=True))
        try:
            if AlreadyLoaned == True:
                print("\nYou are already borrowing the book that you selected!\n")
            elif Success:
                print(f"\nYou have successfully borrowed [{book_title}].\nYour book ID is [{code}]. Please do not forget this ID!\n")
            elif not Success:
                print("\nThe book that you selected is currently not available!\n")
        except:
            print("\nBook not found!\n")
class LoanItem(LoanAdministration):
    def __init__(self):
        pass
    def ReturnBook(self, username): 
        id = input("Please enter the book ID: ")
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
        Status = 0

        for book in books:
            if id.upper() == book["id"]:
                for i in range(0, len(book["borrower"])):
                    if book["borrower"][i].lower() == username.lower():
                        book["available_limit"] += 1
                        del book["borrower"][i]
                        returnedbooktitle = book["title"]
                        Status = 1
                        break
                    else:
                        Status = 2
        if Status == 0:
            print("Book could not be found.\n")
        elif Status == 1:
            print(f"You have successfully returned {returnedbooktitle}.\n")
        elif Status == 2:
            print(f"Book [{id}] was not borrowed by [{username}].\nPlease try again.\n")
        with open("all_books.json", "w") as books_json:
            books_json.write(json.dumps(books, indent=4, sort_keys=True))

    def ListofBorrowers(self, bookID):
        Borrowers = []
        booktitle = ""
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
        for book in books:
            if bookID.upper() == book["id"].upper():
                booktitle = book["title"]
                for i in range(len(book["borrower"])):
                    Borrowers.append(book["borrower"][i])
            elif bookID.lower() == book["title"].lower():
                bookID = book["id"]
                booktitle = book["title"]
                for i in range(len(book["borrower"])):
                    Borrowers.append(book["borrower"][i])
        if len(Borrowers) > 0:
            print(f"Book [{booktitle}] with ID [{bookID}] is currently loaned out to: \n")
            for i in range(len(Borrowers)):
                print("[*] "+ Borrowers[i])
        else:
            print("Book has not been loaned out to anyone yet!\n")

class Book():
    def __init__(self, Author, ID, Country, ImageLink, Language, WikiLink, Pages, Title, Year, Borrower, BookItems):
        self.Author = Author
        self.ID = ID
        self.Country = Country
        self.ImageLink = ImageLink
        self.Language = Language
        self.WikiLink = WikiLink
        self.Pages = Pages
        self.Title = Title
        self.Year = Year
        self.Borrower = Borrower
        self.BookItems = BookItems

class BookItem(Book):
    def __init__(self, IDofBook, AmountItems, AmountAvailable):
        self.IDBook = IDofBook
        self.Amount = AmountItems
        self.Available = AmountAvailable

    def RemoveBookItem(self, BookTitle, BookItemAmountToRemove): 
        bookFound = False
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
        for book in books:
            if BookTitle.lower() == book["title"].lower():
                bookFound = True
                if book["available_limit"] >= BookItemAmountToRemove:
                    book["available_limit"] -= int(BookItemAmountToRemove)
                    print(f"You have successfully removed [{BookItemAmountToRemove}] book item(s) of book [{BookTitle}]")
                    break
                else:
                    amountleft = book["available_limit"]
                    if amountleft > 0:
                        print(f"You only have {amountleft} book items to remove!\n")
                    else:
                        print("You have no book items for this book at all left to remove.")
        if not bookFound:
            print(f"Book [{BookTitle}] could not be found!")
        with open("all_books.json", "w") as books_json:
            books_json.write(json.dumps(books, indent=4, sort_keys=True))

    def AddBookItem(self, book_title, amounttoadd): 
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
            bookFound = False
        for book in books:
            if book_title.lower() == book["title"].lower():
                book["available_limit"] += int(amounttoadd)
                bookFound = True
                print(f"You have successfully added [{amounttoadd}] book item(s) of book [{book_title}]")
                break
        if not bookFound:
            print(f"Book {book_title} could not be found!")
        with open("all_books.json", "w") as books_json:
            books_json.write(json.dumps(books, indent=4, sort_keys=True))


class Subscriber(Person):
    def __init__(self, Gender, NameSet, FirstName, LastName, StreetAddress, ZipCode, City, EmailAddress, Username, PhoneNumber):
        self.Gender = Gender
        self.NameSet = NameSet
        self.FirstName = FirstName
        self.LastName = LastName
        self.StreetAddress = StreetAddress
        self.ZipCode = ZipCode
        self.City = City
        self.Email = EmailAddress
        self.Username = Username
        self.PhoneNumber = PhoneNumber
    #Adding new customers
    def CreateAccount(SubscriberObject): 
        with open("all_customers.csv", "r") as customers_csv:
            data = customers_csv.readlines()
        number = (len(data))
        customer_dict = {
            "Number": number,      
            "Gender": SubscriberObject.Gender.lower(), 
            "NameSet" : SubscriberObject.NameSet,
            "GivenName": SubscriberObject.FirstName,
            "Surname": SubscriberObject.LastName,
            "StreetAddress": SubscriberObject.StreetAddress,
            "ZipCode": SubscriberObject.ZipCode,
            "City": SubscriberObject.City,
            "EmailAddress": SubscriberObject.Email,
            "Username": SubscriberObject.Username,
            "TelephoneNumber": SubscriberObject.PhoneNumber
        }
        with open ("all_customers.csv",  "a", newline="") as customers_csv:
            writer = csv.writer(customers_csv,lineterminator='\r')
            writer.writerow(customer_dict.values())
        with open("all_usernames.json", "r") as usernames_json:
            data = json.load(usernames_json)
        with open("all_usernames.json", "w") as usernames_json:
            data.append({"username": SubscriberObject.Username})
            usernames_json.write(json.dumps(data, indent=4, sort_keys=True))

    def ListofMyBooks(Username):
        with open("all_books.json", "r") as books_json:
            books = json.load(books_json)
            listofbooks = {

                            }
        for book in books:
            for i in range(len(book["borrower"])):
                if Username.upper() == book["borrower"][i].upper():
                    listofbooks[book["id"]] = book["title"]
        if len(listofbooks) <= 0:
            print("\nYou are currently not in possession of any books!")
        else:
            print("\nYou are currently in possession of the following books: ")
            for y in listofbooks:
                print(f"[*]Book ID: [{y}]\t[*] Book Title: [{listofbooks[y]}]\n")
class PublicLibrary:
    def __init__(self):
        self.LoanAdministrationObject = LoanAdministration()
        self.LoanItemObject = LoanItem()
        self.LibrarianInstance = Librarian()
        self.CatalogObject = Catalog()
        self.BookItemObject = BookItem(None, None, None)

    def main(self):
        while True:
            UserInput = input("\n[1] To continue as a Subcriber\n[2] To continue as a Librarian\n[3] Exit\n")
            if UserInput == "1":
                AccountFound = False
                UserInput = input("[*] Please enter your username: ")
                username = UserInput
                AccountFound = Person.username_check(UserInput)
                if AccountFound:
                    print(f"\nWelcome {UserInput}!\n")
                    while True:
                        UserInput = input("[1] Search for a book\n[2] Borrow a book\n[3] Return a book\n[4] My borrowed books\n[5] Exit\n")
                        if UserInput == "1": 
                            SearchCriteria = input("\nType a keyword to search for a book (title, author, ID, etc.): ")
                            self.CatalogObject.SearchBook(SearchCriteria)

                        elif UserInput == "2":
                            RequestedBook = input("Enter the book you would like to borrow: ")
                            self.LoanAdministrationObject.LoanBook(RequestedBook, username)

                        elif UserInput == "3":
                            self.LoanItemObject.ReturnBook(username)
                        elif UserInput == "4":
                            Subscriber.ListofMyBooks(username)
                        elif UserInput == "5":
                            exit()
                else:
                    UserInput = input("We could not find an account with that name! Would you like to create a new account? \n[1] Yes\n[2] No (exit)\n")
                    while True:
                        if UserInput == "1":
                            FirstNameInput = input("[*] What is your first name?: ")
                            LastNameInput = input("[*] What is your last name?: ")
                            GenderInput = input("[*] What is your gender?: ")
                            NameSetInput = input("[*] What is your ethnicity?: ")
                            EmailInput = input("[*] What is your Email address?: ")
                            AddressInput = input("[*] What is your street address?: ")
                            ZipInput = input("[*] What is your Zip code?: ")
                            CityInput = input("[*] What is the city where you live?: ")
                            PhoneInput = input("[*] What is your phone number?: ")
                            UserNameInput = input("[*] What is your desired username (to login with)?: ")
                            AccountFound = Person.username_check(UserNameInput)
                            while True:
                                if AccountFound:
                                    UserNameInput = input("That username is already in use! Try a different username: ")
                                    AccountFound = Person.username_check(UserNameInput)
                                else:
                                    break
                            SubscriberAccount = Subscriber(GenderInput, NameSetInput, FirstNameInput, LastNameInput, AddressInput, ZipInput, CityInput, EmailInput, UserNameInput, PhoneInput)
                            Subscriber.CreateAccount(SubscriberAccount)
                            print(f"You have successfully made a new account with username: {SubscriberAccount.Username}")
                            break
                        else:
                            exit()
            elif UserInput == "2":
                UserInput = input("[*] Please enter the system password to continue: ")
                if UserInput == self.LibrarianInstance.Password:
                    print("\nYou have been successfully logged in as a Librarian!\n")
                    while True:
                        time.sleep(1.5)
                        try:
                            UserInput = int(input("[1] Add a book to the catalog\n[2] Remove a book from the catalog\n[3] Add a book item\n[4] Remove a book item\n[5] Create a new subscriber account\n[6] Check current loans per book\n[7] Make a backup of the system\n[8] Restore backup\n[9] Exit\n"))
                        except ValueError:
                            print("\nWrong input! Please use one of the provided numbers as input!\n")
                        if str(UserInput) == "1":
                            title = input("Title: ")
                            author = input("Author: ")
                            country = input("Country: ")
                            image_link = input("Imagelink: ")
                            language = input("Language: ")
                            link = input("Link: ")
                            borrower = []

                            while True:
                                try:
                                    pages = int(input("Number of pages: "))
                                    break
                                except ValueError:
                                    print("Please enter an integer.")
                            while True:
                                try:
                                    bookitems = int(input("Number of book items (copies): "))
                                    if bookitems >= 0:
                                        break
                                    else:
                                        print("You can't have a negative input")
                                except ValueError:
                                    print("Please enter an integer.")
                            while True:
                                try:
                                    year = int(input("Year: "))
                                    break
                                except ValueError:
                                    print("Please enter an integer.")
                        
                            self.BookObject = Book(author, self.LibrarianInstance.Book_id_generator(), country, image_link, language, link, pages, title, year, borrower, bookitems)
                            self.LibrarianInstance.AddBook(self.BookObject)
                            self.BookItemObject = BookItem(self.BookObject.ID, bookitems, bookitems)

                            print(f"Added new book: {self.BookObject.Title}!")
                        elif str(UserInput) == "2":
                            BookTitle = input("What is the title of the book that you want to remove from the catalog? ")
                            self.LibrarianInstance.RemoveBook(BookTitle)
                        elif str(UserInput) == "3":
                            BookItemTitle = input("What is the title of the book item that you want to add? ")
                            while True:
                                try:
                                    BookItemAmountToAdd = int(input("What is the amount of book items that you want to add? "))
                                    if BookItemAmountToAdd >= 0:
                                        break
                                    else:
                                        print("You can't have a negative input")
                                except ValueError:
                                    print("Please enter an integer.")
                            self.BookItemObject.AddBookItem(BookItemTitle, BookItemAmountToAdd)

                        elif str(UserInput) == "4":
                            BookItemTitle = input("What is the title of the book item that you want to remove? ")
                            while True:
                                try:
                                    BookItemAmountToRemove = int(input("What is the amount of book items that you want to remove? "))
                                    if BookItemAmountToRemove >= 0:
                                       break   
                                    else:
                                        print("You can't have a negative input")
                                except ValueError:
                                    print("Please enter an integer.")
                            self.BookItemObject.RemoveBookItem(BookItemTitle, BookItemAmountToRemove)
                        elif str(UserInput) == "5": #Add new customer
                            FirstName = input("First Name: ")
                            LastName = input("Last Name: ")
                            GivenName = input("Ethnicity: ")
                            Gender = input("Gender: ")
                            Address = input("Street Address: ")
                            Zipcode = input("Zipcode: ")
                            City = input("City: ")
                            Email = input("Email: ")
                            while True:
                                Username = input("Username: ")
                                if Person.username_check(Username):
                                    print("That username is already taken! Try another one.")
                                else:
                                    break
                            PhoneNumber = input("PhoneNumber: ")
                            NewAccount = Subscriber(Gender, GivenName, FirstName, LastName, Address, Zipcode, City, Email, Username, PhoneNumber)
                            Subscriber.CreateAccount(NewAccount)
                            print(f"{NewAccount.Username} has been added to the database.")
                            break

                        elif str(UserInput) == "6": 
                            UserInput = input("Enter the ID or title of the book that you would like a list of loaners of: ")
                            self.LoanItemObject.ListofBorrowers(UserInput)
                        elif str(UserInput) == "7": 
                            self.BackupSystem()
                            print("*** The system has been successfully backed up. ***")
                        elif str(UserInput) == "8": 
                            self.RestoreSystem()
                            print("*** The system has been restored to the most recent backup. ***")
                        elif str(UserInput) == "9": 
                            exit()
            elif UserInput == "3":
                exit()
            else:
                print("\nWrong input! Please use one of the provided numbers as input!\n")
    def BackupSystem(self): 
        with open('all_books.json', 'r') as books_json:
            json_file = open("Backup.json", "w")
            json_file.write(json.dumps(json.load(books_json), indent=4, sort_keys=True))
            json_file.close()
        with open ("all_customers.csv",  "r", newline="") as customers_csv:
            csv_file = open("Backup.csv", "w")
            csv_file.writelines(customers_csv.readlines())
            csv_file.close()

    def RestoreSystem(self): 
        with open('all_books.json', 'w') as books_json:
            json_file = open("Backup.json", "r")
            books_json.write(json.dumps(json.load(json_file), indent=4, sort_keys=True))
            json_file.close()
        with open("all_customers.csv", "w", newline="") as customers_csv:
            csv_file = open("Backup.csv", "r")
            customers_csv.writelines(csv_file.readlines())
            csv_file.close()

Main = PublicLibrary()
Main.main()
