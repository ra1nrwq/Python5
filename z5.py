import json
from typing import List, Optional


class Book:
    def __init__(self, title: str, author: str, year: int, genre: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) - {self.genre}"

    def __eq__(self, other):
        return isinstance(other, Book) and self.title == other.title and self.author == other.author


class Reader:
    def __init__(self, name: str, reader_id: int):
        self.name = name
        self.reader_id = reader_id
        self.borrowed_books: List[Book] = []

    def borrow_book(self, book: Book):
        self.borrowed_books.append(book)

    def return_book(self, book: Book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
        else:
            raise ValueError("Читатель не брал эту книгу.")

    def __str__(self):
        return f"{self.name} (ID: {self.reader_id}), Взятые книги: {', '.join(str(book) for book in self.borrowed_books)}"


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: List[Book] = []
        self.readers: List[Reader] = []

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, book: Book):
        if book in self.books:
            self.books.remove(book)
        else:
            raise ValueError("Книга не найдена в библиотеке.")

    def register_reader(self, reader: Reader):
        if any(r.reader_id == reader.reader_id for r in self.readers):
            raise ValueError("Читатель с таким ID уже зарегистрирован.")
        self.readers.append(reader)

    def lend_book(self, reader_id: int, book_title: str):
        reader = self._find_reader_by_id(reader_id)
        book = next((b for b in self.books if b.title == book_title), None)
        if book:
            reader.borrow_book(book)
            self.books.remove(book)
        else:
            raise ValueError("Книга недоступна для выдачи.")

    def return_book(self, reader_id: int, book_title: str):
        reader = self._find_reader_by_id(reader_id)
        book = next((b for b in reader.borrowed_books if b.title == book_title), None)
        if book:
            reader.return_book(book)
            self.books.append(book)
        else:
            raise ValueError("Читатель не имеет эту книгу.")

    def find_book(self, title: str, author: Optional[str] = None) -> Optional[Book]:
        for book in self.books:
            if book.title == title and (author is None or book.author == author):
                return book
        return None

    def get_reader_books(self, reader_id: int) -> List[Book]:
        reader = self._find_reader_by_id(reader_id)
        return reader.borrowed_books

    def _find_reader_by_id(self, reader_id: int) -> Reader:
        reader = next((r for r in self.readers if r.reader_id == reader_id), None)
        if reader:
            return reader
        else:
            raise ValueError("Читатель с указанным ID не найден.")

    def save_to_file(self, filename: str):
        data = {
            "library": self.name,
            "books": [{"title": b.title, "author": b.author, "year": b.year, "genre": b.genre} for b in self.books],
            "readers": [
                {
                    "name": r.name,
                    "reader_id": r.reader_id,
                    "borrowed_books": [{"title": b.title, "author": b.author, "year": b.year, "genre": b.genre} for b in r.borrowed_books]
                }
                for r in self.readers
            ]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.name = data["library"]
        self.books = [Book(b["title"], b["author"], b["year"], b["genre"]) for b in data["books"]]
        self.readers = [Reader(r["name"], r["reader_id"]) for r in data["readers"]]
        for reader_data, reader in zip(data["readers"], self.readers):
            reader.borrowed_books = [Book(b["title"], b["author"], b["year"], b["genre"]) for b in reader_data["borrowed_books"]]


def main():
    library = Library("Central Library")
    
    while True:
        print("\n--- Библиотека ---")
        print("1. Добавить книгу")
        print("2. Зарегистрировать читателя")
        print("3. Выдать книгу читателю")
        print("4. Вернуть книгу")
        print("5. Показать книги читателя")
        print("6. Сохранить данные в файл")
        print("7. Загрузить данные из файла")
        print("8. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            genre = input("Введите жанр книги: ")
            library.add_book(Book(title, author, year, genre))
            print("Книга добавлена.")
        
        elif choice == "2":
            name = input("Введите имя читателя: ")
            reader_id = int(input("Введите ID читателя: "))
            try:
                library.register_reader(Reader(name, reader_id))
                print("Читатель зарегистрирован.")
            except ValueError as e:
                print(e)
        
        elif choice == "3":
            reader_id = int(input("Введите ID читателя: "))
            book_title = input("Введите название книги: ")
            try:
                library.lend_book(reader_id, book_title)
                print("Книга выдана.")
            except ValueError as e:
                print(e)
        
        elif choice == "4":
            reader_id = int(input("Введите ID читателя: "))
            book_title = input("Введите название книги: ")
            try:
                library.return_book(reader_id, book_title)
                print("Книга возвращена.")
            except ValueError as e:
                print(e)
        
        elif choice == "5":
            reader_id = int(input("Введите ID читателя: "))
            try:
                books = library.get_reader_books(reader_id)
                print("Книги читателя:")
                for book in books:
                    print(book)
            except ValueError as e:
                print(e)
        
        elif choice == "6":
            filename = input("Введите имя файла для сохранения: ")
            library.save_to_file(filename)
            print("Данные сохранены.")
        
        elif choice == "7":
            filename = input("Введите имя файла для загрузки: ")
            try:
                library.load_from_file(filename)
                print("Данные загружены.")
            except FileNotFoundError:
                print("Файл не найден.")
        
        elif choice == "8":
            print("Выход.")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
