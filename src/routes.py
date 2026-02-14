from flask import jsonify, request
from pydantic import ValidationError
from sqlmodel import Session, select

from .db import engine
from .helpers import (
    generate_short_link,
    get_link_or_404,
    get_valid_new_link_or_400,
    uniq_short_name_link_or_409,
)
from .models import Link, LinkUpdate


def register_routes(app):
    @app.get("/api/links")
    def read_links():
        with Session(engine) as session:
            results = session.exec(select(Link)).all()
        return jsonify([link.model_dump() for link in results])

    @app.post("/api/links")
    def create_link():
        (original_url, short_name) = get_valid_new_link_or_400(request)
        with Session(engine) as session:
            uniq_short_name_link_or_409(session, short_name)
            new_link = Link(
                original_url=original_url,
                short_name=short_name,
                short_url=generate_short_link(original_url, short_name),
            )
            session.add(new_link)
            session.commit()
            session.refresh(new_link)
        return new_link.model_dump(), 201

    @app.get("/api/links/<int:link_id>")
    def read_link_by_id(link_id: int):
        with Session(engine) as session:
            link = get_link_or_404(session, link_id)
        return link.model_dump()

    @app.put("/api/links/<int:link_id>")
    def update_link_by_id(link_id: int):
        payload = request.get_json(silent=True)
        if payload is None:
            return "Invalid payload", 422

        with Session(engine) as session:
            link = get_link_or_404(session, link_id)

            try:
                updated_link = LinkUpdate.model_validate(payload)
            except ValidationError:
                return "Invalid payload", 422

            data = updated_link.model_dump(exclude_unset=True)
            for key, value in data.items():
                setattr(link, key, value)

            uniq_short_name_link_or_409(session, link.short_name)
            link.short_url = generate_short_link(
                link.original_url, link.short_name
            )

            session.commit()
            session.refresh(link)

        return link.model_dump(), 200

    @app.delete("/api/links/<int:link_id>")
    def delete_link_by_id(link_id: int):
        with Session(engine) as session:
            link = get_link_or_404(session, link_id)
            session.delete(link)
            session.commit()
        return "", 204
