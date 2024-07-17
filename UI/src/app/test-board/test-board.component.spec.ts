import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestBoardComponent } from './test-board.component';

describe('TestBoardComponent', () => {
  let component: TestBoardComponent;
  let fixture: ComponentFixture<TestBoardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TestBoardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TestBoardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
