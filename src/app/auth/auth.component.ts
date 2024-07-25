import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent {
  isLogin:boolean= true;
  isLoading:boolean= false;
  error:string = null;


  constructor(private authService:AuthService, private router:Router){}

  onSwitch(){
    this.isLogin = !this.isLogin;
  }

  // constructor(private http: HttpClient) {}

  // onSubmit(form: NgForm) {
  //   if(!form.valid){
  //     return;
  //   }
  //   this.isLoading = true;

  //   const email = form.value.email;
  //   const username = form.value.username;
  //   const password1 = form.value.password1;
  //   const password2 = form.value.password2;
  //   const password = form.value.password;
    
  //   if(this.isLogin){
  //     this.authService.onLogin(email, password).subscribe(
  //     (resData)=>{
  //       localStorage.setItem('authToken', resData.access_token);
  //       console.log(resData.data.token)
  //       console.log(resData);
  //       this.isLoading= false;
  //       this.router.navigate(['/home'])
  //     });
  //   }
  //   else{
  //     this.authService.onSignUp(email, username,password1,password2).subscribe(
  //       (resData) => {
  //       localStorage.setItem('authToken', resData.access_token);
  //       console.log(resData);
  //       this.isLoading = false;
  //       this.router.navigate(['/home']);
  //     }
  //     );
  //   }
  //   form.reset();
  // }
  // onSubmit(form: NgForm) {
  //   if (!form.valid) {
  //     return;
  //   }
  //   this.isLoading = true;
  
  //   const email = form.value.email;
  //   const username = form.value.username;
  //   const password = form.value.password;
  
  //   if (this.isLogin) {
  //     this.authService.onLogin(email, password).subscribe(
  //       {next: (resData) => {
  //         localStorage.setItem('authToken', resData.access_token);
  //         console.log(resData);
  //         this.isLoading = false;
  //         this.router.navigate(['/home'])
  //       },
  //       error:(error) => {
  //         console.error('Login error:', error);
  //         this.error = error.error.msg || 'An error occurred';
  //         this.isLoading = false;
  //       }}
  //     );
  //   } else {
  //     this.authService.onSignUp(email, username, password).subscribe(
  //       {next: (resData) => {
  //         localStorage.setItem('authToken', resData.access_token);
  //         console.log(resData);
  //         this.isLoading = false;
  //         this.router.navigate(['/home']);
  //       },
  //       error: (error) => {
  //         console.error('Signup error:', error);
  //         this.error = error.error.msg || 'An error occurred';
  //         this.isLoading = false;
  //       }}
  //     );
  //   }
  //   form.reset();
  // }
  onSubmit(form: NgForm) {
    if (!form.valid) {
      return;
    }
    this.isLoading = true;
  
    const email = form.value.email;
    const password = form.value.password;
    const username = this.isLogin ? null : form.value.username;
  
    if (this.isLogin) {
      this.authService.onLogin(email, password).subscribe({
        next: (resData) => {
          localStorage.setItem('authToken', resData.access_token);
          console.log(resData);
          this.isLoading = false;
          this.router.navigate(['/home']);
        },
        error: (error) => {
          console.error('Login error:', error);
          this.error = error.error.msg || 'An error occurred';
          this.isLoading = false;
        }
      });
    } else {
      this.authService.onSignUp(email, username, password).subscribe({
        next: (resData) => {
          localStorage.setItem('authToken', resData.access_token);
          console.log(resData);
          this.isLoading = false;
          this.router.navigate(['/home']);
        },
        error: (error) => {
          console.error('Signup error:', error);
          this.error = error.error.msg || 'An error occurred';
          this.isLoading = false;
        }
      });
    }
    form.reset();
  }
}


    // this.http.post<any>("http://127.0.0.1:5000/signup", 
    //   { email: email, username: username, password1: password1, password2: password2 }
    // ).subscribe(response => {
    //     console.log(response);
    //     // handle successful response
    //   });