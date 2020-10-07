import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseUrl = 'http://localhost:8000/api/';
  // private const httpOptions = {
  // headers: new HttpHeaders({
  //   'Authorization': `Bearer eyJhbGciOiJ...`
  // })

  constructor(private http: HttpClient) { }

  registerUser(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}create/`, user);
  }

  loginUser(user: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}login/`, user);
  }

  getUser(id:number): Observable<any> {
    return this.http.get(`${this.baseUrl}user/${id}/edit/`);
  }

 //  updateCustomer(id: number, value: any): Observable<Object> {
 //   return this.http.put(`${this.baseUrl}/${id}`, value);
 // }
 //
 // deleteCustomer(id: number): Observable<any> {
 //   return this.http.delete(`${this.baseUrl}/${id}`);
 // }

}
