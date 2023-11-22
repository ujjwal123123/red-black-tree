#!/usr/bin/env python3

from tree import Tree
from heap import Heap
import time
import sys


class NodeData:
    """
    Represents the data of a book node in the library.

    Attributes:
        book_id (int): The ID of the book.
        book_name (str): The name of the book.
        author_name (str): The name of the author.
        is_available (bool): Indicates if the book is available for borrowing.
        borrowed_by (int | None): The ID of the borrower, or None if not borrowed.
        reservation_heap (Heap): The heap containing the reservations for the book.
    """

    def __init__(
        self, book_id: int, book_name: str, author_name: str, is_available: bool
    ) -> None:
        self.book_id: int = book_id
        self.book_name: str = book_name
        self.author_name: str = author_name
        self.is_available: bool = is_available
        self.borrowed_by: int | None = None
        self.reservation_heap: Heap = Heap()

    def __str__(self) -> str:
        """
        Returns a string representation of the Book object.
        """
        ret = []
        ret.append(f"BookID = {self.book_id}")
        ret.append(f'Title = "{self.book_name}"')
        ret.append(f'Author = "{self.author_name}"')
        if self.is_available:
            ret.append('Availability = "Yes"')
        else:
            ret.append('Availability = "No"')
        ret.append(f"BorrowedBy = {self.borrowed_by}")
        ret.append(f"Reservations = {self.reservation_heap.__str__()}")

        return "\n".join(ret)


tree = Tree()


def PrintBook(bookId: int):
    """
    Prints the details of a book based on its ID.

    Parameters:
    bookId (int): The ID of the book to be printed.
    """
    book = tree.search(bookId)
    if book is None:
        print(f"Book {bookId} not found in the Library")
    else:
        print(book.data)
    print()


def BorrowBook(patronID: int, bookID: int, patronPriority: int):
    """
    Borrow a book from the library.

    Args:
    - patronID (int): The ID of the patron borrowing the book.
    - bookID (int): The ID of the book being borrowed.
    - patronPriority (int): The priority of the patron.
    """
    book = tree.search(bookID)
    assert book is not None

    bookdata: NodeData = book.data
    if bookdata.is_available:
        bookdata.is_available = False
        bookdata.borrowed_by = patronID
        print(f"Book {book.key} Borrowed by Patron {patronID}")
    else:
        reservation_heap = bookdata.reservation_heap
        reservation_heap.push((patronPriority, time.time(), patronID))
        print(f"Book {book.key} Reserved by Patron {patronID}")
    print()


def InsertBook(
    bookID: int,
    bookName: str,
    authorName: str,
    availablilityStatus: str,
):
    """
    Inserts a book into the library.

    Parameters:
    - bookID (int): The ID of the book.
    - bookName (str): The name of the book.
    - authorName (str): The name of the author.
    - availablilityStatus (str): The availability status of the book ("Yes" or "No").
    """
    is_available: bool = True if availablilityStatus == "Yes" else False
    node_data = NodeData(bookID, bookName, authorName, is_available)
    tree.insert(bookID, node_data)


def ReturnBook(patronID: int, bookID: int):
    """
    Returns a book to the library and updates its availability status.

    Args:
    - patronID (int): The ID of the patron returning the book.
    - bookID (int): The ID of the book being returned.

    """
    book = tree.search(bookID)
    assert book is not None
    bookdata = book.data
    bookdata.is_available = True
    bookdata.borrowed_by = None
    print(f"Book {bookID} Returned by Patron {patronID}", end="\n\n")

    if bookdata.reservation_heap:
        priority, time, patronID = bookdata.reservation_heap.pop()
        bookdata.is_available = False
        bookdata.borrowed_by = patronID
        print(f"Book {bookID} Allotted to Patron {patronID}", end="\n\n")


def FindClosestBook(bookID: int):
    """
    Finds the closest books to the given bookID and prints the data of the closest books.

    Parameters:
    - bookID (int): The ID of the book to find the closest books for.
    """
    books = tree.find_closest(bookID)

    for book in books:
        print(book.data)
        print()


def DeleteBook(bookID: int):
    """
    Deletes a book from the library.

    Parameters:
    - bookID (int): The ID of the book to be deleted.
    """
    book = tree.search(bookID)
    assert book is not None
    reservation_heap = book.data.reservation_heap
    tree.delete(bookID)
    print(f"Book {bookID} is no longer available", end="")

    if reservation_heap:
        patrons = []
        while reservation_heap:
            priority, time, patronID = reservation_heap.pop()
            patrons.append(patronID)
        if len(patrons) == 1:
            print(f". Reservation made by Patron {patrons[0]} has been cancelled!")
        else:
            print(
                f". Reservations made by Patrons {', '.join(map(str, patrons))} have been cancelled!"
            )
    else:
        print()
    print()


def Quit():
    """
    Terminates the program and prints a message.
    """
    print("Program Terminated!!")

    tree.visualize_binary_tree("tree")
    exit()


def ColorFlipCount():
    """
    Prints the color flip count of the tree.

    This function prints the color flip count of the tree.
    """
    print(f"Color Flip Count: {tree.flip_count}\n")


def PrintBooks(bookID1: int, bookID2: int):
    """
    Prints the books within the range of book IDs specified.

    Parameters:
    bookID1 (int): The starting book ID of the range.
    bookID2 (int): The ending book ID of the range.
    """
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
