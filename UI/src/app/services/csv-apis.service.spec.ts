import { TestBed } from '@angular/core/testing';

import { CsvApisService } from './csv-apis.service';

describe('CsvApisService', () => {
  let service: CsvApisService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CsvApisService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
