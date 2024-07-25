from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from .models import Data, User, Group, Ingredient
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
import os

views = Blueprint('views', __name__)

@views.route('/')
@jwt_required()
def home():
    current_user = User.query.get(get_jwt_identity())
    public_groups = Group.query.filter_by(public=True).all()
    user_groups = Group.query.filter((Group.user_id == current_user.id) | (Group.public == True)).all()
    unique_groups = {group.id: group for group in user_groups}.values()
    public_recipes = Data.query.join(Group).filter(Group.public == True).all()

    return render_template("home.html", user=current_user, groups=unique_groups, public_recipes=public_recipes)

@views.route('/group/<int:group_id>')
@jwt_required()
def group_recipes(group_id):
    current_user = User.query.get(get_jwt_identity())
    group = Group.query.get_or_404(group_id)
    if not group.public and group.user_id != current_user.id:
        flash('You do not have permission to view this group!', category='error')
        return redirect(url_for('views.home'))

    recipes = Data.query.filter_by(group_id=group_id).all()
    
    return render_template("group_recipes.html", user=current_user, group=group, recipes=recipes)

@views.route('/create-group', methods=['GET', 'POST'])
@jwt_required()
def create_group():
    current_user = User.query.get(get_jwt_identity())
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        public = 'public' in request.form

        if len(name) < 1:
            flash('Group name is too short!', category='error')
        else:
            new_group = Group(name=name, description=description, user_id=current_user.id, public=public)
            db.session.add(new_group)
            db.session.commit()
            flash('Group created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_group.html', user=current_user)

@views.route('/edit-group/<int:group_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_group(group_id):
    current_user = User.query.get(get_jwt_identity())
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

@views.route('/delete-group/<int:group_id>', methods=['POST'])
@jwt_required()
def delete_group(group_id):
    current_user = User.query.get(get_jwt_identity())
    group = Group.query.get_or_404(group_id)
    if group and group.user_id == current_user.id:
        Data.query.filter_by(group_id=group_id).delete()
        db.session.delete(group)
        db.session.commit()
        flash('Group deleted!', category='success')
    else:
        flash('You do not have permission to delete this group!', category='error')
    return redirect(url_for('views.home'))

@views.route('/add-recipe/<int:group_id>', methods=['GET', 'POST'])
@jwt_required()
def add_recipe(group_id):
    current_user = User.query.get(get_jwt_identity())
    if group_id is None:
        flash('Please select a group to add a recipe to.', category='error')
        return redirect(url_for('views.home'))

    group = Group.query.get_or_404(group_id)

    if request.method == 'POST':
        recipe_name = request.form.get('name')
        ingredient_quantities = request.form.getlist('ingredient_quantities[]')
        ingredient_names = request.form.getlist('ingredient_names[]')
        instructions = request.form.get('instructions')
        recipe_image = request.files.get('image')
        cooking_time = request.form.get('cooking_time')
        difficulty_level = request.form.get('difficulty_level')
        recipe_type = request.form.get('recipe_type')
        public= request.form.get('public')

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

@views.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
@jwt_required()
def delete_recipe(recipe_id):
    current_user = User.query.get(get_jwt_identity())
    recipe = Data.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id:
        abort(403)

    try:
        Ingredient.query.filter_by(data_id=recipe.id).delete()
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully!', category='success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting the recipe: {str(e)}', category='error')
    
    return redirect(url_for('views.group_recipes', group_id=recipe.group_id))

@views.route('/edit-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_recipe(recipe_id):
    current_user = User.query.get(get_jwt_identity())
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

        existing_ingredients = {str(i.id): i for i in recipe.ingredients}
        for quantity, name, ing_id in zip(ingredient_quantities, ingredient_names, ingredient_ids):
            if ing_id:
                if ing_id in existing_ingredients:
                    ingredient = existing_ingredients[ing_id]
                    ingredient.quantity = quantity
                    ingredient.name = name
                    del existing_ingredients[ing_id]
                else:
                    new_ingredient = Ingredient(quantity=quantity, name=name, data_id=recipe.id)
                    db.session.add(new_ingredient)
            else:
                new_ingredient = Ingredient(quantity=quantity, name=name, data_id=recipe.id)
                db.session.add(new_ingredient)

        for ingredient in existing_ingredients.values():
            db.session.delete(ingredient)

        db.session.commit()
        flash('Recipe updated!', category='success')
        return redirect(url_for('views.group_recipes', group_id=recipe.group_id))

    return render_template('edit_recipe.html', recipe=recipe, user=current_user)

@views.route('/profile')
@jwt_required()
def profile():
    current_user = User.query.get(get_jwt_identity())
    return render_template('profile.html', user=current_user)

@views.route('/profile/public-recipes')
@jwt_required()
def public_recipes():
    current_user = User.query.get(get_jwt_identity())
    public_recipes = Data.query.filter_by(public=True).all()
    return render_template('public_recipes.html', user=current_user, recipes=public_recipes)

@views.route('/profile/personal-recipes')
@jwt_required()
def personal_recipes():
    current_user = User.query.get(get_jwt_identity())
    personal_recipes = Data.query.filter_by(user_id=current_user.id).all()
    return render_template('personal_recipes.html', user=current_user, recipes=personal_recipes)

@views.route('/profile/groups')
@jwt_required()
def profile_groups():
    current_user = User.query.get(get_jwt_identity())
    groups = Group.query.filter_by(user_id=current_user.id).all()
    return render_template('profile_groups.html', user=current_user, groups=groups)


@views.route('/profile/shopping-list', methods=['GET', 'POST'])
@jwt_required()
def shopping_list():
    current_user = User.query.get(get_jwt_identity())
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
@jwt_required()
def remove_from_shopping_list():
    current_user = User.query.get(get_jwt_identity())
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
@jwt_required()
def recipe_detail(recipe_id):
    current_user = User.query.get(get_jwt_identity())
    recipe = Data.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id and not recipe.public:
        flash('You do not have permission to view this recipe!', category='error')
        return redirect(url_for('views.home'))

    ingredients = Ingredient.query.filter_by(data_id=recipe_id).all()
    return render_template('recipe_detail.html', user=current_user, recipe=recipe, ingredients=ingredients)

@views.route('/add-to-shopping-list', methods=['POST'])
@jwt_required()
def add_to_shopping_list():
    current_user = User.query.get(get_jwt_identity())
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
