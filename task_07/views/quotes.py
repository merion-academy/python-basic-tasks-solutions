from http import HTTPStatus

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy.exc import (
    IntegrityError,
    DatabaseError,
)
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
)

from models import db, Quote
from views.forms.quote import QuoteForm

quotes_app = Blueprint(
    "quotes_app",
    __name__,
    url_prefix="/quotes",
)


@quotes_app.get(
    "/",
    endpoint="list",
)
def get_quotes():
    return render_template(
        "quotes/list.html",
        quotes=Quote.query.order_by(Quote.id).all(),
    )


@quotes_app.get(
    "/<int:quote_id>/",
    endpoint="details",
)
def get_quote_by_id(quote_id: int):
    quote = Quote.query.get_or_404(
        ident=quote_id,
        description=f"quote #{quote_id} not found",
    )
    return render_template(
        "quotes/details.html",
        quote=quote,
    )


@quotes_app.route(
    "/add/",
    methods=["GET", "POST"],
    endpoint="add",
)
def create_quote():
    form = QuoteForm()

    template = "quotes/add.html"
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

    quote = Quote(
        text=form.text.data,
    )
    db.session.add(quote)
    try:
        db.session.commit()
    except IntegrityError:
        raise BadRequest("Could not save quote, probably text is not unique.")
    except DatabaseError:
        raise InternalServerError("Could not save quote due to an internal error")

    flash(f"Created quote {quote.text}")

    url = url_for("quotes_app.details", quote_id=quote.id)
    return redirect(url)


@quotes_app.route(
    "/<int:quote_id>/delete/",
    methods=["GET", "POST"],
    endpoint="delete",
)
def delete_quote(quote_id: int):
    quote: Quote = Quote.query.get_or_404(
        ident=quote_id,
        description=f"quote #{quote_id} not found",
    )
    if request.method == "GET":
        return render_template(
            "quotes/delete.html",
            quote=quote,
        )

    flash(f"Deleted quote {quote.text!r}", "warning")

    db.session.delete(quote)
    db.session.commit()

    url = url_for("quotes_app.list")
    return redirect(url)
