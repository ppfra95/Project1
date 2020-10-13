import { Component, OnInit } from '@angular/core';
import { User } from '../user.model';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-recovery-password',
  templateUrl: './user-recovery-password.component.html',
  styleUrls: ['./user-recovery-password.component.css']
})
export class UserRecoveryPasswordComponent implements OnInit {
  user: User = new User();
  submitted = false;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
  }

  save() {
    this.userService.getTokenRecoveyPassword(this.user)
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
