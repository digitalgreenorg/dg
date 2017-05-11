import { TestBed, inject } from '@angular/core/testing';

import { TopBarDataService } from './top-bar-data.service';

describe('TopBarDataService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TopBarDataService]
    });
  });

  it('should ...', inject([TopBarDataService], (service: TopBarDataService) => {
    expect(service).toBeTruthy();
  }));
});
