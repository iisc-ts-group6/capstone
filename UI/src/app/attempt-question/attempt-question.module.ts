import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AttemptQuestionRoutingModule } from './attempt-question-routing.module';
import { AttemptQuestionComponent } from './attempt-question.component';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule} from '@angular/material/paginator';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
  declarations: [
    AttemptQuestionComponent
  ],
  imports: [
    CommonModule,
    AttemptQuestionRoutingModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatIconModule
  ]
})
export class AttemptQuestionModule { }
