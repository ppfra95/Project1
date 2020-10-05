import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterUserComponent } from './register-user/register-user.component';

const routes: Routes = [
    { path: '', redirectTo: 'customer', pathMatch: 'full' },
    { path: 'register', component: RegisterUserComponent },
    // { path: 'add', component: RegisterCustomerComponent },
    // { path: 'findbyage', component: SearchCustomersComponent },
    // { path: 'login', component: LoginCustomerComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }


// import { CustomersListComponent } from './customers-list/customers-list.component';
// import { SearchCustomersComponent } from './search-customers/search-customers.component';
// import { LoginCustomerComponent } from './login-customer/login-customer.component';
//
// const routes: Routes = [
//     { path: '', redirectTo: 'customer', pathMatch: 'full' },
//     { path: 'customer', component: CustomersListComponent },
//     { path: 'add', component: RegisterCustomerComponent },
//     { path: 'findbyage', component: SearchCustomersComponent },
//     { path: 'login', component: LoginCustomerComponent },
// ];
//
// @NgModule({
//     imports: [RouterModule.forRoot(routes)],
//     exports: [RouterModule]
// })
//
// export class AppRoutingModule { }
