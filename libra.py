"""
Console SQLite-library
"""
import json
import sql_actions


search_params_sys = {1: "title", 2: "author", 3: "release_date", 4: "publisher"}
search_params_user = {1: "title", 2: "author", 3: "release date", 4: "publisher"}
msg_start = """1 - Show all books
2 - Search
3 - Edit or Delete
4 - Add book
5 - Download book info
6 - Upload book info
7 - Exit"""
msg_edit = """Search by
1 - Title
2 - Author
3 - Release date
4 - Publisher"""


def pr_show():
    return sql_actions.show_all()


def pr_search():
    print(msg_edit)
    param = input("Enter: ")
    if param != "":
        strg = (input(f"Enter string for search by {search_params_user[int(param)]}: "))
        return sql_actions.search(search_params_sys[int(param)], strg)



def pr_edit_or_del(finded_books):
    cur_title = finded_books[0][0]
    cur_author = finded_books[0][1]
    cur_r_date = finded_books[0][2]
    cur_publisher = finded_books[0][3]
    cur_isbn = finded_books[0][4]
    print(f"Found: {cur_author} - {cur_title}")
    edit_del = (input("Edit(E) or Delete(D)? (E/D): ")).lower()

    if edit_del == "e":
        edit_title = input(f"Title (current is '{cur_title}') : ")
        if edit_title == "":
            edit_title = cur_title
        edit_author = input(f"Author (current is '{cur_author}') : ")
        if edit_author == "":
            edit_author = cur_author
        edit_date = input(f"Release date (current is '{cur_r_date}') : ")
        if edit_date == "":
            edit_date = cur_r_date
        edit_publisher = input(f"Publisher (current is '{cur_publisher}') : ")
        if edit_publisher == "":
            edit_publisher = cur_publisher
        edit_isbn = input(f"ISBN (current is '{cur_isbn}') : ")
        if edit_isbn == "":
            edit_isbn = cur_isbn
        if sql_actions.edit_book(title=edit_title, author=edit_author, release_date=edit_date,
                              publisher=edit_publisher, isbn=edit_isbn, old_isbn=cur_isbn) is True:
            print("Info updated!")
    elif edit_del == "d":
        if sql_actions.del_book(cur_isbn) is True:
            print("Deleted!")


def pr_add_book():
    print("Add new book:")
    new_title = input("Title: ")
    new_author = input("Author : ")
    new_date = input("Release date: ")
    new_publisher = input("Publisher: ")
    new_isbn = input("ISBN: ")
    if new_isbn != "":
        if sql_actions.add_book(title=new_title, author=new_author, release_date=new_date,
                         publisher=new_publisher, isbn=new_isbn) is True:
            print("Book added!")
        else:
            print("Book already have!")
    else:
        print("Empty ISBN, book not added!")


def pr_download_book(downloaded_books):

    #if len(downloaded_books) > 0:
    if downloaded_books is not None:
        up = {}
        items = len(downloaded_books[0])    # Количество параметров книги
        for book in downloaded_books:
            up.update({book[items - 1]: book[0: items - 1]})        # {ISBN : Все остальные параметры}
        with open("download.txt", "w", encoding='utf-8') as d_file:
            json.dump(up, d_file, ensure_ascii=False)
        print("Downloaded books: {}".format(len(up)))
        print("---")
    else:
        print("Downloaded books: 0")
        print("---")


def pr_upload_book():
    with open("upload.txt", "r", encoding='utf-8') as d_file:
        books = json.load(d_file)

    for k, v in books.items():
        try:
            res = sql_actions.upload_book(v[0], v[1], v[2], v[3], k)
            print("Uploaded: {} - {}".format(res[0], res[1]))
        except TypeError as e:
            print("Upload Error!")
    print("---")


def primary():
    print(msg_start)
    act = input("Enter: ")

    if act == "1":
        all_books = pr_show()
        for i in range(len(all_books)):
            print(all_books[i])
        primary()
    elif act == "2":
        search_res = pr_search()
        if search_res is not None:
            for i in range(len(search_res)):
                print(search_res[i])
        else:
            print("Try again!")
            print("---")
        primary()
    elif act == "3":
        finded_books = pr_search()
        if len(finded_books) == 1:
            pr_edit_or_del(finded_books)
        else:
            for i in range(len(finded_books)):
                print("№ {} - {}".format(str(i + 1), finded_books[i]))
            num_for_edit = input("Found more than 1 book, specify №: ")
            pr_edit_or_del([finded_books[int(num_for_edit) - 1]])
        primary()
    elif act == "4":
        pr_add_book()
        primary()
    elif act == "5":
        downloaded_books = pr_search()
        pr_download_book(downloaded_books)
        primary()
    elif act == "6":
        pr_upload_book()
        primary()
    elif act == "7":
        sql_actions.close_conn()
        exit()


if __name__ == "__main__":
    primary()
