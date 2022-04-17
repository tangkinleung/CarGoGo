from datetime import datetime

import MySQLdb

def db_connection():
    conn = MySQLdb.connect("localhost", "root", "p^dLP9EQ4Tnv@W93", "cargogo_optimized")
    return conn

def create_buyer_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS buyer("
        "buyerId varchar(36) NOT NULL, "
        "username varchar(25) NOT NULL, "
        "password varchar(14) NOT NULL, "
        "income INT NOT NULL, "
        "CHECK (income > 0),"
        "email varchar(50) NOT NULL, "
        "UNIQUE (email), "
        "CHECK (email LIKE '%_@_%._%'), "
        "contact_number int(8) NOT NULL, "
        "UNIQUE (contact_number), "
        "CHECK (contact_number between 80000000 AND 99999999), "
        "PRIMARY KEY(buyerId)"
        ");"
    )

    cursor.execute("Drop Trigger IF EXISTS before_insert_table_buyer")

    cursor.execute(
        "CREATE TRIGGER before_insert_table_buyer "
        "before insert on buyer for each row "
        "set new.buyerId = uuid();"
    )


def create_seller_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS seller("
        "sellerId int(4) zerofill AUTO_INCREMENT NOT NULL, "
        "username varchar(25) NOT NULL, "
        "password varchar(14) NOT NULL, "
        "email varchar(50) NOT NULL, "
        "UNIQUE (email), "
        "CHECK (email LIKE '%_@_%._%'), "
        "contact_number int(8) NOT NULL, "
        "UNIQUE (contact_number), "
        "CHECK (contact_number between 80000000 AND 99999999), "
        "cardealerId varchar(36) NULL, "
        "PRIMARY KEY(sellerId), "
        "FOREIGN KEY (cardealerId) REFERENCES cardealer(cardealerId)"
        ");"
    )

    cursor.execute("Drop Trigger IF EXISTS before_insert_table_seller_cardealerId")
    cursor.execute(
        "CREATE TRIGGER before_insert_table_seller_cardealerId before insert on seller for each row "
        "IF (NEW.cardealerId = 'a') THEN "
        "SET  NEW.cardealerId = (select cardealerId from cardealer order by rand() limit 1); "
        "END IF"
    )


def create_carDealer_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS cardealer("
        "cardealerId varchar(36) NOT NULL, "
        "username varchar(25) NOT NULL, "
        "password varchar(25) NOT NULL, "
        "email varchar(50) NOT NULL, "
        "UNIQUE (email), "
        "CHECK (email LIKE '%_@_%._%'), "
        "contact_number int(8) NOT NULL, "
        "UNIQUE (contact_number), "
        "CHECK (contact_number between 80000000 AND 99999999), "
        "companyName varchar(25) NOT NULL, "
        "address varchar(75) NOT NULL, "
        "dealerLicense char(6) NOT NULL, "
        "rating float NOT NULL, "
        "CHECK (rating >= 0 AND rating <= 10), "
        "experience smallint NOT NULL, "
        "CHECK (experience >= 1 AND experience <= 45), "
        "PRIMARY KEY(cardealerId)"
        ");"
    )

    cursor.execute("Drop Trigger IF EXISTS before_insert_table_cardealer")

    cursor.execute(
       "CREATE TRIGGER before_insert_table_cardealer before insert on cardealer for each row "
       "set new.cardealerId = uuid();"
    )


def create_listing_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS vehicle("
        "vehicleId varchar(36) NOT NULL, "
        "sellerId int(4) zerofill NOT NULL, "
        "manufacturer varchar(15) NOT NULL, "
        "model varchar(35) NOT NULL, "
        "vehicleType varchar(11) NOT NULL, "
        "vehicleCondition varchar(9) NOT NULL, "
        "fuelType varchar(8) NOT NULL, "
        "mileage int NOT NULL, "
        "transmission varchar(9) NOT NULL, "
        "colour varchar(8) NOT NULL, "
        "price int NOT NULL, "
        "available boolean NOT NULL, "
        "coeLeft varchar(8) NOT NULL, "
        "depreciation int NOT NULL, "
        "mileageConsumption int NOT NULL, "
        "listedDate datetime NOT NULL, "
        "PRIMARY KEY(vehicleId), "
        "FOREIGN KEY (sellerId) REFERENCES seller(sellerId)"
        ");"
    )
    cursor.execute("Drop Trigger IF EXISTS before_insert_table_vehicle")
    cursor.execute(
        "CREATE TRIGGER before_insert_table_vehicle before insert on vehicle for each row "
        "set new.listedDate = NOW(), "
        "new.vehicleId = UUID();"
    )
    cursor.execute("Drop Trigger IF EXISTS before_insert_table_vehicle_sellerId")
    cursor.execute(
        "CREATE TRIGGER before_insert_table_vehicle_sellerId before insert on vehicle for each row "
        "IF (NEW.sellerId = 0) THEN "
        "SET NEW.sellerId = (select sellerId from seller order by RAND() limit 1); "
        "END IF"
    )

def create_contract_table():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS contract("
        "contractId varchar(36) NOT NULL, "
        "buyerId varchar(36) NOT NULL, "
        "cardealerId varchar(36) NOT NULL, "
        "sellerId int(4) zerofill NOT NULL, "
        "vehicleId varchar(36) NOT NULL, "
        "contractDate datetime NOT NULL, "
        "PRIMARY KEY(contractId), "
        "FOREIGN KEY (buyerId) REFERENCES buyer(buyerId), "
        "FOREIGN KEY (cardealerId) REFERENCES cardealer(cardealerId), "
        "FOREIGN KEY (vehicleId) REFERENCES vehicle(vehicleId), "
        "FOREIGN KEY (sellerId) REFERENCES seller(sellerId)"
        ");"
    )

    cursor.execute("Drop Trigger IF EXISTS before_insert_table_contract")

    cursor.execute(
        "CREATE TRIGGER before_insert_table_contract before insert on contract for each row "
        "set new.contractDate = NOW(), "
        "new.contractId = UUID();"
    )


def insert_buyer(id, username, password, income, email, contact):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO buyer VALUES ('{0}','{1}','{2}',{3},'{4}',{5});".format(id, username, password, int(income), email,
                                                                                int(contact))
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def insert_seller(id, username, password, email, contact):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO seller (sellerId, username, password, email, contact_number) VALUES ({0},'{1}','{2}','{3}',{4});".format(int(id), username, password, email,
                                                                                    int(contact))
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def insert_carDealer(id, username, password, email, contact, companyName, address, dealerLicense, rating, experience):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO cardealer VALUES ('{0}','{1}','{2}','{3}',{4},'{5}','{6}','{7}','{8}',{9}"
            ");".format(id, username, password, email, int(contact), companyName, address, dealerLicense, float(rating),
                        int(experience))
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def insert_listing(vehicleId, sellerId, manufacturer, model, vehicleType, vehicleCondition, fuelType, mileage,
                   transmission, colour, price, available, coeLeft, depreciation, mileageConsumption, listedDate):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO vehicle VALUES ('{0}',{1},'{2}','{3}','{4}','{5}','{6}',{7},'{8}','{9}',{10},{11},'{12}',{13},"
            "{14},'{15}');".format(vehicleId, int(sellerId), manufacturer, model, vehicleType, vehicleCondition, fuelType,
                                int(mileage), transmission, colour, int(price), bool(available), coeLeft,
                                int(depreciation), int(mileageConsumption), str(listedDate))
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def login_buyer(username):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM buyer WHERE username = '{0}'".format(username)
    )

    data = cursor.fetchone()
    return data


def get_buyerId(username):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT buyerId FROM buyer WHERE username = '{0}'".format(username)
    )

    data = cursor.fetchone()
    return data


def get_buyerProfileDetails(buyerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, contact_number, income FROM buyer WHERE buyerId = '{0}'".format(buyerId)
    )

    data = cursor.fetchone()
    return data


def get_buyerProfileDetailsForEdit(buyerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, contact_number, income, buyerId, password FROM buyer WHERE buyerId = '{0}'".format(buyerId)
    )

    data = cursor.fetchone()
    return data


def update_editBuyerProfile(buyerId, username, email, password, contact, income):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE buyer SET username='{1}', email='{2}', password='{3}', contact_number='{4}', income='{5}' "
            "WHERE buyerId = '{0}'".format(buyerId, username, email, password, contact, income)
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()

def login_seller(username):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM seller WHERE username = '{0}'".format(username)
    )

    data = cursor.fetchone()
    return data


def get_sellerId(username):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT sellerId FROM seller WHERE username = '{0}'".format(username)
    )

    data = cursor.fetchone()
    return data


def get_vehicleData(sellerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, vehicleType, vehicleCondition, fuelType, mileage, transmission, colour, price, "
        "available, coeLeft, depreciation, mileageConsumption, date(listedDate), vehicleId FROM vehicle "
        "WHERE sellerId = {0}".format(int(sellerId))
    )

    data = cursor.fetchall()
    return data


def get_vehicleDataForEdit(vehicleId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, vehicleType, vehicleCondition, fuelType, mileage, transmission, colour, price, "
        "available, coeLeft, depreciation, mileageConsumption, date(listedDate), vehicleId FROM vehicle "
        "WHERE vehicleId = '{0}'".format(vehicleId)
    )

    data = cursor.fetchone()
    return data


def update_editListing(vehicleId, model, vehicleType, manufacturer, fuelType, mileage, colour, transmission,
                       consumption, depreciation, coeLeft, condition, price, available):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE vehicle SET model='{1}', vehicleType='{2}', manufacturer='{3}', fuelType='{4}', mileage='{5}', "
        "colour='{6}', transmission='{7}', mileageConsumption='{8}', depreciation='{9}', coeLeft='{10}', "
        "vehicleCondition='{11}', price='{12}', available='{13}' "
        "WHERE vehicleId = '{0}'".format(vehicleId, model, vehicleType, manufacturer, fuelType, mileage, colour,
                                         transmission, consumption, depreciation, coeLeft, condition, price, available)
    )
    conn.commit()


def deleteListing(vehicleId):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM vehicle WHERE vehicleId='{0}'".format(vehicleId)
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def get_sellerProfileDetails(sellerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, contact_number FROM seller WHERE sellerId = {0}".format(int(sellerId))
    )

    data = cursor.fetchone()
    return data


def get_sellerProfileDetailsForEdit(sellerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, contact_number, sellerId, password FROM seller WHERE sellerId = {0}".format(int(sellerId))
    )

    data = cursor.fetchone()
    return data


def update_editSellerProfile(sellerId, username, email, password, contact):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE seller SET username='{1}', email='{2}', password='{3}', contact_number='{4}' "
        "WHERE sellerId = {0}".format(int(sellerId), username, email, password, contact)
    )
    conn.commit()


def get_carDealerData():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT contact_number, companyName, address, dealerLicense, rating, experience, cardealerId FROM cardealer;"
    )

    data = cursor.fetchall()
    return data


def login_cardealer(username):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM cardealer WHERE username = '{0}'".format(username)
    )

    data = cursor.fetchone()
    return data


def get_cardealerId(username):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT cardealerId FROM cardealer WHERE username = '{0}'".format(username)
    )

    data = cursor.fetchone()
    return data


def get_cardealerProfileDetails(cardealerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, contact_number FROM cardealer WHERE cardealerId = '{0}'".format(cardealerId)
    )

    data = cursor.fetchone()
    return data


def get_cardealerProfileDetailsForEdit(cardealerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, email, contact_number, cardealerId, password FROM cardealer WHERE cardealerId = '{0}'".format(cardealerId)
    )

    data = cursor.fetchone()
    return data


def update_editCardealerProfile(cardealerId, username, email, password, contact):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE cardealer SET username='{1}', email='{2}', password='{3}', contact_number='{4}' "
        "WHERE cardealerId = '{0}'".format(cardealerId, username, email, password, contact)
    )
    conn.commit()


def get_vehicleDataForBuyerView():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, sellerId, "
        "mileageConsumption FROM vehicle WHERE available = 1;"
    )

    data = cursor.fetchall()
    return data


def get_vehicleDataForCarDetails(vehicleId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, vehicleType, vehicleCondition, fuelType, mileage, transmission, colour, price, "
        "available, coeLeft, depreciation, mileageConsumption, vehicleId, sellerId FROM vehicle "
        "WHERE vehicleId='{0}'".format(vehicleId)
    )

    data = cursor.fetchone()
    return data


def filterModel(model):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle WHERE model = '{0}' AND available = 1;".format(model)
    )

    data = cursor.fetchall()
    return data


def filterFuelType(fuelType):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle WHERE fuelType = '{0}' AND available = 1;".format(fuelType)
    )

    data = cursor.fetchall()
    return data


def filterVehicleType(vehicleType):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle WHERE vehicleType = '{0}' AND available = 1;".format(vehicleType)
    )

    data = cursor.fetchall()
    return data


def filterColours(colour):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle WHERE colour = '{0}' AND available = 1;".format(colour)
    )

    data = cursor.fetchall()
    return data


def filterPrice(minPrice, maxPrice):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle WHERE price >= '{0}' AND price < '{1}' AND available = 1;".format(minPrice, maxPrice)
    )

    data = cursor.fetchall()
    return data


def filterMileage(minMileage, maxMileage):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle WHERE mileage >= '{0}' AND mileage < '{1}' AND available = 1;".format(minMileage, maxMileage)
    )

    data = cursor.fetchall()
    return data


def filterMileageConsumption(manufacturer):
    conn = db_connection()
    cursor = conn.cursor()
    print(manufacturer)
    cursor.execute(
        "SELECT manufacturer, model, price, vehicleId, fuelType, vehicleType, colour, mileage, available, "
        "mileageConsumption FROM vehicle v1 WHERE v1.mileageConsumption IN (SELECT MAX(v2.mileageConsumption) "
        "FROM vehicle v2 WHERE manufacturer = '{0}' AND available = 1) AND available = 1 AND manufacturer = '{0}'".format(manufacturer)
    )

    data = cursor.fetchall()
    return data


def selectCarDealer(cardealerId, sellerId):
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE seller SET cardealerId = '{0}' WHERE sellerId = {1}".format(cardealerId, int(sellerId))
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def get_carDealerId_for_contract(sellerId, vehicleId):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "select distinct(s.cardealerId) from seller s, vehicle v where s.sellerId=v.sellerId AND s.sellerId={0}"
        " AND vehicleId='{1}';".format(sellerId, vehicleId)
    )
    data = cursor.fetchone()
    return data[0]


def insert_contract(contractId, buyerId, cardealerId, sellerId, vehicleId, contractDate):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO contract VALUES ('{0}','{1}','{2}',{3}, '{4}', '{5}');".format(contractId, buyerId, cardealerId,
                                                                                        int(sellerId), vehicleId,
                                                                                        str(contractDate))
        )

        cursor.execute(
            "UPDATE vehicle SET available = 0 WHERE vehicleId = '{0}'".format(vehicleId)
        )
    except MySQLdb.Error:
        conn.rollback()
        cursor.close()
        conn.close()
    conn.commit()
    cursor.close()
    conn.close()


def viewContract(cardealerId):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM contract WHERE cardealerId = '{0}'".format(cardealerId)
    )

    data = cursor.fetchall()
    return data


def filterCompany(sortFilter):
    conn = db_connection()
    cursor = conn.cursor()

    if sortFilter == 'Ascending':
        cursor.execute(
            "SELECT contact_number, companyName, address, dealerLicense, rating, experience FROM cardealer "
            "ORDER BY companyName ASC;"
        )
    else:
        cursor.execute(
            "SELECT contact_number, companyName, address, dealerLicense, rating, experience FROM cardealer "
            "ORDER BY companyName DESC;"
        )

    data = cursor.fetchall()
    return data


def filterExperience(filterExp):
    conn = db_connection()
    cursor = conn.cursor()

    if filterExp == 'Min':
        cursor.execute(
            "SELECT contact_number, companyName, address, dealerLicense, rating, experience FROM cardealer "
            "WHERE experience = (SELECT MIN(experience) FROM cardealer);"
        )
    else:
        cursor.execute(
            "SELECT contact_number, companyName, address, dealerLicense, rating, experience FROM cardealer "
            "WHERE experience = (SELECT MAX(experience) FROM cardealer);"
        )

    data = cursor.fetchall()
    return data


def filterRating(minRating, maxRating):
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT contact_number, companyName, address, dealerLicense, rating, experience FROM cardealer "
        "WHERE rating >= {0} AND rating < {1};".format(int(minRating), int(maxRating))
    )

    data = cursor.fetchall()
    return data

