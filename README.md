# Book-Store-Management-System
Book Store management System that is using SQLite to store data

This program is a basic console-based library management system that allows the user to perform various operations on a collection of books.

The program starts by defining several functions that correspond to the different operations that can be performed on the book collection, including adding a book, updating a book, deleting a book, and searching for a book.

Each of these options is implemented as a separate function that interacts with the SQL database. When a user selects an option from the menu, the program uses a try-except block to handle any errors that might occur while processing the user's input. If the user enters a valid choice, the corresponding function is called to perform the requested action.

The program's use of an SQL database system allows it to store and retrieve large amounts of data efficiently. By separating the data into discrete fields (e.g., title, author, and Qty), the program can easily search, sort, and filter the collection based on user input. This makes it a useful tool for managing book collections of any size.

Overall, this program provides a basic framework for a library management system and can be expanded upon to include additional features and functionality.
