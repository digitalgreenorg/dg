import { TestBed, inject } from '@angular/core/testing';

import { GraphsService } from './graphs.service';

describe('GraphsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [GraphsService]
    });
  });

  it('should ...', inject([GraphsService], (service: GraphsService) => {
    expect(service).toBeTruthy();
  }));
});
