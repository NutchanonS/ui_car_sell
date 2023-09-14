#CREATE DATABASE naiworks;
#use naiwork;
# DROP DATABASE mydb;
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pns1.5997gg"
)

mycursor = mydb.cursor(buffered=True)
mydb.autocommit = True
mycursor.execute("""CREATE DATABASE naiwork;""")
mycursor.execute("""use naiwork;""")
create_carinfo="""
CREATE TABLE carinfo(
        -- ID INT AUTO_INCREMENT,
    car_no VARCHAR(20),
    brand_color VARCHAR(10),
    state VARCHAR(20),
    sell_date DATE,
    Tel VARCHAR(10),

    date_buy DATE,
    car_price INT,
    car_year VARCHAR(10),
    client_name VARCHAR(30),
    deposit INT,
    finance INT,
    pay_down INT,
    remain_down INT,
    pay_down_date DATE,
    fee INT,
    oil_price INT,
    na INT,
    transfer_book_price INT,
    repair_price INT,
    driver_price INT,
    engine_oil_price INT,
    other_price INT,
    car_regist_date DATE,
    finance_place VARCHAR(20),

    PRIMARY KEY(car_no)
);
"""

mycursor.execute(create_carinfo)
# mycursor.execute("""INSERT INTO carinfo(car_no,brand_color,state,sell_date,Tel)
#     values("A","BM_black","รอขาย","2023-05-11","0814442233");""")