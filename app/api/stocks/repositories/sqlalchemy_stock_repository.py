

class SQLAlchemyStockRepository():

    def __init__(self, sqlalchemy_client, test=False):

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

    def get_all_stocks(self):
        pass
