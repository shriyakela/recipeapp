from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Data, User
from werkzeug.utils import secure_filename
from . import db
import os
from flask import current_app
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    user_recipes = Data.query.filter_by(user_id=current_user.id).all()
    public_recipes = Data.query.filter_by(public=True).filter(Data.user_id != current_user.id).all()
    return render_template("home.html", user=current_user, user_recipes=user_recipes, public_recipes=public_recipes)



@views.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        recipe_name = request.form.get('name')
        recipe_image = request.files.get('image')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        public = request.form.get('public') == 'on'

        if len(recipe_name) < 1 or not recipe_image or len(ingredients) < 1 or len(instructions) < 1:
            flash('All fields are required!', category='error')
        else:
            if recipe_image:
                filename = secure_filename(recipe_image.filename)
                
                # Ensure the 'static' directory exists
                static_folder = os.path.join(current_app.root_path, 'static')
                if not os.path.exists(static_folder):
                    os.makedirs(static_folder)
                
                # Save the file
                image_path = os.path.join(static_folder, filename)
                recipe_image.save(image_path)
                
                # Store the relative path in the database
                relative_image_path = os.path.join('static', filename)
            else:
                relative_image_path = None

            new_recipe = Data(
                recipe=recipe_name,
                image_path=relative_image_path,
                ingredients=ingredients,
                instructions=instructions,
                user_id=current_user.id,
                public=public
            )
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe added!', category='success')
            return redirect(url_for('views.home'))

    return render_template('add_recipe.html', user=current_user)
@views.route('/delete-recipe/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Data.query.get(recipe_id)
    if recipe and recipe.user_id == current_user.id:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted!', category='success')
    else:
        flash('You do not have permission to delete this recipe!', category='error')
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
            return redirect(url_for('views.home'))

    return render_template('edit_recipe.html', recipe=recipe)
