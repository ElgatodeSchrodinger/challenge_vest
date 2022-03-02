class ClientException(Exception):
    def __init__(self, message, status_code):
        self.message = message or "Sin mensaje"
        self.status_code = status_code or 500

    def __str__(self):
        error_message = "Error con NASDAQ: {} Estatus de respuesta: {}".format(
            self.message, self.status_code
        )
        return error_message
