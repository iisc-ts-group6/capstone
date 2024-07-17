import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TestBoardRoutingModule } from './test-board-routing.module';
import { TestBoardComponent } from './test-board.component';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    TestBoardComponent
  ],
  imports: [
    CommonModule,
    TestBoardRoutingModule,
    MatIconModule,
    FormsModule
  ]
})
export class TestBoardModule { }
