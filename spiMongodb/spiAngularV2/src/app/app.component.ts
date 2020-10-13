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
  token = String;

  constructor(private autoLogoutService: AutoLogoutService){}

  ngOnInit(): void {
    console.log("se actualizo");
  }

}
