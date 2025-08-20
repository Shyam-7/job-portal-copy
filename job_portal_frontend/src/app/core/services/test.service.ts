import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { apiConfig } from '../../api.config';

@Injectable({
  providedIn: 'root'
})
export class TestService {
  private apiUrl = apiConfig.apiUrl;

  constructor(private http: HttpClient) { }

  // Test backend connectivity
  testBackendConnection(): Observable<any> {
    return this.http.get(`${this.apiUrl}/health`);
  }

  // Test root endpoint
  testRootEndpoint(): Observable<any> {
    return this.http.get('http://localhost:8000/');
  }
}