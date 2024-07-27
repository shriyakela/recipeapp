import { Component, OnInit } from '@angular/core';
import { GroupService } from '../group.service';
import { Group } from '../group.model';
import { Router, ActivatedRoute } from '@angular/router';

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
  selector: 'app-group-list',
  templateUrl: './group-list.component.html',
  styleUrls: ['./group-list.component.css'] // Fixed typo: styleUrl -> styleUrls
})
export class GroupListComponent implements OnInit {
  // groups: Group[] = []; // Initialize groups array
  // displayPrivate: boolean = false;

  // constructor(
  //   private groupService: GroupService,
  //   private route: ActivatedRoute,
  //   private router: Router
  // ) {}

  // ngOnInit() {
  //   this.checkCurrentRoute();
  //   this.loadGroups();
  // }

  // checkCurrentRoute(): void {
  //   if (this.router.url === '/home') {
  //     this.displayPrivate = false;
  //   } else {
  //     console.log('The current route is not /home');
  //     this.displayPrivate = true;
  //   }
  // }
  
  // loadGroups(): void {
    
  //   // Fetch groups from the service
  //   // this.groupService.getGroups().subscribe(
  //   //   (groups: Group[]) => {
  //   //     if (this.displayPrivate) {
  //   //       // Include all groups
  //   //       this.groups = groups;
  //   //     } else {
  //   //       // Include only public groups
  //   //       this.groups = groups.filter((group: Group) => group.isPublic);
  //   //     }
  //   //   },
  //   //   (error) => {
  //   //     console.error('Error fetching groups:', error);
  //   //   }
  //   // );
  // }
  groups: Groupi[] = [];
  recipes:Recipe[] = []
  publicGroups: Groupi[] = []; // Array to hold public groups
  publicRecipes: Recipe[] = []; // Array to hold public recipes
  userId: number | null = null; // User ID of the current user

  constructor(
    private groupService: GroupService,
    private router: Router,
    private route:ActivatedRoute
  ) {}

  ngOnInit() {
    this.loadPublicGroups(); // Load public groups when component initializes
    if(this.router.url === '/home'){
      this.groups = this.publicGroups;
      // this.groupService.getGroups().subscribe(res=>{
      //   this.groups = res;
      // })
      this.recipes = this.publicRecipes;
    }
  }

  // Method to load public groups from the service
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
}




// import { Component } from '@angular/core';
// import { GroupService } from '../group.service';
// import { Group } from '../group.model';
// import { Router, ActivatedRoute } from '@angular/router';
// @Component({
//   selector: 'app-group-list',
//   templateUrl: './group-list.component.html',
//   styleUrl: './group-list.component.css'
// })
// export class GroupListComponent {
//   groups:Group[];
//   constructor(private groupService: GroupService, private route:ActivatedRoute, private router:Router){}
//   displayPrivate:boolean = false;
//   ngOnInit(){
//     this.checkCurrentRoute();
//     if(this.displayPrivate == false){
      
//     }
//   }

//   checkCurrentRoute(): void {
//     if (this.router.url === '/home') {
//       this.displayPrivate = false;
//     } else {
//       console.log('The current route is not /home');
//       this.displayPrivate = true;
//     }
//   }
// }
