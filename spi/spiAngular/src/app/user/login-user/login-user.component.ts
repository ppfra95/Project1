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
  // data = {'token': "",
  //         'id': "",
  //         'username': "",
  //         'email': ""};

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
  }

  post(){
    // let user = {key:''}:
    this.userService.loginUser(this.user)
      .subscribe(
        data => {
          console.log(data.token);
          localStorage.setItem("key", "Token "+JSON.stringify(data.token));
          this.router.navigate(['user/profile/'+JSON.stringify(data.id)]);
        },
        error => console.log(error));
    this.user = new User();
  }

  onSubmit() {
    this.post();
  }

}
