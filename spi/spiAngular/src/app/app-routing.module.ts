import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterUserComponent } from './user/register-user/register-user.component';
import { LoginUserComponent } from './user/login-user/login-user.component';
import { UserProfileComponent } from './user/user-profile/user-profile.component';
import { UserRecoveryPasswordComponent } from './user/user-recovery-password/user-recovery-password.component';
import { ResetPasswordComponent } from './user/reset-password/reset-password.component';


const routes: Routes = [
  { path: 'user', children: [
    { path: 'login', component: LoginUserComponent },
    { path: 'register', component: RegisterUserComponent },
    { path: 'profile/:id', component: UserProfileComponent },
    { path: 'password_reset', component: UserRecoveryPasswordComponent },
    { path: 'password_reset/confirm/:token', component: ResetPasswordComponent},
  ]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
