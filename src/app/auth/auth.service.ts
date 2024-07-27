import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs';
import { catchError, throwError } from 'rxjs';
import { Observable } from 'rxjs';

import { User } from './user.model';

interface AuthResponseData{
  
  email: string,
  username?: string,
  registered?: boolean
}
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  user = new BehaviorSubject<User|null>(null);
  isAuthenticated = new BehaviorSubject<boolean>(null);
  constructor(private http:HttpClient, private router:Router) { }
  apiUrl = "http://127.0.0.1:5000";
  // onLogin(email:string, password:string){
  //   return this.http.post<AuthResponseData>("http://127.0.0.1:5000/login",
  //     {
  //       email: email,
  //       password: password,
  //     }
  //   ).pipe(tap(resData =>{
  //     const user = new User(resData.email, resData.username);
  //     this.user.next(user);
  //   }))
  // }
  onLogin(email: string, password: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, { email, password }).pipe(
      tap(response => {
        if (response.access_token) {
          localStorage.setItem('authToken', response.access_token);
          const user = new User(response.email, response.username);
          this.user.next(user);
        }
      })
    );
  }
  
  // onSignUp(email:string,username:string, password1:string, password2:string){
  //   return this.http.post<any>("http://127.0.0.1:5000/signup",
  //     { email: email, username: username, password1: password1, password2: password2 }
  //   ).pipe(tap(resData =>{
  //     // if (resData.access_token) {
  //     //   localStorage.setItem('authToken', resData.access_token);
  //     //   // const user = new User(response.email, response.username);
  //     //   // this.user.next(user);
  //     // }
  //     const user = new User(resData.email, resData.username);
  //     this.user.next(user);
  //   }))
  // }

  // onSignUp(email: string, username: string, password: string) {
  //   return this.http.post<any>(`${this.apiUrl}/signup`,
  //     { email: email, username: username, password: password }
  //   ).pipe(tap(resData => {
  //     if (resData.access_token) {
  //       localStorage.setItem('authToken', resData.access_token);
  //     }
  //     const user = new User(email, username);
  //     this.user.next(user);
  //   }))
  // }
  onSignUp(email: string, username: string, password: string) {
    return this.http.post<any>(`${this.apiUrl}/signup`,
      { email, username, password }
    ).pipe(tap(resData => {
      if (resData.access_token) {
        localStorage.setItem('authToken', resData.access_token);
      }
      const user = new User(email, username);
      this.user.next(user);
    }));
  }
  logout(){
    this.user.next(null);
    this.router.navigate(['/auth']);
  }
}
