import hashlib
import os

from flask import abort
from pydantic import ValidationError
from sqlmodel import select

from .models import Link, LinkUpdate


def get_short_hash(input_string, length=6):
    encoded_string = input_string.encode("utf-8")
    hash_object = hashlib.sha256(encoded_string)
    full_hex = hash_object.hexdigest()
    return full_hex[:length]


def generate_short_link(
    original_url: str = None, short_name: str = None
) -> str:
    return f"https://{os.environ['BASE_URL']}/{short_name}/{get_short_hash(original_url)}"


def get_valid_new_link_or_400(request):
    payload = request.json
    if payload is None:
        abort(400)

    original_url = payload.get("original_url", "")
    short_name = payload.get("short_name", "")

    if original_url == "" or short_name == "":
        abort(400)

    return original_url, short_name


def get_link_or_404(session, link_id: int) -> Link:
    link = session.exec(select(Link).where(Link.id == link_id)).one_or_none()

    if link is None:
        abort(404)

    return link


def get_updated_link_or_422(request):
    payload = request.get_json(silent=True)
    if payload is None:
        abort(422)
    try:
        updated_link = LinkUpdate.model_validate(payload)
    except ValidationError:
        abort(422)

    return updated_link


def uniq_short_name_link_or_409(
    session, short_name: str, exclude_link_id: int | None = None
):
    link = session.exec(
        select(Link).where(Link.short_name == short_name)
    ).one_or_none()

    if link is not None and link.id != exclude_link_id:
        abort(409)
