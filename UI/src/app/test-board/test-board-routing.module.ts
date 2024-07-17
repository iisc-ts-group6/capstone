import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TestBoardComponent } from './test-board.component';

const routes: Routes = [{ path: '', component: TestBoardComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TestBoardRoutingModule { }
