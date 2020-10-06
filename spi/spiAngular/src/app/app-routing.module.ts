import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterUserComponent } from './user/register-user/register-user.component';
import { LoginUserComponent } from './user/login-user/login-user.component';
import { UserProfileComponent } from './user/user-profile/user-profile.component';

const routes: Routes = [
  { path: 'user', children: [
    { path: 'login', component: LoginUserComponent },
    { path: 'register', component: RegisterUserComponent },
    { path: 'profile/:id', component: UserProfileComponent },
  ]},
    // { path: 'register', component: RegisterUserComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
