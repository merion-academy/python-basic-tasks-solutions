from http import HTTPStatus

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import BadRequest, InternalServerError

from core.models import db, Movie
from views.forms.movie import MovieForm

movies_app = Blueprint(
    "movies_app",
    __name__,
    url_prefix="/movies",
)


@movies_app.get("/", endpoint="list")
def get_movies():
    return render_template(
        "movies/list.html",
        movies=Movie.query.order_by(Movie.id).all(),
    )


@movies_app.get("/<int:movie_id>/", endpoint="details")
def get_movie_by_id(movie_id: int):
    # movie = Movie.query.get_or_404(
    #     ident=movie_id,
    #     description=f"movie #{movie_id} not found",
    # )
    movie = (
        Movie.query.filter_by(id=movie_id)
        .options(
            joinedload(
                Movie.category,
            )
        )
        .one_or_404(
            description=f"movie #{movie_id} not found",
        )
    )

    return render_template(
        "movies/details.html",
        movie=movie,
    )


@movies_app.route(
    "/add/",
    methods=["GET", "POST"],
    endpoint="add",
)
@login_required
def create_movie():
    form = MovieForm()

    template = "movies/add.html"
    if request.method == "GET":
        return render_template(
            template,
            form=form,
        )

    if not form.validate_on_submit():
        return (
            render_template(
                template,
                form=form,
            ),
            HTTPStatus.BAD_REQUEST,
        )

    movie = Movie(
        title=form.title.data,
        year=form.year.data,
        category_id=form.category.data,
    )
    db.session.add(movie)
    try:
        db.session.commit()
    except IntegrityError:
        raise BadRequest(
            # fmt: off
            "Could not save movie, " 
            f"probably the name {movie.title!r} is not unique"
            # fmt: on
        )
    except DatabaseError:
        raise InternalServerError("Could not save movie due to an internal error")

    flash(f"Created a new movie: {movie.title}")

    url = url_for("movies_app.details", movie_id=movie.id)
    return redirect(url)


@movies_app.route(
    "/<int:movie_id>/delete/",
    methods=["GET", "POST"],
    endpoint="delete",
)
@login_required
def delete_movie(movie_id: int):
    movie = Movie.query.get_or_404(
        ident=movie_id,
        description=f"movie #{movie_id} not found",
    )
    if request.method == "GET":
        return render_template(
            "movies/delete.html",
            movie=movie,
        )

    flash(f"Deleted movie '{movie.title}'", "warning")

    db.session.delete(movie)
    db.session.commit()

    url = url_for("movies_app.list")
    return redirect(url)
