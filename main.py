from tree import Tree, NodeData
import time
import sys

tree = Tree()


def my_print(*args, end="\n"):
    # print("\033[95m", end="")
    print(*args, end=end)
    # print("\033[0m", end="")


def PrintBook(bookId: int):
    book = tree.search(bookId)
    assert book is not None
    if book is None:
        my_print(f"Book {bookId} not found in the Library")
    else:
        my_print(book.data)
    my_print()


def BorrowBook(patronID: int, bookID: int, patronPriority: int):
    book = tree.search(bookID)
    assert book is not None

    bookdata: NodeData = book.data
    if bookdata.is_available:
        bookdata.is_available = False
        bookdata.borrowed_by = patronID
        my_print(f"Book {book.key} Borrowed by Patron {patronID}")
    else:
        reservation_heap = bookdata.reservation_heap
        reservation_heap.push((patronPriority, time.time(), patronID))
        my_print(f"Book {book.key} Reserved by Patron {patronID}")
    print()


def InsertBook(
    bookID: int,
    bookName: str,
    authorName: str,
    availablilityStatus: str,
):
    is_available: bool = True if availablilityStatus == "Yes" else False
    node_data = NodeData(bookID, bookName, authorName, is_available)
    tree.insert(bookID, node_data)


def ReturnBook(patronID: int, bookID: int):
    book = tree.search(bookID)
    assert book is not None
    bookdata = book.data
    bookdata.is_available = True
    bookdata.borrowed_by = None
    my_print(f"Book {bookID} Returned by Patron {patronID}", end="\n\n")

    if bookdata.reservation_heap:
        priority, time, patronID = bookdata.reservation_heap.pop()
        bookdata.is_available = False
        bookdata.borrowed_by = patronID
        my_print(f"Book {bookID} Allotted to Patron {patronID}", end="\n\n")


def FindClosestBook(bookID: int):
    books = tree.find_closest(bookID)

    for book in books:
        my_print(book.data)
        print()

    tree.visualize_binary_tree("before")


def DeleteBook(bookID: int):
    book = tree.search(bookID)
    assert book is not None
    reservation_heap = book.data.reservation_heap
    tree.delete(bookID)
    my_print(f"Book {bookID} is no longer available.", end="")

    if reservation_heap:
        patrons = []
        while reservation_heap:
            priority, time, patronID = reservation_heap.pop()
            patrons.append(patronID)
        if len(patrons) == 1:
            my_print(f" Reservation made by Patron {patrons[0]} has been cancelled!")
        else:
            my_print(
                f" Reservations made by Patrons {', '.join(map(str, patrons))} have been cancelled!"
            )
    else:
        my_print()
    print()


def Quit():
    my_print("Program Terminated!!")
    exit()


def ColorFlipCount():
    print("Color Flip Count: not implemented yet\n")


def PrintBooks(bookID1: int, bookID2: int):
    nodes = tree.range_search(bookID1, bookID2)
    for node in nodes:
        PrintBook(node.key)


if len(sys.argv) > 1:
    filename = sys.argv[1]
    input_file = open(filename, "r")

    # output_filename: str = str(filename.split(".")[0] + "_output_file.txt")
    output_filename = str(filename) + "_output_file.txt"
    sys.stdout = open(output_filename, "w")
else:
    input_file = sys.stdin

for command in input_file.readlines():
    exec(command)
sys.stdout.close()
