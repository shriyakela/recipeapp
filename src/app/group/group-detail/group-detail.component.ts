import { Component } from '@angular/core';
import { GroupService } from '../group.service';
import { Group } from '../group.model';
@Component({
  selector: 'app-group-detail',
  templateUrl: './group-detail.component.html',
  styleUrl: './group-detail.component.css'
})
export class GroupDetailComponent {
  group:Group = { imagePath: '', name: '', description: '', isPublic:true };
  constructor(private groupService:GroupService){}
  ngOnInit(){
    this.groupService.getGroup.subscribe(res=>
    {
      this.group = res;
      console.log(res)
    }
    )
  }
}
