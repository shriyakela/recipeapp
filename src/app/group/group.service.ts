import { Injectable } from '@angular/core';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { Group } from './group.model';
// interface Group {
//   name: string;
//   description: string;
//   public: boolean;
// }

@Injectable({
  providedIn: 'root'
})
export class GroupService {
  

  
  
  private apiUrl = 'http://localhost:5000/create-group'; // Replace with your actual backend URL

  constructor(private http: HttpClient) { }

  createGroup(group: Group): Observable<any> {
    // const token = localStorage.getItem('auth_token');
    // const headers = new HttpHeaders({
    //   'Content-Type': 'application/json',
    //   'Authorization': `Bearer ${token}`
      
    // });

    return this.http.post<any>(this.apiUrl, group);
  }

}
