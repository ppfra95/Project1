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
          console.log(data);
          localStorage.setItem("key", "Token "+data.token);
          // localStorage.setItem("key", data.token);
          this.router.navigate(['user/profile/'+data.id], { state: JSON.stringify(data) }, );
        },
        error => console.log(error));
    this.user = new User();
  }

  onSubmit() {
    this.post();
  }

}
