def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(err):
        return "Bad request", 400

    @app.errorhandler(404)
    def page_not_found(err):
        return "Not Found", 404

    @app.errorhandler(409)
    def conflicted_payload(err):
        return "Conflicted payload", 409

    @app.errorhandler(422)
    def invalid_payload(err):
        return "Invalid payload", 422
