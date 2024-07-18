import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AppConstants } from '../app-constants';

@Injectable({
  providedIn: 'root'
})
export class CsvApisService {

  //private apiUrl =  AppConstants.baseURL + '/api/v1/getquestions?filename=master_sheet_use.csv&num_of_questions=5';
  private apiUrl =  AppConstants.baseURL + '/api/v1/getquestions?filename=sample1.csv&num_of_questions=5';

  constructor(private http: HttpClient) { }

  getQuestions(): Observable<any> {
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
