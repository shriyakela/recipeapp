from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Data, User, Group, Ingredient
from werkzeug.utils import secure_filename
from . import db
import os
from flask import current_app

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # Query for all public groups and private groups for the current user
    public_groups = Group.query.filter_by(public=True).all()
    user_groups = Group.query.filter_by(user_id=current_user.id).all()
    public_recipes = Data.query.join(Group).filter(Group.public == True).all()
    
    return render_template("home.html", user=current_user, groups=user_groups + public_groups, public_recipes=public_recipes)
@views.route('/group/<int:group_id>')
@login_required
def group_recipes(group_id):
    group = Group.query.get_or_404(group_id)
    
    # Check if the group is public or if the user is the creator of the group
    if not group.public and group.user_id != current_user.id:
        flash('You do not have permission to view this group!', category='error')
        return redirect(url_for('views.home'))

    # Get recipes only if the group is public or if the user is a member
    recipes = Data.query.filter_by(group_id=group_id).all()
    
    return render_template("group_recipes.html", user=current_user, group=group, recipes=recipes)
@views.route('/create-group', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if len(name) < 1:
            flash('Group name is too short!', category='error')
        else:
            new_group = Group(name=name, description=description, user_id=current_user.id)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_group.html', user=current_user)

@views.route('/edit-group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group.user_id != current_user.id:
        flash('You do not have permission to edit this group.', 'danger')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        group.name = request.form.get('name')
        group.description = request.form.get('description')
        group.public = 'public' in request.form
        db.session.commit()
        flash('Group has been updated!', 'success')
        return redirect(url_for('views.home'))

    return render_template('edit_group.html', group=group, user=current_user)


from flask import abort

@views.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Data.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id:
        abort(403)  # Forbidden

    try:
        # First, delete all ingredients associated with this recipe
        Ingredient.query.filter_by(data_id=recipe.id).delete()
        
        # Then delete the recipe
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully!', category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting the recipe: {str(e)}', category='error')
    
    return redirect(url_for('views.group_recipes', group_id=recipe.group_id))



@views.route('/delete-group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group and group.user_id == current_user.id:
        # Delete related recipes
        Data.query.filter_by(group_id=group_id).delete()
        db.session.delete(group)
        db.session.commit()
        flash('Group deleted!', category='success')
    else:
        flash('You do not have permission to delete this group!', category='error')
    return redirect(url_for('views.home'))

@views.route('/add-recipe/<int:group_id>', methods=['GET', 'POST'])
@login_required
def add_recipe(group_id):
    if group_id is None:
        flash('Please select a group to add a recipe to.', category='error')
        return redirect(url_for('views.home'))

    group = Group.query.get_or_404(group_id)
    if group.user_id != current_user.id:
        flash('You do not have permission to add recipes to this group!', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        recipe_name = request.form.get('name')
        ingredient_quantities = request.form.getlist('ingredient_quantities[]')
        ingredient_names = request.form.getlist('ingredient_names[]')
        instructions = request.form.get('instructions')
        recipe_image = request.files.get('image')
        cooking_time = request.form.get('cooking_time')
        difficulty_level = request.form.get('difficulty_level')
        recipe_type = request.form.get('recipe_type')

        if not recipe_name or not ingredient_names or not instructions:
            flash('Recipe name, ingredients, and instructions are required!', category='error')
            return redirect(url_for('views.add_recipe', group_id=group_id))

        if recipe_image:
            filename = secure_filename(recipe_image.filename)
            static_folder = os.path.join(current_app.root_path, 'static')
            if not os.path.exists(static_folder):
                os.makedirs(static_folder)
            image_path = os.path.join(static_folder, filename)
            recipe_image.save(image_path)
            relative_image_path = os.path.join('static', filename)
        else:
            relative_image_path = None

        new_recipe = Data(
            recipe=recipe_name,
            image_path=relative_image_path,
            instructions=instructions,
            user_id=current_user.id,
            public=True,
            group_id=group_id,
            cooking_time=cooking_time,
            difficulty_level=difficulty_level,
            recipe_type=recipe_type
        )
        db.session.add(new_recipe)
        db.session.commit()

        for quantity, name in zip(ingredient_quantities, ingredient_names):
            new_ingredient = Ingredient(quantity=quantity, name=name, data_id=new_recipe.id)
            db.session.add(new_ingredient)

        db.session.commit()
        flash(f'Recipe added to {group.name}!', category='success')
        return redirect(url_for('views.group_recipes', group_id=group_id))

    return render_template('add_recipe.html', user=current_user, group=group)



@views.route('/edit-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Data.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe!', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        recipe_name = request.form.get('name')
        ingredient_quantities = request.form.getlist('ingredient_quantities[]')
        ingredient_names = request.form.getlist('ingredient_names[]')
        ingredient_ids = request.form.getlist('ingredient_ids[]')
        instructions = request.form.get('instructions')
        recipe_image = request.files.get('image')
        cooking_time = request.form.get('cooking_time')
        difficulty_level = request.form.get('difficulty_level')
        recipe_type = request.form.get('recipe_type')

        # Check for empty fields
        if not recipe_name or not ingredient_names or not instructions:
            flash('All fields are required!', category='error')
            return render_template('edit_recipe.html', recipe=recipe, user=current_user)

        recipe.recipe = recipe_name
        recipe.instructions = instructions
        recipe.cooking_time = cooking_time
        recipe.difficulty_level = difficulty_level
        recipe.recipe_type = recipe_type

        if recipe_image:
            filename = secure_filename(recipe_image.filename)
            image_path = os.path.join('static', 'images', filename)
            recipe_image.save(os.path.join(current_app.root_path, image_path))
            recipe.image_path = image_path

        # Update or create ingredients
        existing_ingredients = {str(i.id): i for i in recipe.ingredients}
        for quantity, name, ing_id in zip(ingredient_quantities, ingredient_names, ingredient_ids):
            if ing_id:
                if ing_id in existing_ingredients:
                    # Update existing ingredient
                    ingredient = existing_ingredients[ing_id]
                    ingredient.quantity = quantity
                    ingredient.name = name
                    del existing_ingredients[ing_id]
                else:
                    # Add new ingredient
                    new_ingredient = Ingredient(quantity=quantity, name=name, data_id=recipe.id)
                    db.session.add(new_ingredient)
            else:
                # Handle case where ing_id is not provided
                new_ingredient = Ingredient(quantity=quantity, name=name, data_id=recipe.id)
                db.session.add(new_ingredient)

        # Delete remaining ingredients
        for ingredient in existing_ingredients.values():
            db.session.delete(ingredient)

        db.session.commit()
        flash('Recipe updated!', category='success')
        return redirect(url_for('views.group_recipes', group_id=recipe.group_id))

    return render_template('edit_recipe.html', recipe=recipe, user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/profile/public-recipes')
@login_required
def public_recipes():
    user_public_recipes = Data.query.filter_by(user_id=current_user.id, public=True).all()
    return render_template('public_recipes.html', user=current_user, recipes=user_public_recipes)

@views.route('/profile/private-recipes')
@login_required
def private_recipes():
    user_private_recipes = Data.query.filter_by(user_id=current_user.id, public=False).all()
    return render_template('private_recipes.html', user=current_user, recipes=user_private_recipes)

@views.route('/profile/shopping-list', methods=['GET', 'POST'])
@login_required
def shopping_list():
    if request.method == 'POST':
        ingredient = request.form.get('ingredient')
        if ingredient:
            if current_user.shopping_list:
                shopping_list = current_user.shopping_list.split(',')
            else:
                shopping_list = []
            shopping_list.append(ingredient)
            current_user.shopping_list = ','.join(shopping_list)
            db.session.commit()
            flash('Ingredient added to shopping list!', category='success')
        else:
            flash('Ingredient cannot be empty!', category='error')
    
    shopping_list = current_user.shopping_list.split(',') if current_user.shopping_list else []
    return render_template('shopping_list.html', user=current_user, shopping_list=shopping_list)

@views.route('/profile/shopping-list/remove', methods=['POST'])
@login_required
def remove_from_shopping_list():
    ingredient = request.form.get('ingredient')
    if ingredient and current_user.shopping_list:
        shopping_list = current_user.shopping_list.split(',')
        if ingredient in shopping_list:
            shopping_list.remove(ingredient)
            current_user.shopping_list = ','.join(shopping_list)
            db.session.commit()
            flash('Ingredient removed from shopping list!', category='success')
        else:
            flash('Ingredient not found in shopping list!', category='error')
    else:
        flash('Invalid request!', category='error')
    return redirect(url_for('views.shopping_list'))
@views.route('/recipe/<int:recipe_id>')
@login_required
def recipe_detail(recipe_id):
    recipe = Data.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id and not recipe.public:
        flash('You do not have permission to view this recipe!', category='error')
        return redirect(url_for('views.home'))

    ingredients = Ingredient.query.filter_by(data_id=recipe_id).all()
    return render_template('recipe_detail.html', user=current_user, recipe=recipe, ingredients=ingredients)
@views.route('/add-to-shopping-list', methods=['POST'])
@login_required
def add_to_shopping_list():
    ingredient_id = request.form.get('ingredient_id')
    ingredient = Ingredient.query.get_or_404(ingredient_id)

    if ingredient:
        if current_user.shopping_list:
            shopping_list = current_user.shopping_list.split(',')
        else:
            shopping_list = []

        shopping_item = f"{ingredient.quantity} {ingredient.name}"
        if shopping_item not in shopping_list:
            shopping_list.append(shopping_item)
            current_user.shopping_list = ','.join(shopping_list)
            db.session.commit()
            flash('Ingredient added to shopping list!', category='success')
        else:
            flash('Ingredient already in shopping list!', category='info')
    else:
        flash('Invalid ingredient!', category='error')

    return redirect(url_for('views.recipe_detail', recipe_id=ingredient.data_id))