import { Component, OnInit } from '@angular/core';
import { AutoLogoutService } from './auto-logout.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'spiAngular';
  login = false;

  constructor(private autoLogoutService: AutoLogoutService){}

  ngOnInit(): void {
    const token: string = localStorage.getItem('key');

    if (token){
      this.login = true;
    }
    else{
      this.login = false;
    }

  }

  singOut(): void {
  localStorage.clear()
  }

}
