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
  recipeForm: FormGroup;  // FormGroup instance to manage recipe form
  difficultyLevels: string[] = ['Easy', 'Medium', 'Hard'];  // Predefined difficulty levels
  recipeTypes: string[] = ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Dessert'];  // Predefined recipe types

  constructor(
    private fb: FormBuilder,
    private recipeService: RecipeService,
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit() {
    this.recipeForm = this.fb.group({
      user_id: [null, Validators.required], // User ID field with validation
      group_id: [null, Validators.required], // Group ID field with validation
      cooking_time: [0, [Validators.required, Validators.min(1)]], // Cooking time field with validation
      difficulty_level: ['', Validators.required], // Difficulty level field with validation
      recipe: ['', [Validators.required, Validators.maxLength(10000)]], // Recipe field with validation
      image_path: [''], // Image path field
      ingredients: this.fb.array([]), // Ingredients form array for dynamic inputs
      instructions: ['', Validators.required], // Instructions field with validation
      recipe_type: ['', Validators.required], // Recipe type field with validation
      public: [false] // Public checkbox with default value
    });

    // Optionally initialize with one empty ingredient form group
    this.addIngredient();
  }

  get ingredients(): FormArray {
    return this.recipeForm.get('ingredients') as FormArray;
  }

  // Add a new ingredient form group to the form array
  addIngredient() {
    const ingredientForm = this.fb.group({
      quantity: ['', Validators.required], // Quantity field with validation
      name: ['', Validators.required] // Name field with validation
    });

    this.ingredients.push(ingredientForm);
  }

  // Remove an ingredient form group from the form array by index
  removeIngredient(index: number) {
    this.ingredients.removeAt(index);
  }

  // Submit the recipe form to the server
  onSubmit() {
    if (this.recipeForm.valid) {
      const formData = this.recipeForm.value;
      console.log('Recipe data:', formData);

      this.recipeService.createRecipe(formData).subscribe({
        next: response => {
          console.log('Recipe created successfully:', response);
          alert('Recipe created successfully!');

          // Optionally navigate to another page after successful submission
          this.router.navigate(['/recipes']); // Adjust the route as needed
        },
        error: error => {
          console.error('Error creating recipe:', error);
          alert('An error occurred while creating the recipe.');
        }
      });
    } else {
      console.log('Recipe form is invalid:', this.recipeForm);
      alert('Please fill in all required fields correctly.');
    }
  }
}
