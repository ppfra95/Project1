import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import {Router, ActivatedRoute} from "@angular/router";

import { User } from '../user.model';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  user: User = new User();
  login = false;

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
    const token: string = localStorage.getItem('key');
    if (token) {
      this.user = JSON.parse(localStorage.getItem('user'));
      if (!this.user) {
        this.reloadData();
      }
    }else{
      this.router.navigate(['user/login/'], );
    }
  }

  reloadData() {
    this.userService.getUser()
    .subscribe(
        (data: any) => {
          this.user = data;
          localStorage.setItem("user", JSON.stringify(this.user))
          window.location.reload(false);
        },
        error => console.log(error));
  }

  save() {
    console.log(this.user);

    this.userService.updateUser(this.user)
      .subscribe(
        data => {
          console.log(data);
        },
        error => console.log(error));
  }

  onSubmit() {
    this.save();
  }

}
