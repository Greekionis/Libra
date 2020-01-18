"""
SQL-functions
"""

import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()


def show_all():
    cursor.execute("Select * FROM books ORDER BY title")
    return cursor.fetchall()


def search(param, strg):
    sql = f"Select * FROM books WHERE {param} LIKE lower('%{strg}%')"
    cursor.execute(sql)
    return cursor.fetchall()


def edit_book(title, author, release_date, publisher, isbn, old_isbn):
    sql = "UPDATE books SET title = ?, author = ?, release_date = ?, publisher = ?, isbn = ? where isbn = ?"
    val = (title, author, release_date, publisher, isbn, old_isbn)
    cursor.execute(sql, val)
    conn.commit()
    return True


def add_book(title, author, release_date, publisher, isbn):
    sql = f"Select * FROM books WHERE isbn LIKE lower('%{isbn}%')"
    cursor.execute(sql)
    if cursor.fetchone() is None:
        sql = "INSERT INTO books (title, author, release_date, publisher, isbn) values (?,?,?,?,?)"
        val = (title, author, release_date, publisher, isbn)
        cursor.execute(sql, val)
        conn.commit()
        return True


def upload_book(title, author, release_date, publisher, isbn):
    sql = f"Select * FROM books WHERE isbn LIKE lower('%{isbn}%')"
    cursor.execute(sql)
    if cursor.fetchone() is None:
        sql = "INSERT INTO books (title, author, release_date, publisher, isbn) values (?,?,?,?,?)"
        val = (title, author, release_date, publisher, isbn)
        cursor.execute(sql, val)
        conn.commit()
        return author, title

def del_book(cur_isbn):
    sql = f"DELETE FROM books WHERE isbn LIKE lower('%{cur_isbn}%')"
    cursor.execute(sql)
    conn.commit()
    return True


def close_conn():
    cursor.close()
