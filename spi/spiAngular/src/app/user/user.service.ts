import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) { }

  registerUser(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}create/`, user);
  }

  loginUser(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}login/`, user);
  }

}
