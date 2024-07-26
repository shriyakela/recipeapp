import { Component, Input } from '@angular/core';
export interface Recipe {
  id: number;
  name: string;
  imageUrl: string;
}
@Component({
  selector: 'app-recipe-list',
  templateUrl: './recipe-list.component.html',
  styleUrl: './recipe-list.component.css'
})
export class RecipeListComponent {


  constructor() {}

  ngOnInit(): void {
    console.log('Recipes:');
  }
}
