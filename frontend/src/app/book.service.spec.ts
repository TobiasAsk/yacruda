import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';

import { BookService } from './book.service';
import { Book } from './book';


describe('BookService', () => {
  let bookService: BookService;
  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        BookService,
      ]
    });

    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);
    bookService = TestBed.get(BookService);
  });

  it('should be created', () => {
    const service: BookService = TestBed.get(BookService);
    expect(service).toBeTruthy();
  });

  describe('#getBooks', () => {
    let expectedBooks: Book[];
    let booksUrl = '/api/books';

    beforeEach(() => {
      bookService = TestBed.get(BookService);
      expectedBooks = [
        {
          title: 'The Lord of the Rings',
          genre: 'High-fantasy novel'
        }
      ];
    });

    it('should return expected books (called once)', () => {

      bookService.getBooks().subscribe(
        books => expect(books).toEqual(expectedBooks, 'should return expected books'),
        fail
      );

      // BookService should have made one request to GET books from expected URL
      const req = httpTestingController.expectOne(booksUrl);
      expect(req.request.method).toEqual('GET');

      // Respond with the mock books
      req.flush(expectedBooks);
    });
  });
});
