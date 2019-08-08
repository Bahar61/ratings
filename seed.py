"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app
from datetime import datetime



def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()



def load_movies():
    """Load movies from u.item into database."""

    print("Movies")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate movies
    Movie.query.delete()

    # Read u.item file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        movie_id, title, released_date, _, imdb_url, *_rest = row.split("|")

        #convert string time to Datetime
        if released_date:
            released_date = datetime.strptime(released_date, "%d-%b-%Y")
        else:
            released_date = None


        title = title[:-7]  # remove year from title


        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_date=released_date,
                      imdb_url=imdb_url)


        # add to the session to store
        db.session.add(movie)

    # commit the work
    db.session.commit()



def load_ratings():
    """Load ratings from u.data into database."""

    print("Ratings")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate ratings
    Rating.query.delete()

    # Read u.data file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        movie_id, user_id, score, timestamp = row.split()

        rating = Rating(movie_id=movie_id,
                        user_id=user_id,
                        score=score)

        #add to the session to store
        db.session.add(rating)

    #commit the work
    db.session.commit()


def set_val_movie_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Movie.movie_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('movies_movie_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
