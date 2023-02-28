# importing database module
import sqlite3
# connecting ebookstore database to my program
with sqlite3.connect("ebookstore.db") as db:
    # creating cursor so we can manipulate database
    cursor = db.cursor()

    try:
        cursor.execute('''DROP TABLE IF EXISTS books''')
        #creating database with id,title,author and qty attributes
        cursor.execute('''CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        qty INT NOT NULL
        )''')
        # data that will use to pupulate database            
        book_data = [(3002, 'Harry Potter and the Philosopher\'','J.K.Rowling',40),
                        (3003, 'The Lion,the Witch and the Wardrobe','C.S. Lewis',25),
                        (3004, 'The Lord of the Rings','J.R.R. Tolkien',37),
                        (3005, 'Alice in Wonderland','Lewis Carroll',12)]

        # inserting data into a database using executmany method that inserts more records at once
        cursor.executemany('''
                INSERT INTO books(id,title,author,qty)
                VALUES(?,?,?,?)
        '''     ,book_data)
        # commiting changes
        db.commit()
        print("Data inserted sucessfully")
    # handling any database errors and going back to previous stable state with rollback method
    except sqlite3.Error as error:
        print("Error occured: ", error)
        db.rollback()

# Define a function to add a new book to the database
    def add_book():
        while True:
            title = input("Enter the book title: ")
            author = input("Enter the book author: ")
            qty = int(input("Enter the quantity of books: "))
            # handling value error
            try:
                qty = int(qty)
            except ValueError:
                print("Quantity must be a whole number.")
            
            # handling any error that can occur while trying to insert new book record
            try:
                mycursor = db.cursor()
                sql ='''INSERT INTO books (title, author, qty) VALUES (?, ?, ?)'''
                val = (title, author, qty)
                mycursor.execute(sql, val)
                # commiting changes to database
                db.commit()
                # rowcount function is counting how many records is changed within our database and we use it to record how many books is added
                print(mycursor.rowcount, "book added to the database.")
                break
            # handling possible errors
            except Exception as e:
                print("An error appeared while adding a book,",e)

# Function to update a book in the database
    def update_book():
        while True:
            # asking user to enter ID for book they want to update
            book_id = int(input("Enter the book ID: "))
            # handling value error
            try:
                book_id = int(book_id)
            except ValueError:
                print("BookID must be an integer,please try again.")
                continue

            mycursor = db.cursor()
            # making sure that there is record in the databse for the ID user entered
            sql = '''SELECT * FROM books WHERE id = ?'''
            val = (book_id,)
            mycursor.execute(sql,val)
            result = mycursor.fetchone()
            # if ID user entered is not valid we will print error and return user back to enter ID
            if result is None:
                print("Book with ID,",book_id,"not found,please try again.")
                continue
            # asking user to enter new title author and quantity to be updated or 'space' if they want to keep some information same and change only certain information for the record
            new_title = input("Enter the new book title (leave blank to keep current title): ")
            new_author = input("Enter the new book author (leave blank to keep current author): ")
            new_qty = input("Enter the new quantity of books (leave blank to keep current quantity): ")

            mycursor = db.cursor()
            # variable that we will use to exicute query to our database based on the ID for the record
            sql = '''UPDATE books SET title = ?, author = ?, qty = ? WHERE id = ?'''

        # Build the tuple of values to update
        # checking if user entered a value or left a blank space
            val = ()
            # if user entered value we are adding that value to the tuple we use as a part of the query
            if new_title != '':
                val += (new_title,)
            # if user left blank space we are getting record from database that has ID of the book we want to update
            else:
                mycursor.execute('''SELECT title FROM books WHERE id = ?''', (book_id,))
                # taking title from the record and assigning it to our tuple list
                new_title = mycursor.fetchone()[0]
                val += (new_title,)
            # if user enters new author we add it to our tuple
            if new_author != '':
                val += (new_author,)
            # if user doesn't enter author
            else:
                # getting recor for the author with ID of the book we are trying to update
                mycursor.execute('''SELECT author FROM books WHERE id = ?''', (book_id,))
                # fetching author for that record and adding author to the tuple
                new_author = mycursor.fetchone()[0]
                val += (new_author,)
            # checking if user entered new quantity
            if new_qty != '':
                # handling value error
                try:
                    int(new_qty)
                except ValueError:
                    print("Quantity must be an integer,pleaase try again")
                val += (new_qty,)
            else:
                # if user didn't enter quantity we are getting record based on the ID for book we want to update
                mycursor.execute('''SELECT qty FROM books WHERE id = ?''', (book_id,))
                # getting quantity from the record and adding it to a tuple
                new_qty = mycursor.fetchone()[0]
                val += (new_qty,)
            # book ID that we need in order to know which record to update
            val += (book_id,)
            try:
                # updating database
                mycursor.execute(sql, val)
                #commiting changes
                db.commit()
                # getting confirmation that update was successful
                print(mycursor.rowcount, "book updated in the database.")
                break
            # handling errors
            except Exception as e:
                print("An Error occured while updating a book",e)

    # function to delete a book from the database based on ID(primary key)
    def delete_book():
        while True:
            book_id = int(input("Enter the book ID: "))
            try:
                book_id = int(book_id)
            except ValueError:
                print("BookID must be an integer,please try again.")
                continue
        

            mycursor = db.cursor()
            # selecting book with the ID of the book user wants to delete to make sure record with that ID exists
            sql = '''SELECT * FROM books WHERE id = ?'''
            val = (book_id,)
            mycursor.execute(sql,val)
            # fetching record we want to delete
            result = mycursor.fetchone()

            # if there is no record with that ID we let user know and ask to enter ID again
            if result is None:
                print("Book with ID,",book_id,"not found,please try again.")
                continue
            # if record exists we delete that record from the database
            sql = '''DELETE FROM books WHERE id = ?'''
            val = (book_id,)
            try:
                # deleting record
                mycursor.execute(sql, val)
                # commiting changes
                db.commit()
                # printing confirmation that record was successfuly deleted
                print(mycursor.rowcount, "book deleted from the database.")
                break
            # handling errors
            except Exception as e:
                print("An error occured while trying to delete book",e)

    # function to search for a book in the database
    def search():
        try:
            # asking user to enter keyword to search for the record
            keyword = input("Enter a keyword to search for: ")

            mycursor = db.cursor()
            # selecting all records from the database where title or author contain keyword 
            sql = '''SELECT * FROM books WHERE title LIKE ? OR author LIKE ?'''
            # placeholders for title and author that will be populated keyword in order to compare with database records
            val = val = (f"%{keyword}%", f"%{keyword}%")
            mycursor.execute(sql, val)
            # fetching records as list of tuples 
            result = mycursor.fetchall()
            # checking if there is any search results
            if len(result) == 0:
                # printing message for the user if there is no books they are searchng for
                print(f"No books found with keyword '{keyword}'.")
            else:
                # printing all records that contain author or title user is interested in
                print("Search results:\n")
                # iterating through books and for each book displaying information in friendly manner
                for book in result:
                    print(f"ID: {book[0]}\nTitle: {book[1]}\nAuthor: {book[2]}\nQuantity: {book[3]}\n")
                    # handling errors
        except sqlite3.Error as error:
            print("An error occured",error)


# Function to display the menu for the user

    def menu():
        # menu with options
        while True:
            print("Select an option:\n")
            print("1: Add a book")
            print("2: Update a book")
            print("3: Delete a book")
            print("4: Search for a book")
            print("5: Exit\n")
            # based on the option user chose we are triggering functions defined above
            try:
                # asking user to enter choice
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    # calling func that is adding book
                    add_book()
                elif choice == 2:
                    # calling func that is updating book
                    update_book()
                elif choice == 3:
                    # func that is deleting book
                    delete_book()
                elif choice == 4:
                    # func that is searching for books
                    search()
                    # option to exit program
                elif choice == 5:
                    print("Exiting program...")
                    break
                # handling invalid choice from the user
                else:
                    print("Invalid choice, please try again.")
                # handling value error in case user enters wrong data-type
            except ValueError:
                print("Invalid choice, please enter a number.")


# calling main function to start a program
menu()