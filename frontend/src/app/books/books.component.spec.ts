import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';

import { BooksComponent } from './books.component';
import { BookEditorComponent } from '../book-editor/book-editor.component';
import { BookService } from '../book.service';
import { of } from 'rxjs';


describe('BooksComponent', () => {
  let component: BooksComponent;
  let fixture: ComponentFixture<BooksComponent>;
  let getBooksSpy: jasmine.Spy;
  const books = [{
    'title': 'The Lord of the Rings',
    'genre': 'Novel'
  }];

  beforeEach(async(() => {
    const bookService = jasmine.createSpyObj('BookService', ['getBooks']);
    getBooksSpy = bookService.getBooks.and.returnValue(of(books));

    TestBed.configureTestingModule({
      declarations: [
        BooksComponent,
        BookEditorComponent
      ],
      providers: [{ provide: BookService, useValue: bookService }],
      imports: [FormsModule]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BooksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
    expect(getBooksSpy.calls.any()).toBe(true, 'getBooks called');
    expect(component.books).toContain(books[0]);
  });
});
