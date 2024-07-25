import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { authInterceptor } from './shared/auth.interceptor';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthComponent } from './auth/auth.component';
import { HeaderComponent } from './header/header.component';
import { HomeComponent } from './home/home.component';
import { LoadingComponent } from './shared/loading/loading.component';
import { GroupComponent } from './group/group.component';
import { GroupListComponent } from './group/group-list/group-list.component';
import { GroupItemComponent } from './group/group-list/group-slider/group-item/group-item.component';
import { GroupDetailComponent } from './group/group-detail/group-detail.component';
import { GroupEditComponent } from './group/group-edit/group-edit.component';
import { GroupStartComponent } from './group/group-start/group-start.component';
import { RecipesComponent } from './group/group-detail/recipes/recipes.component';
import { NewRecipeComponent } from './group/group-detail/recipes/new-recipe/new-recipe.component';
import { RecipeDetailComponent } from './group/group-detail/recipes/recipe-detail/recipe-detail.component';
import { RecipeEditComponent } from './group/group-detail/recipes/recipe-edit/recipe-edit.component';
import { RecipeListComponent } from './group/group-detail/recipes/recipe-list/recipe-list.component';
import { RecipeItemComponent } from './group/group-detail/recipes/recipe-list/recipe-item/recipe-item.component';
import { MyrecipesComponent } from './myrecipes/myrecipes.component';
import { GroupSliderComponent } from './group/group-list/group-slider/group-slider.component';

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    HeaderComponent,
    HomeComponent,
    LoadingComponent,
    GroupComponent,
    GroupListComponent,
    GroupItemComponent,
    GroupDetailComponent,
    GroupEditComponent,
    GroupStartComponent,
    RecipesComponent,
    NewRecipeComponent,
    RecipeDetailComponent,
    RecipeEditComponent,
    RecipeListComponent,
    RecipeItemComponent,
    MyrecipesComponent,
    GroupSliderComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [provideHttpClient(withInterceptors([authInterceptor]))],
  bootstrap: [AppComponent]
})
export class AppModule { }
