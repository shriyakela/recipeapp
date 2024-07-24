import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyrecipesComponent } from './myrecipes.component';

describe('MyrecipesComponent', () => {
  let component: MyrecipesComponent;
  let fixture: ComponentFixture<MyrecipesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MyrecipesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyrecipesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
