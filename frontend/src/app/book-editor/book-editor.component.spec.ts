import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BookEditorComponent } from './book-editor.component';
import { FormsModule } from '@angular/forms';


describe('BookEditorComponent', () => {
  let component: BookEditorComponent;
  let fixture: ComponentFixture<BookEditorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [BookEditorComponent],
      imports: [FormsModule]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BookEditorComponent);
    component = fixture.componentInstance;
    component.book = {
      title: 'some book title',
      genre: 'some genre'
    }
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
