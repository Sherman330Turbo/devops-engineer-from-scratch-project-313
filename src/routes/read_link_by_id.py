from ..db import select_link


def register_read_link_by_id_route(app):
    @app.get("/api/links/<int:link_id>")
    def read_link_by_id(link_id: int):
        link = select_link(link_id)

        if link is None:
            return {"detail": "Not Found"}, 404

        return link.model_dump()
