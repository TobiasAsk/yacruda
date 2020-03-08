import { Component, OnInit } from '@angular/core';
import { Book } from '../book';
import { BookService } from '../book.service';

@Component({
  selector: 'app-books',
  templateUrl: './books.component.html'
})
export class BooksComponent implements OnInit {

  books: Book[];
  showingEditor: boolean;
  activeBook: Book;

  constructor(private bookService: BookService) { }

  ngOnInit() {
    this.bookService.getBooks().subscribe(books => this.books = books);
    this.resetActiveBook();
  }

  submitBook() {
    if (this.activeBook.uid) {
      this.bookService.updateBook(this.activeBook).subscribe(response => {
        if (response.ok) {
          const oldBook = this.books.find(b => b.uid == this.activeBook.uid);
          Object.assign(oldBook, this.activeBook);
          this.hideBookEditor();
        }
      });
    } else {
      this.bookService.addBook(this.activeBook).subscribe(response => {
        if (response.ok && response.body.id) {
          this.activeBook.uid = response.body.id;
          this.books.push(this.activeBook);
          this.hideBookEditor();
        }
      });
    }
  }

  hideBookEditor() {
    this.resetActiveBook();
    this.showingEditor = false;
  }

  showBookEditor() {
    this.showingEditor = true;
  }

  resetActiveBook() {
    this.activeBook = {

    } as Book;
  }

  onSelectBook(book: Book) {
    this.activeBook = JSON.parse(JSON.stringify(book));
    this.showBookEditor();
  }

}
