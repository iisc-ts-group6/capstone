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
    { position: 2, assessmentId: 'Assessment - 2', assessmentName: 'Assessment - 2' }
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
