from flask import request
from sqlmodel import Session, select

from ..helpers import (
    generate_short_link,
    push_error,
)
from ..models import Link

accepted_keys = ["original_url", "short_name"]


def validate_payload(payload):
    errors = []

    if not isinstance(payload, dict):
        push_error(errors, ["body"], "Invalid payload")
        return errors

    if payload == {}:
        push_error(errors, ["body"], "Payload is empty")
        return errors

    for key in accepted_keys:
        key_value = payload.get(key)
        if key_value is None:
            continue

        if not isinstance(key_value, str):
            push_error(errors, ["body", key], f"{key} is not string")

    return errors


def register_update_link_by_id_route(app, engine):
    @app.put("/api/links/<int:link_id>")
    def update_link_by_id(link_id: int):
        payload = request.get_json(silent=True)
        validation_errors = validate_payload(payload)
        if len(validation_errors):
            return {"detail": validation_errors}, 422

        with Session(engine) as session:
            link = session.exec(
                select(Link).where(Link.id == link_id)
            ).one_or_none()

            if link is None:
                return {"detail": "Not Found"}, 404

            short_name = payload.get("short_name", None)
            if short_name:
                another_link = session.exec(
                    select(Link).where(
                        Link.short_name == short_name,
                        Link.id != link.id,
                    )
                ).one_or_none()

                if another_link is not None:
                    return {"detail": "Conflicted payload"}, 409

            for key, value in payload.items():
                if key in accepted_keys:
                    setattr(link, key, value)

            link.short_url = generate_short_link(link.short_name)

            session.commit()
            session.refresh(link)

        return link.model_dump(), 200
