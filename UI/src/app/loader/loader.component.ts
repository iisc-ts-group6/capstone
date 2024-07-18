import { Component } from '@angular/core';
import { LoadingService } from '../services/loading.service';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrl: './loader.component.css'
})
export class LoaderComponent {
  isLoading: boolean = false;

  constructor(private loadingService: LoadingService) { }

  ngOnInit() {
    this.loadingService.isLoading$.subscribe((isLoading) => {
      this.isLoading = isLoading;
    });
  }
}
