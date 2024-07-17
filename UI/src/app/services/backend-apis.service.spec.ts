import { TestBed } from '@angular/core/testing';

import { BackendApisService } from './backend-apis.service';

describe('BackendApisService', () => {
  let service: BackendApisService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BackendApisService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
