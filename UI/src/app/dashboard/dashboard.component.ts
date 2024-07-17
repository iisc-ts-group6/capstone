import { Component } from '@angular/core';
import { FormControl } from '@angular/forms';
export interface Assessment {
  position: number;
  assessmentId: string;
  assessmentName: string;
}
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  ASSESSMENTS: Assessment[] = [
    { position: 1, assessmentId: 'Assessment - 1', assessmentName: 'Assessment - 1' },
    { position: 2, assessmentId: 'Assessment - 2', assessmentName: 'Assessment - 2' },
    { position: 3, assessmentId: 'Assessment - 3', assessmentName: 'Assessment - 3' },
    { position: 4, assessmentId: 'Assessment - 4', assessmentName: 'Assessment - 4' },
    { position: 5, assessmentId: 'Assessment - 5', assessmentName: 'Assessment - 5' },
    { position: 6, assessmentId: 'Assessment - 6', assessmentName: 'Assessment - 6' },
    { position: 7, assessmentId: 'Assessment - 7', assessmentName: 'Assessment - 7' },
    { position: 8, assessmentId: 'Assessment - 8', assessmentName: 'Assessment - 8' },
    { position: 9, assessmentId: 'Assessment - 9', assessmentName: 'Assessment - 9' },
    { position: 10, assessmentId: 'Assessment - 10', assessmentName: 'Assessment - 10' },
  ];
  disableSelect = new FormControl(false);
  selectedAssessmentId: number = 1;
  isActive: boolean = true;

  onAssessmentChange(event: Event) {
    const selectElement = event.target as HTMLSelectElement;
    const selectedPosition = parseInt(selectElement.value, 10);
    this.selectAssessment(selectedPosition);
  }
  selectAssessment(position: number) {
    console.log(position);

    this.selectedAssessmentId = position;
  }
}
