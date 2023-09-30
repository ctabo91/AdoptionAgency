from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, Pet
from forms import AddPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "keepitonthelow"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
with app.app_context():
    db.create_all()


# Pet Routes:
@app.route('/')
def show_pets():
    """Shows list of pets."""

    pets = Pet.query.order_by(Pet.name).all()
    return render_template('pets.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Shows pet form (GET) or handles pet form submission (POST)"""

    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data

        pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes,
            available=available)
        db.session.add(pet)
        db.session.commit()

        flash(f"Added {name} the {species}")

        return redirect('/')
    else:
        return render_template("add_pet_form.html", form=form)
    

@app.route('/pet/<int:pet_id>', methods=['GET', 'POST'])
def show_detail_and_edit(pet_id):
    """Show single pet details, and a form to edit that pet."""

    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect('/')
    else:
        return render_template('pet_details.html', form=form, pet=pet)