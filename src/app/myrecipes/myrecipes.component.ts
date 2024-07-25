import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-myrecipes',
  templateUrl: './myrecipes.component.html',
  styleUrl: './myrecipes.component.css'
})
export class MyrecipesComponent {

  constructor(private router:Router){}

  onCreate(){
    this.router.navigate(['/create'])
  }
}
