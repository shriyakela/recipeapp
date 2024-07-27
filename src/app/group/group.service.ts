// import { Injectable } from '@angular/core';
// import { HttpClient , HttpHeaders} from '@angular/common/http';
// import { Observable, of } from 'rxjs';
// import { Group } from './group.model';
// interface Groupi {
//   name: string;
//   description: string;
//   public: boolean;
// }

// @Injectable({
//   providedIn: 'root'
// })
// export class GroupService {
//   groups: Group[] = [
//     new Group(
//       "Chinese",
//       "Explore a wide variety of authentic Chinese recipes, from dumplings to stir-fries.",
//       "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s",
//       true
//     ),
//     new Group(
//       "Vegan",
//       "Discover delicious and healthy vegan recipes for every occasion.",
//       ""
//       true
//     ),
//     new Group(
//       "Dessert",
//       "Indulge in sweet and savory desserts from around the world.",
//       ""
//       true
//     ),
//     new Group(
//       "Italian",
//       "Experience the rich flavors of Italy with these classic Italian recipes.",
//       ""
//       ,true
//     ),
//     new Group(
//       "Mexican",
//       "Savor the spicy and vibrant taste of traditional Mexican cuisine.",
//       ""
//       true
//     ),
//     new Group(
//       "Indian",
//       "Dive into the aromatic and diverse world of Indian cooking.",
//       "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGwaeDfRMQtMcjRl3C5oZnMBghGTULWW7kJA&s",
//       true
//     ),
//     new Group(
//       "Thai",
//       "Enjoy the balance of flavors in authentic Thai dishes.",
//       "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSt1MkLo70al1hoILtvG5MKKghK2HG0RZAGBA&s",
//       true
//     ),
//     new Group(
//       "French",
//       "Experience the elegance and sophistication of French cuisine.",
//       ""
//       true
//     ),
//     new Group(
//       "Mediterranean",
//       "Delight in healthy and flavorful Mediterranean recipes.",
//       "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvS3FMiWfUSHyaRa4x4AD2vQKEdwbaPC1dUA&s",
//       true
//     ),
//     new Group(
//       "BBQ",
//       "Master the art of barbecue with these mouth-watering recipes.",
//       "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOvWAFn03-A1jq5KtRalwZ2zsUidRwEF4Nsw&s",
//       true
//     )
//   ];

//   getGroups(): Observable<Group[]> {
//     return of(this.groups);
//   }
  
//   private apiUrl = 'http://localhost:5000/create-group'; // Replace with your actual backend URL

//   constructor(private http: HttpClient) { }

//   createGroup(group: Groupi): Observable<any> {
//     // const token = localStorage.getItem('auth_token');
//     // const headers = new HttpHeaders({
//     //   'Content-Type': 'application/json',
//     //   'Authorization': `Bearer ${token}`
      
//     // });

//     return this.http.post<Groupi>(this.apiUrl, group);
//   }

// }
import { Injectable, Output, EventEmitter } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Group } from './group.model';
import { map } from 'rxjs';
import { Subject } from 'rxjs';
interface Groupi {
  id: number;
  name: string;
  description: string;
}
@Injectable({
  providedIn: 'root'
})
export class GroupService {
  // getGroup = new Subject<Groupi>();
  storeSingleGroup: Groupi;
  private apiUrl = 'http://localhost:5000/create-group';
  
  constructor(private http: HttpClient) { }
  getPublicGroups(): Observable<any> {
    const token = localStorage.getItem('authToken'); // JWT token if authentication is required
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}` // Include token in headers if necessary
    });

    return this.http.get<any>("http://localhost:5000/", { headers }).pipe(
      map(response => {
        // Transform the response if needed, otherwise return directly
        return {
          user: response.user,
          publicGroups: response.public_groups,
          publicRecipes: response.public_recipes
        };
      })
    );
  }
  createGroup(group: Group): Observable<any> {
    const token = localStorage.getItem('authToken');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });

    return this.http.post<any>("http://localhost:5000/create-group", group, { headers });


  }
  getGroup(group:Groupi){
    this.storeSingleGroup = group;
  }

  deleteGroup(groupId: number): Observable<any> {
    const url = `http://localhost:5000/delete-group/${groupId}`;
    return this.http.delete(url);
  }

  // groups: Group[] = [
  //   new Group(
  //     "Chinese",
  //     "Explore a wide variety of authentic Chinese recipes, from dumplings to stir-fries.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s",
  //     true
  //   ),
  //   new Group(
  //     "Vegan",
  //     "Discover delicious and healthy vegan recipes for every occasion.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s",
  //     true
  //   ),
  //   new Group(
  //     "Dessert",
  //     "Indulge in sweet and savory desserts from around the world.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s",
  //     true
  //   ),
  //   new Group(
  //     "Italian",
  //     "Experience the rich flavors of Italy with these classic Italian recipes.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s"
  //     ,true
  //   ),
  //   new Group(
  //     "Mexican",
  //     "Savor the spicy and vibrant taste of traditional Mexican cuisine.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s",
  //     true
  //   ),
  //   new Group(
  //     "Indian",
  //     "Dive into the aromatic and diverse world of Indian cooking.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGwaeDfRMQtMcjRl3C5oZnMBghGTULWW7kJA&s",
  //     true
  //   ),
  //   new Group(
  //     "Thai",
  //     "Enjoy the balance of flavors in authentic Thai dishes.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSt1MkLo70al1hoILtvG5MKKghK2HG0RZAGBA&s",
  //     true
  //   ),
  //   new Group(
  //     "French",
  //     "Experience the elegance and sophistication of French cuisine.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQew-cK8LNSbh3QT6-DOmMGdPzwUbCUgeB_Lg&s",
  //     true
  //   ),
  //   new Group(
  //     "Mediterranean",
  //     "Delight in healthy and flavorful Mediterranean recipes.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvS3FMiWfUSHyaRa4x4AD2vQKEdwbaPC1dUA&s",
  //     true
  //   ),
  //   new Group(
  //     "BBQ",
  //     "Master the art of barbecue with these mouth-watering recipes.",
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOvWAFn03-A1jq5KtRalwZ2zsUidRwEF4Nsw&s",
  //     true
  //   )
  // ];


  // getGroups(): Observable<Group[]> {
  //     return of(this.groups);
  //   }


}