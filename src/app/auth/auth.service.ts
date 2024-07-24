import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs';
import { catchError, throwError } from 'rxjs';

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
  user = new BehaviorSubject<User>(null);
  constructor(private http:HttpClient, private router:Router) { }

  onLogin(email:string, password:string){
    return this.http.post<AuthResponseData>("http://127.0.0.1:5000/login",
      {
        email: email,
        password: password,
      }
    ).pipe(tap(resData =>{
      const user = new User(resData.email, resData.username);
      this.user.next(user);
    }))
  }
  
  onSignUp(email:string,username:string, password1:string, password2:string){
    return this.http.post<AuthResponseData>("http://127.0.0.1:5000/signup",
      { email: email, username: username, password1: password1, password2: password2 }
    ).pipe(tap(resData =>{
      const user = new User(resData.email, resData.username);
      this.user.next(user);
    }))
  }
  logout(){
    this.user.next(null);
    this.router.navigate(['/auth']);
  }
}
