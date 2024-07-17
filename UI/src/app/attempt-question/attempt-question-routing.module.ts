import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AttemptQuestionComponent } from './attempt-question.component';

const routes: Routes = [{ path: '', component: AttemptQuestionComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AttemptQuestionRoutingModule { }
