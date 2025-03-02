"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"
    # user model class

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"


    
class Movie(db.Model):
    """Movies to be rated """

    __tablename__ = "movies"
    # movie model class

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    released_date = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.Text, nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Movie movie_id={self.movie_id} 
                   title={self.title} 
                   released_date={self.released_date}
                   imdb_url={self.imdb_url}>"""


    

class Rating(db.Model):
    """Rating of the movies"""

    __tablename__ = "ratings"
    # rating model class

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer,
                         db.ForeignKey('movies.movie_id'))
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, nullable=False)



    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Rating rating_id={self.rating_id} 
                   movie_id={self.movie_id} 
                   user_id={self.user_id} 
                   score={self.score}>"""

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)




if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
