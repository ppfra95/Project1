import { Component, OnInit } from '@angular/core';
import {Router, ActivatedRoute} from "@angular/router";
import { User } from '../user.model';
import { UserService } from '../user.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})

export class ResetPasswordComponent implements OnInit {
  user: User = new User();
  submitted = false;

  constructor(private userService: UserService, private route: ActivatedRoute,) { }

  ngOnInit(): void {
  }

  save() {
    this.user.token=String(new URLSearchParams(window.location.search).get('token'))

    this.userService.resetPassword(this.user)
      .subscribe(
        data => {
          this.submitted = true;
        },
        error => console.log(error));
  }

  onSubmit() {
    this.save();
  }

}
