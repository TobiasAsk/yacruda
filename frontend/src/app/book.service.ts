import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Book } from './book';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookService {

  private booksUrl = '/api/books';

  constructor(private httpClient: HttpClient) { }

  getBooks(): Observable<Book[]> {
    return this.httpClient.get<Book[]>(this.booksUrl);
  }

  addBook(book: Book): Observable<HttpResponse<any>> {
    return this.httpClient.post(this.booksUrl, book, { observe: 'response' });
  }

  updateBook(book: Book): Observable<HttpResponse<any>> {
    const path = this.booksUrl + '/' + book.uid;
    return this.httpClient.put(path, book, { observe: 'response' });
  }
}
