import { Component, OnInit } from '@angular/core';
import { Book } from '../book';
import { BookService } from '../book.service';

@Component({
  selector: 'app-books',
  templateUrl: './books.component.html'
})
export class BooksComponent implements OnInit {

  books: Book[];
  activeBook: Book;

  constructor(private bookService: BookService) { }

  ngOnInit() {
    this.bookService.getBooks().subscribe(books => this.books = books);
  }

  onSubmitBook(book: Book) {
    if (book.uid) {
      this.bookService.updateBook(book).subscribe(response => {
      });
    } else {
      this.bookService.addBook(book).subscribe(response => {
        if (response.ok && response.body.id) {
          book.uid = response.body.id;
          this.books.push(book);
        }
      });
    }
    this.setActiveBook(null);
  }

  setActiveBook(book: Book) {
    this.activeBook = book;
  }

  onSelectBook(book: Book) {
    this.setActiveBook(book);
  }

  onClose(event: any) {
    this.setActiveBook(null);
  }

  addNewBook() {
    this.setActiveBook({} as Book);
  }

}
