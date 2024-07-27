import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class RecipeService {

  private apiUrl = "http://127.0.0.1:5000/add-recipe"; // Adjust API URL as needed

  constructor(private http: HttpClient) {}

  // Create a new recipe
  createRecipe(recipeData: any): Observable<any> {
    const token = localStorage.getItem('authToken'); // Get JWT token if required
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}` // Include token in headers if required
    });

    return this.http.post<any>(this.apiUrl, recipeData, { headers });
  }
}
