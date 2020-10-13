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

  constructor(private userService: UserService, private route: ActivatedRoute,
    private router: Router) { }

  ngOnInit(): void {
    this.reloadData();
  }

  reloadData() {
    this.userService.getUser()
    .subscribe(
        (data: any) => {
          console.log(data);
          this.user = data;
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
