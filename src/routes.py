import json

from flask import abort, jsonify, make_response, request
from sqlmodel import Session, func, select

from .db import engine
from .helpers import (
    generate_short_link,
    get_link_or_404,
    get_updated_link_or_422,
    get_valid_new_link_or_400,
    uniq_short_name_link_or_409,
)
from .models import Link


def register_routes(app):
    @app.get("/api/links")
    def read_links():
        raw_range = request.args.get("range", "[0, 9]")
        try:
            range_list = json.loads(raw_range)
            if (
                not len(range_list) == 2
                or not all(isinstance(value, int) for value in range_list)
                or range_list[0] > range_list[1]
                or range_list[0] < 0
            ):
                raise ValueError
        except json.JSONDecodeError, TypeError, ValueError:
            abort(400)

        min = int(range_list[0])
        max = int(range_list[1])

        with Session(engine) as session:
            results = session.exec(
                select(Link).order_by(Link.id).offset(min).limit(max + 1 - min)
            ).all()
            total = session.exec(select(func.count()).select_from(Link)).one()

        response = make_response(
            jsonify([link.model_dump() for link in results]), 200
        )
        response.headers["Content-Range"] = f"links {min}-{max}/{total}"
        return response

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
        updated_link = get_updated_link_or_422(request)

        with Session(engine) as session:
            link = get_link_or_404(session, link_id)
            if updated_link.short_name:
                uniq_short_name_link_or_409(
                    session, updated_link.short_name, exclude_link_id=link.id
                )

            data = updated_link.model_dump(exclude_unset=True)
            for key, value in data.items():
                setattr(link, key, value)

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
