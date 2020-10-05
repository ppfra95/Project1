import { Component, OnInit } from '@angular/core';
import { UserModel } from '../customer.model';
import { UserService } from '../user.service';

@Component({
  selector: 'app-register-user',
  templateUrl: './register-user.component.html',
  styleUrls: ['./register-user.component.css']
})
export class RegisterUserComponent implements OnInit {
  user: User = new UserModel();
  submitted = false;

  constructor(private userService: userService) { }

  ngOnInit(): void {
  }

  newCustomer(): void {
    this.submitted = false;
    this.user = new UserModel();
  }

  save() {
    this.customerService.registerCustomer(this.user)
      .subscribe(
        data => {
          console.log(data);
          this.submitted = true;
        },
        error => console.log(error));
    this.user = new UserModel();
  }

  onSubmit() {
    this.save();
  }

}
