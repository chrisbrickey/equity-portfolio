# WIP Schema

*don't forget `from decimal import Decimal` on models*


## stocks
column_name             | data_type                                 | details
------------------------|-------------------------------------------|-----------------------
id                      | integer                                   | not null, primary key
company_name            | string (max_length = 200)                 | not null
symbol                  | string (max_length = 20)                  | not null, unique   
last_trade_price        | decimal (max_digits=19, decimal_places=3) |    
last_trade_time         | datetime                                  |
timestamp_last_updated  | datetime                                  | not null
timestamp_created       | datetime                                  | not null

##### may not use
column_name             | data_type                                 | details
------------------------|-------------------------------------------|-----------------------
shares_owned            | decimal (max_digits=19, decimal_places=3) |  


## portfolio
column_name             | data_type | details
------------------------|-----------|-----------------------
id                      | integer   | not null, primary key
timestamp_last_updated  | datetime  | not null
timestamp_created       | datetime  | not null

##### may not use
column_name             | data_type | details
------------------------|-----------|-----------------------
stock1                  | integer   | foreign key (stocks)
stock2                  | integer   | foreign key (stocks)
stock3                  | integer   | foreign key (stocks)
stock4                  | integer   | foreign key (stocks)
stock5                  | integer   | foreign key (stocks)


## follows
column_name             | data_type | details
------------------------|-----------|-----------------------
id                      | integer   | not null, primary key
portfolio_id            | integer   | not null, foreign key (portfolios)
stock_id                | integer   | not null, foreign key (stocks), unique (portfolio_id)
shares_owned            | integer   |
timestamp_last_updated  | datetime  | not null
timestamp_created       | datetime  | not null
