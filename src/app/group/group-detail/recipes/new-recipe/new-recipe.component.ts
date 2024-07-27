// import { Component } from '@angular/core';

// @Component({
//   selector: 'app-new-recipe',
//   templateUrl: './new-recipe.component.html',
//   styleUrl: './new-recipe.component.css'
// })
// export class NewRecipeComponent {

// }
// recipe.component.ts

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { RecipeService } from '../recipe.service';
import { HttpClient } from '@angular/common/http'; // Ensure this is imported if you're making HTTP requests
import { Router } from '@angular/router'; // Import Router if needed for navigation

@Component({
    selector: 'app-new-recipe',
    templateUrl: './new-recipe.component.html',
    styleUrl: './new-recipe.component.css'
})
export class NewRecipeComponent implements OnInit {
  recipeForm!: FormGroup;
  selectedFile: File | null = null;

  constructor(private fb: FormBuilder, private http: HttpClient) {}

  ngOnInit(): void {
    this.recipeForm = this.fb.group({
      name: ['', Validators.required],
      ingredients: this.fb.array([
        this.fb.group({
          quantity: ['', Validators.required],
          name: ['', Validators.required],
        }),
      ]),
      instructions: ['', Validators.required],
      cookingTime: ['', [Validators.required, Validators.min(1)]],
      difficultyLevel: ['Easy', Validators.required],
      recipeType: ['Vegetarian', Validators.required],
      public: [true],
    });
  }

  get ingredients(): FormArray {
    return this.recipeForm.get('ingredients') as FormArray;
  }

  addIngredient(): void {
    this.ingredients.push(
      this.fb.group({
        quantity: ['', Validators.required],
        name: ['', Validators.required],
      })
    );
  }

  removeIngredient(index: number): void {
    this.ingredients.removeAt(index);
  }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  onSubmit(): void {
    if (this.recipeForm.invalid) {
      alert('Please fill out all required fields!');
      return;
    }

    const formData = new FormData();
    formData.append('name', this.recipeForm.get('name')?.value);
    formData.append('instructions', this.recipeForm.get('instructions')?.value);
    formData.append('cooking_time', this.recipeForm.get('cookingTime')?.value);
    formData.append('difficulty_level', this.recipeForm.get('difficultyLevel')?.value);
    formData.append('recipe_type', this.recipeForm.get('recipeType')?.value);
    formData.append('public', this.recipeForm.get('public')?.value ? '1' : '0');

    this.ingredients.controls.forEach((ingredient, index) => {
      formData.append(
        `ingredient_quantities[]`,
        ingredient.get('quantity')?.value
      );
      formData.append(
        `ingredient_names[]`,
        ingredient.get('name')?.value
      );
    });

    if (this.selectedFile) {
      formData.append('recipe_image', this.selectedFile, this.selectedFile.name);
    }

    // Replace 'group_id' with the actual ID of the group you want to add the recipe to
    const groupId = 1; 

    this.http
      .post(`http://127.0.0.1:5000/add-recipe/${groupId}`, formData)
      .subscribe(
        {next:(response) => {
          alert('Recipe added successfully!');
          this.recipeForm.reset({
            name: '',
            ingredients: [],
            instructions: '',
            cookingTime: '',
            difficultyLevel: 'Easy',
            recipeType: 'Vegetarian',
            public: true,
          });
        },
        error:(error) => {
          console.error('Error adding recipe:', error);
          alert('Failed to add recipe!');
        }}
      );
  }
}
