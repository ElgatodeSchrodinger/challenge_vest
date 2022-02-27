

class SQLAlchemyStockHistoryRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test

    def get_all_stocks(self):
        pass
