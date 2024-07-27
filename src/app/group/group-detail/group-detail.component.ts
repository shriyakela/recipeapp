import { Component } from '@angular/core';
import { GroupService } from '../group.service';
import { Group } from '../group.model';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
interface Groupi {
  id: number;
  name: string;
  description: string;
}
interface Recipe {
  id: number;
  recipe: string;
  image_path: string;
  instructions: string;
  group_id: number;
}
@Component({
  selector: 'app-group-detail',
  templateUrl: './group-detail.component.html',
  styleUrl: './group-detail.component.css'
})
export class GroupDetailComponent {
  group:Groupi;
  groups: Groupi[] = [];
  recipes:Recipe[] = []
  publicGroups: Groupi[] = []; // Array to hold public groups
  publicRecipes: Recipe[] = []; // Array to hold public recipes
  userId: number | null = null; // User ID of the current user

  private apiUrl = 'http://localhost:5000'; 
  constructor(private groupService:GroupService, private http:HttpClient,
    private router:Router
  ){}
  ngOnInit(){
    // this.groupService.getGroup.subscribe(res=>
    // {
    //   this.group = res;
    //   console.log(res)
    // }
    // )
    this.group= this.groupService.storeSingleGroup;
    this.loadPublicGroups(); // Load public groups when component initializes
    if(this.router.url === '/home'){
      this.groups = this.publicGroups;
      // this.groupService.getGroups().subscribe(res=>{
      //   this.groups = res;
      // })
      this.recipes = this.publicRecipes;
    }
  }

  loadPublicGroups() {
    this.groupService.getPublicGroups().subscribe({
      next: (data) => {
        this.userId = data.user; // Store user ID
        this.publicGroups = data.publicGroups; // Store public groups
        this.publicRecipes = data.publicRecipes; // Store public recipes
        console.log('Public Groups:', this.publicGroups);
        console.log('Public Recipes:', this.publicRecipes);
      },
      error: (error) => {
        console.error('Error loading public groups:', error);
        alert('An error occurred while fetching public groups.');
      }
    });
  }

 
  deleteGroup(groupId: number): void {
    if (confirm('Are you sure you want to delete this group?')) {
      this.groupService.deleteGroup(groupId).subscribe({
        next: (response) => {
          console.log('Group deleted successfully!', response);
          // Refresh the group list after deletion
          this.loadPublicGroups();
          this.router.navigate(['/home'])
        },
        error: (error) => {
          console.error('Error deleting group:', error);
          // Handle error appropriately, e.g., show a message to the user
        }
      });
    }
  }

  toAddRecipe(){
    this.router.navigate(['/add-recipe'])
  }
}
