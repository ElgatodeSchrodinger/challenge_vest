import json


def test_buy_stocks(client):
    data = {"qty": 3, "symbol": "aapl", "transaction_type": "buy"}
    response = client.post("/stocks/transfers", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["qty"] == 3
    assert response.json()["transaction_type"] == "buy"


def test_sell_stocks(client):
    shares_to_buy_data = {
        "qty": 10,
        "symbol": "tsla",
        "transaction_type": "buy",
    }
    shares_to_sell_data = {
        "qty": 5,
        "symbol": "tsla",
        "transaction_type": "sell",
    }

    bought_response = client.post(
        "/stocks/transfers", json.dumps(shares_to_buy_data)
    )

    assert bought_response.status_code == 200
    assert bought_response.json()["qty"] == 10
    assert bought_response.json()["transaction_type"] == "buy"

    sold_response = client.post(
        "/stocks/transfers", json.dumps(shares_to_sell_data)
    )
    assert sold_response.status_code == 200
    assert sold_response.json()["qty"] == 5
    assert sold_response.json()["transaction_type"] == "sell"


def test_sell_stocks_if_not_enough(client):
    shares_to_buy_data = {"qty": 5, "symbol": "tsla", "transaction_type": "buy"}
    shares_to_sell_data = {
        "qty": 10,
        "symbol": "tsla",
        "transaction_type": "sell",
    }

    bought_response = client.post(
        "/stocks/transfers", json.dumps(shares_to_buy_data)
    )

    assert bought_response.status_code == 200
    assert bought_response.json()["qty"] == 5
    assert bought_response.json()["transaction_type"] == "buy"

    sold_response = client.post(
        "/stocks/transfers", json.dumps(shares_to_sell_data)
    )
    assert sold_response.status_code == 422


def test_buy_stocks_if_symbol_not_found(client):
    data = {"qty": 2, "symbol": "ABCD", "transaction_type": "buy"}
    response = client.post("/stocks/transfers", json.dumps(data))
    assert response.status_code == 404


def test_holding_stock_information(client):
    bought_share_data_1 = {
        "qty": 5,
        "symbol": "tsla",
        "transaction_type": "buy",
    }

    bought_share_data_2 = {
        "qty": 3,
        "symbol": "tsla",
        "transaction_type": "buy",
    }

    response_share_1 = client.post(
        "/stocks/transfers", json.dumps(bought_share_data_1)
    )
    response_share_2 = client.post(
        "/stocks/transfers", json.dumps(bought_share_data_2)
    )

    assert response_share_1.status_code == 200
    assert response_share_2.status_code == 200

    # Validate mystocks endpoint
    mystocks_response = client.get("/stocks/my")
    assert mystocks_response.status_code == 200
    mystocks = mystocks_response.json().get("stocks")
    assert len(mystocks) == 1
    mystock = mystocks[0]
    assert mystock["symbol"] == "TSLA"
    assert mystock["name"] == "Tesla, Inc. Common Stock"
    assert mystock["indicators_data"]["held_shares"] == 8


def test_stock_history_without_transfers(client):
    stock_history_response = client.get("/stocks/history/tsla")
    assert stock_history_response.status_code == 404


def test_stock_history_after_buy(client):
    shares_to_buy_data = {"qty": 5, "symbol": "tsla", "transaction_type": "buy"}

    bought_response = client.post(
        "/stocks/transfers", json.dumps(shares_to_buy_data)
    )

    assert bought_response.status_code == 200
    assert bought_response.json()["qty"] == 5
    assert bought_response.json()["transaction_type"] == "buy"

    stock_history_response = client.get("/stocks/history/tsla")
    assert stock_history_response.status_code == 200
    stock_history_data = stock_history_response.json()
    assert stock_history_data["stock_history"]["symbol"] == "TSLA"
    assert (
        stock_history_data["stock_history"]["name"]
        == "Tesla, Inc. Common Stock"
    )
    assert isinstance(stock_history_data["stock_history"]["records"], list)
