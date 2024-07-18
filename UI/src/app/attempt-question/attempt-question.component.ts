import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { BackendApisService } from '../services/backend-apis.service';
import { LoadingService } from '../services/loading.service';
// export interface ASSESTMENT {
//   position: number;
//   question: string;
//   nlp_answer: string;
//   given_answer: string;
//   result: string;
// }

export interface ASSESTMENT {
  position: number;
  question: string;
  student_answer: string;
  llm_answer: string;
  gpt_result: string;
  gpt_feedback: string;
  score: string;
}

/**
 * @title Basic use of `<table mat-table>`
 */
@Component({
  selector: 'app-attempt-question',
  templateUrl: './attempt-question.component.html',
  styleUrl: './attempt-question.component.css'
})
export class AttemptQuestionComponent implements OnInit {
  isVisible: boolean = false;
  isOverAllResultPass: boolean = false;
  constructor(private backendApisService: BackendApisService, private loadingService: LoadingService) {

  }
  
  ngOnInit(): void {
    this.loadingService.show();
    let results = localStorage.getItem('results') ?? '';
    let parsedResults = JSON.parse(results);
    this.ASSESTMENT = [];
    let stdScore = 0;
    let stdAns = '';
    for(let i = 0; i < parsedResults.length; i++) {
      stdScore = parsedResults[i].score.toFixed(3);
      if(stdScore < 0 ) {
        stdScore = 0;
      }
      stdAns = parsedResults[i].student_answer;
      if(stdAns.trim().length <= 0) {
        stdAns = '';
        stdScore = 0;
      }
      console.log(parsedResults[i].question);
      this.ASSESTMENT[i] = {
        position: i + 1,
        question: parsedResults[i].question,
        student_answer: stdAns,
        llm_answer: parsedResults[i].llm_answer,
        gpt_result: parsedResults[i].result,
        gpt_feedback: parsedResults[i].feedback,
        score: stdScore.toString()
      };
  
    }
    this.isVisible = true;
    this.dataSource = new MatTableDataSource(this.ASSESTMENT);  
    this.isOverAllResultPass = this.isGreaterThanOrPassingPercentage(this.calculateTotalPercentage(this.ASSESTMENT));
    this.loadingService.hide();
  }

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  displayedColumns: string[] = ['position', 'question', 'student_answer', 'llm_answer', 'gpt_result', 'gpt_feedback', 'score'];
  ASSESTMENT: ASSESTMENT[] = [];
  dataSource = new MatTableDataSource(this.ASSESTMENT);

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  isGreaterThanOrPassingPercentage(result: string): boolean {
    return  Number(result) >= 0.5;
  }

  calculateTotalPercentage(assessment: ASSESTMENT[]): string {
    let total: number = 0;
    for(let i=0; i< assessment.length; i++){
      total = total + Number(assessment[i].score);
    } 
    let avarageTotal: number = total / (assessment.length + 1);
    return  Number(avarageTotal.toFixed(3)).toString();
  }
}