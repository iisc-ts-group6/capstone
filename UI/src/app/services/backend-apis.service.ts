import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AppConstants } from '../app-constants';
export interface Question {
  position: number;
  question: string;
  nlp_answer: string;
  given_answer: string;
  result: string;
}
@Injectable({
  providedIn: 'root'
})
export class BackendApisService {
  private apiUrl = AppConstants.baseURL + '/api/v1/validate_answers';
  
  constructor(private http: HttpClient) { }

  postAnswersFromCandidateAndGetResult(inputs: any): Observable<any> {
    const body = { inputs: inputs.questionAnswerSetFromStudent };
    console.log(body);
    console.log('body >>>>>>>>> ');
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post<any>(this.apiUrl, body, { headers: headers }).pipe(
      catchError(this.handleError)
    );
  }

  getAnswersFromCandidate(): Observable<any> {
    return this.http.get<any>(this.apiUrl).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Unknown error!';
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(errorMessage);
  }
}
