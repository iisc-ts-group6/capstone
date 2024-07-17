import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AttemptQuestionComponent } from './attempt-question.component';

describe('AttemptQuestionComponent', () => {
  let component: AttemptQuestionComponent;
  let fixture: ComponentFixture<AttemptQuestionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AttemptQuestionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AttemptQuestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
