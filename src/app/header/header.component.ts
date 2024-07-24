import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { DataStorageService } from '../shared/data-storage.service';
import { AuthService } from '../auth/auth.service';
import { GroupService } from '../group/group.service';
@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  isAuthenticated: boolean = false;
  userSub:Subscription;
  constructor(private routes:Router, 
    private dataService: DataStorageService,
    private authService:AuthService,
    private groupService: GroupService
  ){}
  navigateToRecipes(){
    this.routes.navigate(['/recipes']);
  }

  ngOnInit(){
    this.userSub = this.authService.user.subscribe(user =>{
      this.isAuthenticated = !!user;
      // console.log(!user);
      console.log("user authentication status: ",!!user);
    });
  }

  onMyRecipeClicked(){
    // this.groupService.isPrivate = true;
    // console.log("Private recipes group status",this.groupService.isPrivate)
  }
  saveRecipes(){
    this.dataService.storeRecipes();
  }

  fetchData(){
    // this.dataService.fetchRecipes().subscribe();
  }

  ngOnDestroy(){
    this.userSub.unsubscribe();
  }

  onLogout(){
    this.authService.logout();
  }
}
