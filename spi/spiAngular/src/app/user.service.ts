import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {

  private baseUrl = 'http://localhost:8000/';

  constructor(private http: HttpClient) { }

  getCustomer(id: number): Observable<Object> {
    return this.http.get(`${this.baseUrl}${id}`);
  }

  registerCustomer(customer: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}`, customer);
  }

}
