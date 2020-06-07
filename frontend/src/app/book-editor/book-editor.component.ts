import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Book } from '../book';
import { FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-book-editor',
  templateUrl: './book-editor.component.html'
})
export class BookEditorComponent implements OnInit {

  bookForm: FormGroup;

  @Input() book: Book;
  @Output() close: EventEmitter<any> = new EventEmitter();
  @Output() submitBook: EventEmitter<Book> = new EventEmitter();

  constructor() { }

  ngOnInit() {
    this.bookForm = new FormGroup({
      title: new FormControl(this.book.title),
      genre: new FormControl(this.book.genre)
    })
  }

  onSubmit() {
    this.submitBook.emit(Object.assign(this.book, this.bookForm.value));
  }

  closeEditor() {
    this.close.emit(null);
  }

}
