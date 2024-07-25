import { Component, OnInit } from '@angular/core';
import { GroupService } from '../group.service';
import { Group } from '../group.model';
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-group-list',
  templateUrl: './group-list.component.html',
  styleUrls: ['./group-list.component.css'] // Fixed typo: styleUrl -> styleUrls
})
export class GroupListComponent implements OnInit {
  groups: Group[] = []; // Initialize groups array
  displayPrivate: boolean = false;

  constructor(
    private groupService: GroupService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.checkCurrentRoute();
    this.loadGroups();
  }

  checkCurrentRoute(): void {
    if (this.router.url === '/home') {
      this.displayPrivate = false;
    } else {
      console.log('The current route is not /home');
      this.displayPrivate = true;
    }
  }

  loadGroups(): void {
    // Fetch groups from the service
    this.groupService.getGroups().subscribe(
      (groups: Group[]) => {
        if (this.displayPrivate) {
          // Include all groups
          this.groups = groups;
        } else {
          // Include only public groups
          this.groups = groups.filter((group: Group) => group.isPublic);
        }
      },
      (error) => {
        console.error('Error fetching groups:', error);
      }
    );
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
