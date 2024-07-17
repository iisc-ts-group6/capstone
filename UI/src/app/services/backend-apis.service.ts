import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
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
  private apiUrl = AppConstants.baseURL + '/api/answers-from-candidate';
  
  constructor(private http: HttpClient) { }

  postAnswersFromCandidate(attemptedQuestion: Question[]): Observable<any> {
    return this.http.post<any>(this.apiUrl, attemptedQuestion).pipe(
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
