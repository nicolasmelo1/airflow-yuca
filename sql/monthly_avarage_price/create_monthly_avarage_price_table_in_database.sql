CREATE TABLE IF NOT EXISTS monthly_sao_paulo_rent_price (
    id integer PRIMARY KEY AUTOINCREMENT,
    total float NOT NULL,
    month integer NOT NULL,
    created_at datetime NOT NULL
)
        