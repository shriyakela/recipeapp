import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { AuthComponent } from './auth/auth.component';
import { HomeComponent } from './home/home.component';
import { GroupComponent } from './group/group.component';
import { MyrecipesComponent } from './myrecipes/myrecipes.component';

const routes: Routes = [
  {path: '', redirectTo: '', pathMatch:"full"},
  {path: 'home', component: HomeComponent},
  {path: 'group', component: GroupComponent},
  {path:'myrecipes', component:MyrecipesComponent},
  {path: 'recipes', component: AppComponent},
  {path:'shopping-list', component: AppComponent},
  {path:'auth', component: AuthComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
