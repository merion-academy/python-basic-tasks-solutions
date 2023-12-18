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
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, DatabaseError
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from core.models import db, Category
from views.forms.category import CategoryForm

categories_app = Blueprint(
    "categories_app",
    __name__,
    url_prefix="/categories",
)


@categories_app.get("/", endpoint="list")
def get_categories():
    return render_template(
        "categories/list.html",
        categories=Category.query.order_by(Category.id).all(),
    )


@categories_app.get("/<int:category_id>/", endpoint="details")
def get_category_by_id(category_id: int):
    category = Category.query.get_or_404(
        ident=category_id,
        description=f"category #{category_id} not found",
    )
    return render_template(
        "categories/details.html",
        category=category,
    )


@categories_app.route(
    "/add/",
    methods=["GET", "POST"],
    endpoint="add",
)
@login_required
def create_category():
    form = CategoryForm()

    template = "categories/add.html"
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

    category = Category(
        name=form.name.data,
        description=form.description.data,
    )
    db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        raise BadRequest(
            "Could not save category, "
            f"probably the name {category.name!r} is not unique"
        )
    except DatabaseError:
        raise InternalServerError("Could not save category due to an internal error")

    flash(f"Created category {category.name}")

    url = url_for("categories_app.details", category_id=category.id)
    return redirect(url)


@categories_app.get(
    "/<int:category_id>/movies/",
    endpoint="category_movies",
)
def get_movies_for_category(category_id: int):
    # category = Category.query.get_or_404(
    #     ident=category_id,
    #     description=f"category #{category_id} not found",
    # )
    # movies = (
    #     Movie.query.filter_by(
    #         category_id=category.id,
    #     )
    #     .order_by(Movie.id)
    #     .all()
    # )

    # category: Category | None = (
    category: Category = (
        db.session.query(Category)
        .filter(
            Category.id == category_id,
        )
        .options(
            selectinload(Category.movies),
        )
        # .one_or_none()
        .one_or_404(
            description=f"category #{category_id} not found",
        )
    )
    # if category is None:
    #     raise NotFound(f"category {category_id} not found")

    return render_template(
        "categories/category-movies.html",
        category=category,
        movies=category.movies,
    )


@categories_app.route(
    "/<int:category_id>/delete/",
    methods=["GET", "POST"],
    endpoint="delete",
)
@login_required
def delete_category(category_id: int):
    category: Category = Category.query.get_or_404(
        ident=category_id,
        description=f"category #{category_id} not found",
    )
    if request.method == "GET":
        return render_template(
            "categories/delete.html",
            category=category,
        )

    flash(f"Deleted category {category.name!r}", "warning")

    db.session.delete(category)
    db.session.commit()

    url = url_for("categories_app.list")
    return redirect(url)
