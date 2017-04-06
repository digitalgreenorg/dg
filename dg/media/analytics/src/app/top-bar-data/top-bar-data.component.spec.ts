import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopBarDataComponent } from './top-bar-data.component';

describe('TopBarDataComponent', () => {
  let component: TopBarDataComponent;
  let fixture: ComponentFixture<TopBarDataComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopBarDataComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopBarDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
