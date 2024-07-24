from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Data, User, Group
from werkzeug.utils import secure_filename
from . import db
import os
from flask import current_app

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    public_recipes = Data.query.filter_by(public=True).filter(Data.user_id != current_user.id).all()
    return render_template("home.html", user=current_user, groups=groups, public_recipes=public_recipes)

@views.route('/group/<int:group_id>')
@login_required
def group_recipes(group_id):
    group = Group.query.get_or_404(group_id)
    if group.user_id != current_user.id:
        flash('You do not have permission to view this group!', category='error')
        return redirect(url_for('views.home'))

    recipes = Data.query.filter_by(group_id=group_id).all()
    return render_template("group_recipes.html", user=current_user, group=group, recipes=recipes, group_id=group_id)

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
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        recipe_image = request.files.get('image')

        if not recipe_name or not ingredients or not instructions:
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
            ingredients=ingredients,
            instructions=instructions,
            user_id=current_user.id,
            public=True,
            group_id=group_id
        )
        db.session.add(new_recipe)
        db.session.commit()
        flash(f'Recipe added to {group.name}!', category='success')
        return redirect(url_for('views.group_recipes', group_id=group_id))

    return render_template('add_recipe.html', user=current_user, group=group)

@views.route('/delete-recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Data.query.get(recipe_id)
    if recipe and recipe.user_id == current_user.id:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted!', category='success')
        return redirect(url_for('views.group_recipes', group_id=recipe.group_id))
    else:
        flash('You do not have permission to delete this recipe!', category='error')
    return redirect(url_for('views.home'))

@views.route('/delete-group/<int:group_id>', methods=['POST'])
@login_required
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    if group and group.user_id == current_user.id:
        db.session.delete(group)
        db.session.commit()
        flash('Group deleted!', category='success')
    else:
        flash('You do not have permission to delete this group!', category='error')
    return redirect(url_for('views.home'))

@views.route('/edit-recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Data.query.get(recipe_id)
    if not recipe or recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe!', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        recipe_name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        recipe_image = request.files.get('image')

        if len(recipe_name) < 1 or len(ingredients) < 1 or len(instructions) < 1:
            flash('All fields are required!', category='error')
        else:
            recipe.recipe = recipe_name
            recipe.ingredients = ingredients
            recipe.instructions = instructions
            if recipe_image:
                image_path = f'static/images/{recipe_image.filename}'
                recipe_image.save(image_path)
                recipe.image_path = image_path
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
