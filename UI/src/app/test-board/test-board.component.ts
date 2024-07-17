import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CsvApisService } from '../services/csv-apis.service';
import { BackendApisService } from '../services/backend-apis.service';
export interface Question {
  position: number;
  question: string;
  nlp_answer: string;
  given_answer: string;
  result: string;
}

@Component({
  selector: 'app-test-board',
  templateUrl: './test-board.component.html',
  styleUrl: './test-board.component.css'
})
export class TestBoardComponent {
  assessmentId: string | null = null;
  errorMessage: string | null = null;
  constructor(private router: Router, private route: ActivatedRoute, private csvApisService: CsvApisService, private backendApisService: BackendApisService) { }
  position: number = 0;
  QUESTIONS!: Question[];
  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.assessmentId = 'Assessment ID: ' + params.get('id');
      this.fetchQuestions();
    });
  }
  fetchQuestions(): void {
    this.csvApisService.getQuestions().subscribe(
      data => {
        this.QUESTIONS = [];
        console.log(data);
        for(let i = 0; i<=data.items.length -1; i++) {
          this.QUESTIONS.push({
            position: i + 1,
            question: data.items[i].question,
            nlp_answer: data.items[i].answer,
            given_answer: '',
            result: Math.floor(Math.random() * 100).toString()
          });

          console.log(this.QUESTIONS[i].position);
        }
        console.log(this.QUESTIONS);
        // this.QUESTIONS = data.items
      },
      error => this.errorMessage = error
    );
  }

  previous() {
    if (this.position != 0) {
      this.position = this.position - 1;
    }
  }
  next() {
    if (this.position != this.QUESTIONS.length - 1) {
      this.position = this.position + 1;
    } else {
      let attemptedQuestion: string = JSON.stringify(this.QUESTIONS, null, 2);
      console.log(attemptedQuestion);
      localStorage.setItem('attemptedQuestions', attemptedQuestion);
      this.backendApisService.postAnswersFromCandidate(this.QUESTIONS).subscribe(
        response => {
          this.router.navigateByUrl('/attempt-question');
        },
        error => {
          console.error('Error:', error);
        }
      );
    }
  }
}
