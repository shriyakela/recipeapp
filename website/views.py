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

# @views.route('/')
# @login_required
# def home():
#     user_recipes = Data.query.filter_by(user_id=current_user.id).all()
#     public_recipes = Data.query.filter_by(public=True).filter(Data.user_id != current_user.id).all()
#     return render_template("home.html", user=current_user, user_recipes=user_recipes, public_recipes=public_recipes)


# @views.route('/group/<int:group_id>')
# @login_required
# def group_recipes(group_id):
#     group = Group.query.get_or_404(group_id)
#     if group.user_id != current_user.id:
#         flash('You do not have permission to view this group!', category='error')
#         return redirect(url_for('views.home'))

#     recipes = Data.query.filter_by(group_id=group_id).all()
#     return render_template("group_recipes.html",user=current_user, group=group, recipes=recipes,group_id=group_id)
@views.route('/group/<int:group_id>')
@login_required
def group_recipes(group_id):
    group = Group.query.get_or_404(group_id)
    if group.user_id != current_user.id:
        flash('You do not have permission to view this group!', category='error')
        return redirect(url_for('views.home'))

    recipes = Data.query.filter_by(group_id=group_id).all()
    print(f"Fetched {len(recipes)} recipes for group {group_id}")  # Debug print
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


# @views.route('/add-recipe', methods=['GET', 'POST'])
# @login_required
# def add_recipe():
#     groups = Group.query.filter_by(user_id=current_user.id).all()
#     if request.method == 'POST':
#         recipe_name = request.form.get('name')
#         ingredients = request.form.get('ingredients')
#         instructions = request.form.get('instructions')
#         recipe_image = request.files.get('image')
#         group_id = request.form.get('group_id')
#         new_group_name = request.form.get('new_group_name')

#         if not recipe_name or not ingredients or not instructions:
#             flash('All fields are required!', category='error')
#             return redirect(url_for('views.add_recipe'))
#         group_id = request.form.get('group_id')

#         if not group_id:
#         # Handle the error, e.g., return an error message
#             return 'Group ID is required', 400


#         if new_group_name:
#             existing_group = Group.query.filter_by(name=new_group_name, user_id=current_user.id).first()
#             if not existing_group:
#                 new_group = Group(name=new_group_name, description='', user_id=current_user.id)
#                 db.session.add(new_group)
#                 db.session.commit()
#                 group_id = new_group.id
#             else:
#                 group_id = existing_group.id

#         if recipe_image:
#             filename = secure_filename(recipe_image.filename)
#             static_folder = os.path.join(current_app.root_path, 'static')
#             if not os.path.exists(static_folder):
#                 os.makedirs(static_folder)
#             image_path = os.path.join(static_folder, filename)
#             recipe_image.save(image_path)
#             relative_image_path = os.path.join('static', filename)
#         else:
#             relative_image_path = None

#         new_recipe = Data(
#             recipe=recipe_name,
#             image_path=relative_image_path,
#             ingredients=ingredients,
#             instructions=instructions,
#             user_id=current_user.id,
#             public=True,
#             group_id=group_id
#         )
#         db.session.add(new_recipe)
#         db.session.commit()
#         flash('Recipe added!', category='success')
#         return redirect(url_for('views.home'))

#     return render_template('add_recipe.html', user=current_user, groups=groups,group_id=group_id)
# @views.route('/add-recipe', methods=['GET', 'POST'])
# @login_required
# def add_recipe():
#     groups = Group.query.filter_by(user_id=current_user.id).all()
#     if request.method == 'POST':
#         recipe_name = request.form.get('name')
#         ingredients = request.form.get('ingredients')
#         instructions = request.form.get('instructions')
#         recipe_image = request.files.get('image')
#         group_id = request.form.get('group_id')
#         new_group_name = request.form.get('new_group_name')

#         # Ensure group_id is present
#         if not group_id:
#             flash('Group ID is required', category='error')
#             return redirect(url_for('views.add_recipe'))

#         # Handle new group creation if necessary
#         if new_group_name:
#             existing_group = Group.query.filter_by(name=new_group_name, user_id=current_user.id).first()
#             if not existing_group:
#                 new_group = Group(name=new_group_name, description='', user_id=current_user.id)
#                 db.session.add(new_group)
#                 db.session.commit()
#                 group_id = new_group.id
#             else:
#                 group_id = existing_group.id

#         # Handle recipe image saving
#         if recipe_image:
#             filename = secure_filename(recipe_image.filename)
#             static_folder = os.path.join(current_app.root_path, 'static')
#             if not os.path.exists(static_folder):
#                 os.makedirs(static_folder)
#             image_path = os.path.join(static_folder, filename)
#             recipe_image.save(image_path)
#             relative_image_path = os.path.join('static', filename)
#         else:
#             relative_image_path = None

#         # Create new recipe
#         new_recipe = Data(
#             recipe=recipe_name,
#             image_path=relative_image_path,
#             ingredients=ingredients,
#             instructions=instructions,
#             user_id=current_user.id,
#             public=True,
#             group_id=group_id
#         )
#         db.session.add(new_recipe)
#         db.session.commit()
#         flash('Recipe added!', category='success')
#         return redirect(url_for('views.group_recipes', group_id=group_id))

#     # Render the form with group_id
#     group_id = request.args.get('group_id', None)
#     return render_template('add_recipe.html', user=current_user, groups=groups, group_id=group_id)

@views.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    groups = Group.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        recipe_name = request.form.get('name')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        recipe_image = request.files.get('image')
        group_id = request.form.get('group_id')
        new_group_name = request.form.get('new_group_name')

        if not recipe_name or not ingredients or not instructions:
            flash('Recipe name, ingredients, and instructions are required!', category='error')
            return redirect(url_for('views.add_recipe'))

        # Handle new group creation if necessary
        if new_group_name:
            new_group = Group(name=new_group_name, user_id=current_user.id)
            db.session.add(new_group)
            db.session.commit()
            group_id = new_group.id
        elif not group_id:
            flash('Please select a group or create a new one!', category='error')
            return redirect(url_for('views.add_recipe'))

        # Handle recipe image saving
        # if recipe_image:
        #     filename = secure_filename(recipe_image.filename)
        #     static_folder = os.path.join(current_app.root_path, 'static', 'images')
        #     if not os.path.exists(static_folder):
        #         os.makedirs(static_folder)
        #     image_path = os.path.join(static_folder, filename)
        #     recipe_image.save(image_path)
        #     relative_image_path = os.path.join('static', 'images', filename)
        # else:
        #     relative_image_path = None


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

        # Create new recipe
        try:
            new_recipe = Data(
                recipe=recipe_name,
                image_path=relative_image_path,
                ingredients=ingredients,
                instructions=instructions,
                user_id=current_user.id,
                public=True,
                group_id=int(group_id)
            )
            db.session.add(new_recipe)
            db.session.commit()
            flash(f'Recipe added to group {group_id}!', category='success')
            return redirect(url_for('views.group_recipes', group_id=group_id))
        except ValueError:
            flash('Invalid group selected. Please try again.', category='error')
            return redirect(url_for('views.add_recipe'))

    group_id = request.args.get('group_id')
    return render_template('add_recipe.html', user=current_user, groups=groups, group_id=group_id)

# @views.route('/add-recipe', methods=['GET', 'POST'])
# @login_required
# def add_recipe():
#     if request.method == 'POST':
#         recipe_name = request.form.get('name')
#         recipe_image = request.files.get('image')
#         ingredients = request.form.get('ingredients')
#         instructions = request.form.get('instructions')
#         public = request.form.get('public') == 'on'

#         if len(recipe_name) < 1 or not recipe_image or len(ingredients) < 1 or len(instructions) < 1:
#             flash('All fields are required!', category='error')
#         else:
#             if recipe_image:
#                 filename = secure_filename(recipe_image.filename)
                
#                 # Ensure the 'static' directory exists
#                 static_folder = os.path.join(current_app.root_path, 'static')
#                 if not os.path.exists(static_folder):
#                     os.makedirs(static_folder)
                
#                 # Save the file
#                 image_path = os.path.join(static_folder, filename)
#                 recipe_image.save(image_path)
                
#                 # Store the relative path in the database
#                 relative_image_path = os.path.join('static', filename)
#             else:
#                 relative_image_path = None

#             new_recipe = Data(
#                 recipe=recipe_name,
#                 image_path=relative_image_path,
#                 ingredients=ingredients,
#                 instructions=instructions,
#                 user_id=current_user.id,
#                 public=public
#             )
#             db.session.add(new_recipe)
#             db.session.commit()
#             flash('Recipe added!', category='success')
#             return redirect(url_for('views.home'))

#     return render_template('add_recipe.html', user=current_user)
# @views.route('/add-recipe', methods=['GET', 'POST'])
# @login_required
# def add_recipe():
#     groups = Group.query.filter_by(user_id=current_user.id).all()
#     if request.method == 'POST':
#         recipe_name = request.form.get('name')
#         ingredients = request.form.get('ingredients')
#         instructions = request.form.get('instructions')
#         recipe_image = request.files.get('image')
#         group_id = request.form.get('group_id')

        # if len(recipe_name) < 1 or len(ingredients) < 1 or len(instructions) < 1:
        #     flash('All fields are required!', category='error')
        # else:
        #     image_path = None
        #     if recipe_image:
        #         image_path = f'static/images/{recipe_image.filename}'
        #         recipe_image.save(image_path)
        #     new_recipe = Data(
        #         user_id=current_user.id,
        #         group_id=group_id,
        #         recipe=recipe_name,
        #         ingredients=ingredients,
        #         instructions=instructions,
        #         image_path=image_path,
        #         public=True
        #     )
        #     db.session.add(new_recipe)
        #     db.session.commit()
        #     flash('Recipe added!', category='success')
        #     return redirect(url_for('views.home'))
        # if len(recipe_name) < 1 or not recipe_image or len(ingredients) < 1 or len(instructions) < 1:
        #     flash('All fields are required!', category='error')
        # else:
        #     if recipe_image:
        #         filename = secure_filename(recipe_image.filename)
                
        #         # Ensure the 'static' directory exists
        #         static_folder = os.path.join(current_app.root_path, 'static')
        #         if not os.path.exists(static_folder):
        #             os.makedirs(static_folder)
                
        #         # Save the file
        #         image_path = os.path.join(static_folder, filename)
        #         recipe_image.save(image_path)
                
        #         # Store the relative path in the database
        #         relative_image_path = os.path.join('static', filename)
        #     else:
        #         relative_image_path = None

        #     new_recipe = Data(
        #         recipe=recipe_name,
        #         image_path=relative_image_path,
        #         ingredients=ingredients,
        #         instructions=instructions,
        #         user_id=current_user.id,
        #         public=True
        #     )
        #     db.session.add(new_recipe)
        #     db.session.commit()
        #     flash('Recipe added!', category='success')
        #     return redirect(url_for('views.home'))

    # return render_template('add_recipe.html', user=current_user, groups=groups)
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
            return redirect(url_for('views.home'))

    return render_template('edit_recipe.html', recipe=recipe)
