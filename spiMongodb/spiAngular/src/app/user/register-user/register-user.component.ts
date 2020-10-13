import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
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

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
  }


  save() {
    this.userService.registerUser(this.user)
      .subscribe(
        data => {
          this.router.navigate(['user/login/'], );
        },
        error => console.log(error));
  }

  onSubmit() {
    this.save();
  }

}
