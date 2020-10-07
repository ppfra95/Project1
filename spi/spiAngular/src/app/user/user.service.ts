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

  getUser(id:string): Observable<any> {
    return this.http.get(`${this.baseUrl}user/${id}/edit/`);
  }

  updateUser(id: string, value: any): Observable<Object> {
   return this.http.put(`${this.baseUrl}user/${id}/edit/`, value);
 }
 //
 // deleteCustomer(id: number): Observable<any> {
 //   return this.http.delete(`${this.baseUrl}/${id}`);
 // }

}
