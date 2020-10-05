import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  id:number;
  username:string;
  first_name:string;
  last_name:string;
  age:number;
  address:string;
  email:string;
  password:string;
  cell_Phone:number;
  last_login:string;
  date_joined:sritng;
  token:number;

  constructor() { }
}
