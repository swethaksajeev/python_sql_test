import mysql.connector


def db_connection():
    try:
        connection = mysql.connector.connect(host="localhost",user="root",password="root",database="library_management")
        print('successful connection')
        return connection

    except Exception:
        print("database connection failed")
        return None
db_connection()


def add_book():
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    category = input("Enter Category: ")
    total_copies = int(input("Enter Total Copies: "))
    available_copies = int(input("Enter Available Copies: "))
    if total_copies < 0 or available_copies < 0:
        print("copies cannot be negative")
        return

    if available_copies > total_copies:
        print("available copies cannot be more than total copies")
        return
    conn = db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        query = "insert into books (title, author, category, total_copies, available_copies) values (%s, %s, %s, %s, %s)"
        data = (title, author, category, total_copies, available_copies)
        cursor.execute(query, data)
        conn.commit()
        print("Book added successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        print("Failed to add book:", e)


def view_available_books():
    conn = db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        query = "select * from books where available_copies > 0 order by title asc limit 20"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("no records found")
        cursor.close()
        conn.close()
    except Exception as e:
        print("failed to view books:", e)


def delete_book():
    try:
        book_id = int(input("Enter Book id to delete: "))
    except ValueError:
        print("Please enter a valid Book id :")
        return

    confirm = input("are you sure you want to delete this book? (yes/no): ")
    if confirm != "yes":
        print("no deletion")
        return

    conn = db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("delete from books where book_id = %s", (book_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Book deleted successfully")
        else:
            print("Book not found")
        cursor.close()
        conn.close()
    except Exception as e:
        print("failed to delete book:", e)

def library_summary():
    conn = db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("select count(*), sum(available_copies), avg(total_copies) from books")
        total_books, total_available, avg_copies = cursor.fetchone()
        print("Total books:", total_books)
        print("Total available copies:", total_available)
        print("Average total copies per book:", avg_copies)
        cursor.close()
        conn.close()
    except Exception as e:
        print("failed to get summary:", e)

def update_available_copies():
    try:
        book_id = int(input("Enter Book id: "))
        new_available = int(input("Enter the new available copies: "))
    except ValueError:
        print("please enter valid numbers")
        return

    if new_available < 0:
        print("available copies cannot be negative")
        return

    conn = db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("select total_copies from books where book_id = %s", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print("Book not found")
            return

        total_copies, = row
        if new_available > total_copies:
            print("Available copies cannot be more than total copies.")
            return

        cursor.execute(
            "update books set available_copies = %s where book_id = %s",
            (new_available, book_id)
        )
        conn.commit()
        print("available copies are updated successfully")

        cursor.close()
        conn.close()
    except Exception as e:
        print("failed to update:", e)


def search_book():
    print("1.Search a book by id")
    print("2. Search using Title or Author")
    choice = int(input("Enter choice (1 or 2): "))

    category = input("Enter Category to filter:")
    conn = db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        if choice == 1:
            try:
                book_id = int(input("Enter Book id: "))
            except ValueError:
                print("enter valid book id")
                return
            if category != "":
                query = "select * from books where book_id = %s and category = %s"
                data = (book_id, category)
            else:
                query = "select * from books where book_id = %s"
                data = (book_id,)

        elif choice == 2:
            keyword = input("Enter part of Title or Author: ")
            like_text = "%" + keyword + "%"

            if category != "":
                query = "select * from books where (title like %s or author like %s) and category = %s"
                data = (like_text, like_text, category)
            else:
                query = "select * from books where title like %s or author like %s"
                data = (like_text, like_text)
        else:
            print("Invalid choice.")
            return

        cursor.execute(query, data)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("no records found")
        cursor.close()
        conn.close()
    except Exception as e:
        print("search Failed:", e)


while True:
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. View Available Books")
    print("3. Search Book")
    print("4. Update Available Copies")
    print("5. Delete Book")
    print("6. Library Summary")
    print("7. Exit")

    try:
        choice = int(input("Enter choice (1-7): "))
    except ValueError:
        print("Please enter a number from 1 to 7.")
        continue

    if choice == 1:
        add_book()
    elif choice == 2:
        view_available_books()
    elif choice == 3:
        search_book()
    elif choice == 4:
        update_available_copies()
    elif choice == 5:
        delete_book()
    elif choice == 6:
        library_summary()
    elif choice == 7:
        print("Exiting...")
        break
    else:
        print("Invalid choice.")


