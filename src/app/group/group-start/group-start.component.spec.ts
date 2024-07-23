import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupStartComponent } from './group-start.component';

describe('GroupStartComponent', () => {
  let component: GroupStartComponent;
  let fixture: ComponentFixture<GroupStartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GroupStartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GroupStartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
