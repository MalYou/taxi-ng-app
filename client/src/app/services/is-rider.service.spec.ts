import { TestBed } from '@angular/core/testing';

import { IsRiderService } from './is-rider.service';

describe('IsRiderService', () => {
  let service: IsRiderService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IsRiderService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
