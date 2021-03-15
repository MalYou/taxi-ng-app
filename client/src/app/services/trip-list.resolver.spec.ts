import { TestBed } from '@angular/core/testing';

import { TripListResolver } from './trip-list.resolver';

describe('TripListService', () => {
  let service: TripListResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TripListResolver);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
