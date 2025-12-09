from getpass import getpass
from mysql.connector import connect, Error
from datetime import date, timedelta

#Global variable for current user that is logged in
current_user = None


#Establishing a connection with the database.
try:
    with connect(
        host = "localhost",
        user = "root",
        password = getpass("Enter password: "),
        database = "book_store" 
    ) as connection:
        print(connection)

except Error as e:
    print(e)
    quit(1)


#Prints the graphics of the UI for the start menu.
def startup_graphic():
    stars = "*"
    space = " "
    print("\n" + (stars * 60))
    print((stars * 3) + (space * 54) + (stars * 3))
    print((stars * 3) + (space * 11) + "Welcome to the Online Book Store" + (space * 11) + (stars * 3))
    print((stars * 3) + (space * 54) + (stars * 3))
    print(stars * 60)


#Prints the graphics of the UI for the member menu.
def member_menu_graphics():
    stars = "*"
    space = " "
    print(stars * 60)
    print((stars * 3) + (space * 54) + (stars * 3))
    print((stars * 3) + (space * 11) + "Welcome to the Online Book Store" + (space * 11) + (stars * 3))
    print((stars * 3) + (space * 21) + "Member Menu" + (space * 22) + (stars * 3))
    print((stars * 3) + (space * 54) + (stars * 3))
    print(stars * 60)


#Handles login to interact with the database
def login():
    global current_user
    email = input("\nEnter your email address: ")
    password = input("Enter your password: ")

    member_login = "SELECT * FROM members WHERE email = %s AND password = %s"
    user_val = (email, password)
    connection.reconnect()
    with connection.cursor() as cursor:
        cursor.execute(member_login, user_val)
        result = cursor.fetchone()

    if result:
        user_fields = ["fname", "lname", "address", "city", "state", "zip", "phone", "email", "userid", "password"]
        user_dict = {}
        for i in range(len(user_fields)):
            user_dict[user_fields[i]] = result[i]
        current_user = user_dict 
        return user_dict
    else:
        print("Invalid email or password! ")
        return None
    

# Returns the current user
def get_current_user():
    global current_user
    if current_user:
        return current_user
    else:
        current_user = login()  # Prompt for login if no current user
        return current_user


#Allows user to register onto the database into the members table.
def member_registration():
    print("\nWelcome to the Online Book Store \n", "  New Member Registration")
    
    fname = input("\nEnter first name: ")
    lname = input("Enter last name: ")
    address = input("Enter street address: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    zip = int(input("Enter zip: "))
    phone = int(input("Enter Phone: "))
    email = input("Enter email address: ")
    password = input("Enter password: ")

   
    insert_members_query = """
    INSERT INTO members
    (fname, lname, address, city, state, zip, phone, email, password)
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s )
    """
    members_records = [
        (fname, lname, address, city, state, zip, phone, email, password)
    ]
    connection.reconnect()
    with connection.cursor() as cursor:
        cursor.executemany(insert_members_query, members_records)
        connection.commit()


#Next Menu screen that shows after login is successful.
def member_menu():
    member_menu_graphics()
    option1 = "\n\t1. Browse by Subject"
    option2 = "\n\t2. Search by Author/Title"
    option3 = "\n\t3. Check Out"
    option4 = "\n\t4. Logout" 

    print("\n" + option1 + "\n" + option2 + "\n" + option3 + "\n" + option4)
    choice = int(input("\nType in your option:"))

    if choice == 1:
        browse_by_subject()
    elif choice == 2:
        search_by_author()
    elif choice == 3:
       checkout()
    elif choice == 4:
        print("\nSession has ended. ")
        quit


#onverts a tuple list into a dictionary list for browse by subject.
def tuples_to_dict(list_tuples, column_names):
    list_dict = []
    for tuple in list_tuples:
        dict = {}
        dict[column_names[0]] = tuple[0]
        dict[column_names[1]] = tuple[1]
        dict[column_names[2]] = tuple[2]
        dict[column_names[3]] = tuple[3]
        list_dict.append(dict)
    return list_dict


#Converts a tuple list into a dictionary list for title/author search.
def title_tuples_to_dict(list_tuples, column_names):
    list_dict = []
    for tuple in list_tuples:
        dict = {}
        #dict = {k: v for k, v in zip(column_names, tuple)}
        dict[column_names[0]] = tuple[0]
        dict[column_names[1]] = tuple[1]
        dict[column_names[2]] = tuple[2]
        dict[column_names[3]] = tuple[3]
        dict[column_names[4]] = tuple[4]
        list_dict.append(dict)
    return list_dict


#Adds the users choice of book to the cart table in the DB.
def cart(isbn, qty):

    user_dict = get_current_user()
    userid = user_dict["userid"]

    if user_dict:
        to_cart_query = '''
        INSERT INTO cart
        (isbn, qty, userid)
        VALUES ( %s, %s, %s )
        '''
        cart_records = [isbn, qty, userid]

        connection.reconnect()
        with connection.cursor() as cursor:
            cursor.executemany(to_cart_query, [cart_records])
            connection.commit()
        print("\nOrder added to cart successfully! ")

        member_menu()


#Lists all books alphabetically and then it allows user to browse books
# by subject and after choosing a subject only 2 books are displayed at a time.
#The user is then given 3 options: put in cart, return to main menu or browse more.
def browse_by_subject():
    subject_list = []

    #This part is to get the subject names and print them out as options for the user.
    select_subject_query = "SELECT DISTINCT subject FROM books ORDER BY subject ASC"
    connection.reconnect()
    with connection.cursor() as cursor:
        cursor.execute(select_subject_query)
        result = cursor.fetchall()
        for row in result:
            subject_list.append(row)
    for i, item in enumerate(subject_list):
        print(f"{i+1}. {item[0]}")

    lowercase_names = [item[0].lower() for item in subject_list]
    choice = int(input("\nEnter your choice: "))  #User selects subject.
    option = lowercase_names[choice - 1]    #Subject name is stored as option based on index in list lowercase_names.
    
    #After user has chosen a subject, this part gets the number of books available on the subject.
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(title) FROM books WHERE subject = %s", (option,))
        nr_books = cursor.fetchone()
        print(f"\n{nr_books[0]} books available on the subject of", option)

    #This part is for getting the books and making a list of dictionaries.
    col_names = ["author", "title", "isbn", "price"]
    book_detail_query = """
    SELECT author, title, isbn, price
    FROM books
    WHERE subject = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(book_detail_query, (option, ))
        result = cursor.fetchall()

    book_dict_list = tuples_to_dict(result, col_names)

    #First checks for the case if there is only 1 book on the subject.
    if len(book_dict_list) == 1:
        book = book_dict_list[0]
        print("\nAuthor:", book['author'])
        print("Title:", book['title'])
        print("ISBN:", book['isbn'])
        print("Price:", book['price'])
        user_choice = input("\nEnter ISBN to add to cart or \nENTER to go back to menu: \n")
        if user_choice != "":
            isbn = int(user_choice)
            quantity = int(input("Enter quantity: "))
            cart(isbn, quantity)
        else:
            member_menu()

    #Then if there are 2 or more it prints 2 at a time.
    else:     
        i = 0
        while i < len(book_dict_list):
            print("\nAuthor:", book_dict_list[i]['author'])
            print("Title:", book_dict_list[i]['title'])
            print("ISBN:", book_dict_list[i]['isbn'])
            print("Price:", book_dict_list[i]['price'])
            i += 1
            if i < len(book_dict_list):
                print("\nAuthor:", book_dict_list[i]['author'])
                print("Title:", book_dict_list[i]['title'])
                print("ISBN:", book_dict_list[i]['isbn'])
                print("Price:", book_dict_list[i]['price'])
                i += 1
            
            if i < len(book_dict_list):
                user_choice = input("\nEnter ISBN to add to cart or \nn ENTER to browse more or \n ENTER to go back to menu: \n")
                if user_choice.lower() != 'n':
                    break
        if user_choice == "":
            member_menu()   
        elif user_choice.isdigit():
            isbn = user_choice
            quantity = int(input("Enter quantity: "))
            cart(isbn, quantity)

#Allows the user to search books by author name or part of his name.
#As well as allowing the user to search by title or part of the title.
def search_by_author():
    option1 = "\n\t1. Author search "
    option2 = "\n\t2. Titile search "
    option3 = "\n\t3. Go back to the main menu "

    print("\n" + option1 + "\n" + option2 + "\n" + option3)
    choice = int(input("\nType in your option: "))

    #This part is for allowing the user to search by author.
    if choice == 1:
        list_books = []
        user_search = input("Enter Author or part of the Author's name: ")
        search_author_query = "SELECT * FROM books WHERE author LIKE '%" + user_search + "%'"
        connection.reconnect()
        with connection.cursor() as cursor:
            cursor.execute(search_author_query)
            result = cursor.fetchall()
            for row in result:
                list_books.append(row)
        print(len(list_books), "books found")

        col_names = ["isbn", "author", "title", "price", "subject"]
        book_dict_list = title_tuples_to_dict(result, col_names)
        
        if len(book_dict_list) == 0:
            user_choice = input("\nENTER to go back to menu: \n")
            if user_choice == "":
                member_menu()
        elif len(book_dict_list) == 1:
            book = book_dict_list[0]
            print("\nAuthor:", book['author'])
            print("Title:", book['title'])
            print("ISBN:", book['isbn'])
            print("Price:", book['price'])
            print("subject:", book['subject'])
            user_choice = input("\nEnter ISBN to add to cart or \nENTER to go back to menu: \n")
            if user_choice != "":
                isbn = int(user_choice)
                quantity = int(input("Enter quantity: "))
                cart(isbn, quantity)
            else:
                member_menu()

        else:     
            i = 0
            while i < len(book_dict_list):
                print("\nAuthor:", book_dict_list[i]['author'])
                print("Title:", book_dict_list[i]['title'])
                print("ISBN:", book_dict_list[i]['isbn'])
                print("Price:", book_dict_list[i]['price'])
                print("Subject:", book_dict_list[i]['subject'])
                i += 1
                if i < len(book_dict_list):
                    print("\nAuthor:", book_dict_list[i]['author'])
                    print("Title:", book_dict_list[i]['title'])
                    print("ISBN:", book_dict_list[i]['isbn'])
                    print("Price:", book_dict_list[i]['price'])
                    print("Subject:", book_dict_list[i]['subject'])
                    i += 1
                    if i < len(book_dict_list):
                        print("\nAuthor:", book_dict_list[i]['author'])
                        print("Title:", book_dict_list[i]['title'])
                        print("ISBN:", book_dict_list[i]['isbn'])
                        print("Price:", book_dict_list[i]['price'])
                        print("Subject:", book_dict_list[i]['subject'])
                        i += 1
                if i < len(book_dict_list) + 1:
                    user_choice = input("\nEnter ISBN to add to cart or \nn ENTER to browse more or \n ENTER to go back to menu: \n")
                    if user_choice.lower() != 'n':
                        break
            if user_choice == "":
                member_menu()   
            elif user_choice.isdigit():
                isbn = user_choice
                quantity = int(input("Enter quantity: "))
                cart(isbn, quantity)            
    #This part is for if the user chooses to search by title.
    elif choice == 2:
        list_books = []
        user_search = input("Enter title or part of the title: ")
        search_title_query = "SELECT * FROM books WHERE title LIKE '%" + user_search + "%'"
        connection.reconnect()
        with connection.cursor() as cursor:
            cursor.execute(search_title_query)
            result = cursor.fetchall()
            for row in result:
                list_books.append(row)
        print(len(list_books), "books found")

        col_names = ["isbn", "author", "title", "price", "subject"]
        book_dict_list = title_tuples_to_dict(result, col_names)
        
        if len(book_dict_list) == 0:
            user_choice = input("\nENTER to go back to menu: \n")
            if user_choice == "":
                member_menu()
        elif len(book_dict_list) == 1:
            book = book_dict_list[0]
            print("\nAuthor:", book['author'])
            print("Title:", book['title'])
            print("ISBN:", book['isbn'])
            print("Price:", book['price'])
            print("subject:", book['subject'])
            user_choice = input("\nEnter ISBN to add to cart or \nENTER to go back to menu: \n")
            if user_choice != "":
                isbn = int(user_choice)
                quantity = int(input("Enter quantity: "))
                cart(isbn, quantity)
            else:
                member_menu()

        else:     
            i = 0
            while i < len(book_dict_list):
                print("\nAuthor:", book_dict_list[i]['author'])
                print("Title:", book_dict_list[i]['title'])
                print("ISBN:", book_dict_list[i]['isbn'])
                print("Price:", book_dict_list[i]['price'])
                print("Subject:", book_dict_list[i]['subject'])
                i += 1
                if i < len(book_dict_list):
                    print("\nAuthor:", book_dict_list[i]['author'])
                    print("Title:", book_dict_list[i]['title'])
                    print("ISBN:", book_dict_list[i]['isbn'])
                    print("Price:", book_dict_list[i]['price'])
                    print("Subject:", book_dict_list[i]['subject'])
                    i += 1
                    if i < len(book_dict_list):
                        print("\nAuthor:", book_dict_list[i]['author'])
                        print("Title:", book_dict_list[i]['title'])
                        print("ISBN:", book_dict_list[i]['isbn'])
                        print("Price:", book_dict_list[i]['price'])
                        print("Subject:", book_dict_list[i]['subject'])
                        i += 1
                if i < len(book_dict_list) + 1:
                    user_choice = input("\nEnter ISBN to add to cart or \nn ENTER to browse more or \n ENTER to go back to menu: \n")
                    if user_choice.lower() != 'n':
                        break
            if user_choice == "":
                member_menu()   
            elif user_choice.isdigit():
                isbn = user_choice
                quantity = int(input("Enter quantity: "))
                cart(isbn, quantity)            
    elif choice == 3:
        member_menu()


#Displays all books that have been added to cart and allows the user to checkout.
def checkout():
    dash = "-"
    print("\nCurrent cart contents: ")
    print("\n{:<15}{:<70}{:<10}{:<10}{:<10}".format("ISBN", "Title", "$",  "Qty", "Total"))
    print(dash * 120)

    user = get_current_user()
    userid = user["userid"]

    get_cart_query = "SELECT isbn, qty FROM cart WHERE userid = " + str(userid)
    connection.reconnect()
    with connection.cursor() as cursor:
        cursor.execute(get_cart_query)
        cart_result = cursor.fetchall()

    final_price = 0
    for row in cart_result:
        isbn, qty = row
        with connection.cursor() as cursor:
            cursor.execute("SELECT title, price FROM books WHERE isbn = %s", (isbn,))
            book_data = cursor.fetchone()
        title, price = book_data
        total = price * qty
        final_price += total

        print("{:<15}{:<70}{:<10}{:<10}{:<10}".format(isbn, title, price, qty, total))
        print(dash * 120)

    proceed = input("Proceed to checkout (Y/N)?: ")

    if proceed.lower() == "y":
        shipment_date = None
        eta_delivery = date.today() + timedelta(days=7)

        to_order_query = '''
        INSERT INTO orders
        (userid, recieved, shipped, shipAddress, shipCity, shipState, shipZip)
        VALUES ( %s, %s, %s, %s, %s, %s, %s )
        '''
        cart_records = [userid, eta_delivery, shipment_date, user["address"], user["city"], user["state"], user["zip"]]

        connection.reconnect()
        with connection.cursor() as cursor:
            cursor.executemany(to_order_query, [cart_records])
            connection.commit()
            

        #Display of the invoice
        get_shipping_details = "SELECT ono FROM orders WHERE userid = " + str(userid)
        connection.reconnect()
        with connection.cursor() as cursor:
            cursor.execute(get_shipping_details)
            result = cursor.fetchall()
            for row in result:
                ono = row[0]
        print("\n\t\t\t\t\t Invoice for Order nr.", ono)
        print("\t\tShipping Adress")
        print("\t\tName: ", "\t" + user["fname"], user["lname"])
        print("\t\tAddress: ", user["address"], "\n\t\t\t  " + user["city"], "\n\t\t\t  " + user["state"], " " + str(user["zip"]) + ("\n"))
        
        print(dash * 120)
        print("{:<15}{:<70}{:<10}{:<10}{:<10}".format("ISBN", "Title", "$",  "Qty", "Total"))
        print(dash * 120)
        final_price = 0
        for row in cart_result:
            isbn, qty = row
            with connection.cursor() as cursor:
                cursor.execute("SELECT title, price FROM books WHERE isbn = %s", (isbn,))
                book_data = cursor.fetchone()
            title, price = book_data
            total = price * qty
            final_price += total

            print("{:<15}{:<70}{:<10}{:<10}{:<10}".format(isbn, title, price, qty, total))
            print(dash * 120)
        print("{:<105}{:<10}".format("Total = ", final_price) + "\n")

        print("Estimated date of delivery: ", eta_delivery)

        #Removing order and emptying cart from database once it has gone through
        delete_cart_query = "DELETE FROM cart WHERE userid = %s"
        delete_orders_query = "DELETE FROM orders WHERE userid = %s"

        with connection.cursor() as cursor:
            cursor.execute(delete_cart_query, (userid,))
            cursor.execute(delete_orders_query, (userid,))
        connection.commit()

        back_to_menu = input("\nEnter to back to menu: ")
        if back_to_menu == "":
            main_menu()
        

    else:
        member_menu()


#Starts the program and runs the main menu of the UI
def main_menu():
    startup_graphic()
    option1 = "\n\t1. Member Login"
    option2 = "\n\t2. New Member Registration"
    option3 = "\n\t3. Quit"

    print("\n" + option1 + "\n" + option2 + "\n" + option3)
    choice = int(input("\nType in your option: "))

    if choice == 1:
        while True:
            logged_in = login()
            if logged_in:
                member_menu()
                break
    elif choice == 2:
        member_registration()
        print("\nYou have registered successfully!")
        input("Press Enter to go back to the main menu")
        main_menu()
    elif choice == 3:
       print("\nSession has ended. ")
       connection.close()
       quit()


main_menu()

if connection is not None:
    connection.close()