import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CsvApisService } from '../services/csv-apis.service';
import { BackendApisService } from '../services/backend-apis.service';
import { LoadingService } from '../services/loading.service';
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
  constructor(private router: Router, private route: ActivatedRoute, private csvApisService: CsvApisService, private backendApisService: BackendApisService, private loadingService: LoadingService) { }
  position: number = 0;
  QUESTIONS!: Question[];
  isVisible: boolean = false;
  ngOnInit() {
    this.loadingService.show();
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
        for (let i = 0; i <= data.length - 1; i++) {
          this.QUESTIONS.push({
            position: i + 1,
            question: data[i],
            nlp_answer: '',
            given_answer: '',
            result: Math.floor(Math.random() * 100).toString()
          });
          
          console.log(this.QUESTIONS[i].position);
        }
        console.log(this.QUESTIONS);
        this.loadingService.hide();
        if(this.QUESTIONS.length > 0) {
          this.isVisible = true;
        }
        
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

      let body = this.formQuestionAnswerSet(this.QUESTIONS);
      this.loadingService.show();
      this.backendApisService.postAnswersFromCandidateAndGetResult(body).subscribe(
        response => {
          localStorage.setItem('results', JSON.stringify(response.predictions));
          this.loadingService.hide();
          this.router.navigateByUrl('/results');
        },
        error => {
          console.error('Error:', error);
        }
      );
    }
  }

  formQuestionAnswerSet(question: Question[]): any {
    let questionAnswerSetFromStudent: any = [];
    for (let i = 0; i < question.length; i++) {
      questionAnswerSetFromStudent[i] = {}; // Initialize each element as an object
      questionAnswerSetFromStudent[i].question = question[i].question;
      questionAnswerSetFromStudent[i].user_input = question[i].given_answer;
    }

    return {
      questionAnswerSetFromStudent
    }
  }
}
