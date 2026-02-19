from ..db import engine
from .create_link import register_create_link_route
from .delete_link_by_id import register_delete_link_by_id_route
from .read_link_by_id import register_read_link_by_id_route
from .read_links import register_read_links_route
from .update_link_by_id import register_update_link_by_id_route


def register_routes(app):
    register_read_links_route(app, engine)
    register_create_link_route(app, engine)
    register_read_link_by_id_route(app, engine)
    register_update_link_by_id_route(app, engine)
    register_delete_link_by_id_route(app, engine)
