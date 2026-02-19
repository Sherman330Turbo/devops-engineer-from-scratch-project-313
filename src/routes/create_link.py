from flask import request
from sqlmodel import Session, select

from ..helpers import generate_short_link, push_error
from ..models import Link


def validate_payload(payload):
    errors = []

    if not isinstance(payload, dict):
        push_error(errors, ["body"], "Invalid payload")
        return errors

    for key in ["original_url", "short_name"]:
        if payload.get(key, "") == "":
            push_error(errors, ["body", key], f"{key} is empty")

    return errors


def register_create_link_route(app, engine):
    @app.post("/api/links")
    def create_link():
        payload = request.get_json(silent=True)
        validation_errors = validate_payload(payload)
        if len(validation_errors):
            return {"detail": validation_errors}, 422

        original_url = payload["original_url"]
        short_name = payload["short_name"]

        with Session(engine) as session:
            link = session.exec(
                select(Link).where(Link.short_name == short_name)
            ).one_or_none()

            if link is not None:
                return {"detail": "Conflicted payload"}, 409

            new_link = Link(
                original_url=original_url,
                short_name=short_name,
                short_url=generate_short_link(short_name),
            )
            session.add(new_link)
            session.commit()
            session.refresh(new_link)

        return new_link.model_dump(), 201
