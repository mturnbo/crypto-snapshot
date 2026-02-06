import csv


def test_token_defaults_and_fields(models_with_stubs):
    _, _, Token = models_with_stubs
    token = Token()

    assert token.name == ""
    assert token.symbol == ""
    assert token.blockchain == ""
    assert token.description == ""
    assert token.logo == ""
    assert token.contracts == []


def test_asset_table_output_with_default_fields(models_with_stubs):
    Asset, _, _ = models_with_stubs
    asset = Asset(name="Bitcoin", symbol="BTC", blockchain="Bitcoin", address="addr", balance=1.5, price=20000)

    output = asset.table_format()

    assert output[0]["value"] == "BTC"
    assert output[1]["value"] == "1.5000"
    assert output[2]["value"] == "20000.00000000"
    assert output[3]["value"] == "$30,000.00"


def test_asset_formatted_output_without_price(models_with_stubs):
    Asset, _, _ = models_with_stubs
    asset = Asset(name="Bitcoin", symbol="BTC", address="addr", balance=1.5, price=None)
    output = asset.table_format()

    assert output[2]["value"] == "N/A"


def test_portfolio_add_remove_assets(monkeypatch, models_with_stubs):
    Asset, Portfolio, _ = models_with_stubs
    monkeypatch.setattr(Portfolio, "get_assets", lambda *args, **kwargs: None)
    portfolio = Portfolio(name="Test", portfolio_type="wallet")

    asset = Asset(name="Bitcoin", symbol="BTC", balance=1)
    portfolio.add_asset(asset)

    assert portfolio.assets == [asset]

    portfolio.remove_asset("Bitcoin")

    assert portfolio.assets == []


def test_portfolio_export_assets_creates_csv(monkeypatch, tmp_path, models_with_stubs):
    Asset, Portfolio, _ = models_with_stubs
    monkeypatch.setattr(Portfolio, "get_assets", lambda *args, **kwargs: None)
    monkeypatch.chdir(tmp_path)

    portfolio = Portfolio(name="Test", portfolio_type="wallet")
    asset = Asset(name="Bitcoin", symbol="BTC", blockchain="bitcoin", balance=1.25, price=20000)
    asset.id = ""
    portfolio.assets = [asset]

    portfolio.export_assets()

    export_root = tmp_path / "data" / "export"
    exported_files = list(export_root.rglob("wallet_test_*.csv"))
    assert len(exported_files) == 1

    with exported_files[0].open(newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    assert rows[0] == ["Name", "Symbol", "Blockchain", "Balance", "Price", "Currency", "Snapshot Date"]
    assert rows[1][:6] == ["Bitcoin", "BTC", "bitcoin", "1.25", "20000", "USD"]
    assert rows[1][6]
