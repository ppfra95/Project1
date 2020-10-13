import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserRecoveryPasswordComponent } from './user-recovery-password.component';

describe('UserRecoveryPasswordComponent', () => {
  let component: UserRecoveryPasswordComponent;
  let fixture: ComponentFixture<UserRecoveryPasswordComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserRecoveryPasswordComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserRecoveryPasswordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
