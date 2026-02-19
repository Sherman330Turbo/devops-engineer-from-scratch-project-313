from sqlmodel import Session, select

from ..models import Link


def register_read_link_by_id_route(app, engine):
    @app.get("/api/links/<int:link_id>")
    def read_link_by_id(link_id: int):
        with Session(engine) as session:
            link = session.exec(
                select(Link).where(Link.id == link_id)
            ).one_or_none()

            if link is None:
                return {"detail": "Not Found"}, 404

        return link.model_dump()
