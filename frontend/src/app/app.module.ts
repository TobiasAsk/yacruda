import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { BooksComponent } from './books/books.component';
import { BookEditorComponent } from './book-editor/book-editor.component';

@NgModule({
  declarations: [
    AppComponent,
    BooksComponent,
    BookEditorComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
