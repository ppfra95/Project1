import { Component, OnInit } from '@angular/core';
import { User } from '../user.model';
import { UserService } from '../user.service';

@Component({
  selector: 'app-register-user',
  templateUrl: './register-user.component.html',
  styleUrls: ['./register-user.component.css']
})

export class RegisterUserComponent implements OnInit {
  user: User = new User();
  submitted = false;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
  }

  newCustomer(): void {
    this.submitted = false;
    this.user = new User();
  }

  save() {
    this.userService.registerUser(this.user)
      .subscribe(
        data => {
          console.log(data);
          this.submitted = true;
        },
        error => console.log(error));
    this.user = new User();
  }

  onSubmit() {
    this.save();
  }

}
