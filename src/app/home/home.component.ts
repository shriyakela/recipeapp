import { ChangeDetectorRef, Component } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { Subscription } from 'rxjs';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  isAuthenticated:boolean = false;
  userSub:Subscription;

  constructor(private authService:AuthService, private cd: ChangeDetectorRef){}

  ngOnint(){
    this.userSub = this.authService.user.subscribe(user =>{
      this.isAuthenticated = !!user;
      // console.log(!user);
      console.log("user authentication status: ",!!user);
      this.cd.detectChanges();
    });
  }
  

  ngOnDestroy() { // Implement OnDestroy to clean up the subscription
    if (this.userSub) {
      this.userSub.unsubscribe();
    }
  }
}
