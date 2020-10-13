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

  getUser(): Observable<any> {
    return this.http.get(`${this.baseUrl}user/`);
  }

  updateUser(value: any): Observable<Object> {
   return this.http.put(`${this.baseUrl}user/`, value);
  }

  getTokenRecoveyPassword(user: Object): Observable<any> {
   return this.http.post(`${this.baseUrl}password_reset/`, user);
  }

  resetPassword(user: Object): Observable<any> {
   return this.http.post(`${this.baseUrl}password_reset/confirm/`,user);
  }

}
