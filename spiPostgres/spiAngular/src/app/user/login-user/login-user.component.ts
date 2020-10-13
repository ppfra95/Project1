import { Component, OnInit } from '@angular/core';
import { User } from '../user.model';
import { UserService } from '../user.service';
import {Router} from "@angular/router";

@Component({
  selector: 'app-login-user',
  templateUrl: './login-user.component.html',
  styleUrls: ['./login-user.component.css']
})
export class LoginUserComponent implements OnInit {
  user: User = new User();

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
  }

  post(){
    this.userService.loginUser(this.user)
      .subscribe(
        (data: any) => {
          localStorage.setItem("key", "Token "+data.token);
          this.router.navigate(['user/profile/'], );
        },
        error => console.log(error));
    this.user = new User();
  }

  onSubmit() {
    this.post();
  }

}
