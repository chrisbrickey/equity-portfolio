# Initial Schema (evolved during development)

*don't forget `from decimal import Decimal` on models*


## stocks
column_name             | data_type                                 | details
------------------------|-------------------------------------------|-----------------------
id                      | integer                                   | not null, primary key
company_name            | string (max_length = 200)                 |
symbol                  | string (max_length = 20)                  | not null, unique   
last_trade_price        | decimal (max_digits=19, decimal_places=3) |    
last_trade_time         | datetime                                  |
timestamp_created       | datetime                                  | not null

##### use this field only when one user/portfolio is sufficient
column_name             | data_type                                                           | details
------------------------|---------------------------------------------------------------------|--------
shares_owned            | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null


## follows - when multiple users/portfolios required
column_name             | data_type                                                           | details
------------------------|---------------------------------------------------------------------|-----------------------
id                      | integer                                                             | not null, primary key
portfolio_id            | integer (on_delete=models.PROTECT)                                  | not null, foreign key (portfolios)
stock_id                | integer (on_delete=models.PROTECT)                                  | not null, foreign key (stocks), unique (portfolio_id)
shares_owned            | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null
timestamp_created       | datetime                                                            | not null


## portfolio
column_name             | data_type | details
------------------------|-----------|-----------------------
id                      | integer   | not null, primary key
timestamp_created       | datetime  | not null

##### backup option for multiple users/portfolios if follows 'join table' does not work well
column_name             | data_type                                                           | details
------------------------|---------------------------------------------------------------------|-----------------------
stock1                  | integer                                                             | foreign key (stocks)
stock1_shares_owned     | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null
stock2                  | integer                                                             | foreign key (stocks)
stock2_shares_owned     | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null
stock3                  | integer                                                             | foreign key (stocks)
stock3_shares_owned     | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null
stock4                  | integer                                                             | foreign key (stocks)
stock4_shares_owned     | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null
stock5                  | integer                                                             | foreign key (stocks)
stock5_shares_owned     | decimal (max_digits=19, decimal_places=3, default=Decimal('0.000')) | not null
