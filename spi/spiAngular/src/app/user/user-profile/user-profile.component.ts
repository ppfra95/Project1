import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import {Router} from "@angular/router";

import { User } from '../user.model';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  user: User = new User();

  constructor(private userService: UserService, private router: Router) {
  console.log(this.router.getCurrentNavigation().extras.state); // should log out 'bar'
  this.user=JSON.parse(this.router.getCurrentNavigation().extras.state);
}
  ngOnInit(): void {
    this.reloadData();
  }

  reloadData() {
    // this.user =
    console.log("aqui3");
    this.userService.getUser(this.user.id)
    .subscribe(
        data => {
          console.log(data);
          // this.listComponent.reloadData();
        },
        error => console.log(error));
  }

}

  // post(){
  //   // let user = {key:''}:
  //   this.userService.loginUser(this.user)
  //     .subscribe(
  //       data => {
  //         console.log(data.token);
  //         localStorage.setItem("key", "Token "+data.token);
  //         this.router.navigate(['user/profile/'+data.id], { state: JSON.stringify(data) }, );
  //       },
  //       error => console.log(error));
  //   this.user = new User();
  // }
  //
  // onSubmit() {
  //   this.post();
  // }
