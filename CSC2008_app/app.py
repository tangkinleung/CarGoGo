from flask import Flask, render_template, request, url_for, flash, redirect
from datetime import date
import dbReading
import csv

app = Flask(__name__, template_folder="template")
app.config["SECRET_KEY"] = "24f4e39a07e30bb5c2ccd0f6c66cba04"

conn = dbReading.db_connection()
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS cargogo_optimized;")
cursor.execute("USE cargogo_optimized;")

dbReading.create_buyer_table()
dbReading.create_carDealer_table()
dbReading.create_seller_table()
dbReading.create_listing_table()
dbReading.create_contract_table()

sellerId = ""
buyerId = ""
cardealerId = ""

cursor.execute("SELECT * FROM buyer;")
data = cursor.fetchall()
if not data:
    buyer_data = csv.reader(open('data/buyer.csv'))
    header = next(buyer_data)
    print('Importing the buyer CSV Files')
    for row in buyer_data:
        print(row)
        cursor.execute(
            "INSERT INTO buyer (buyerId,username,password,income,email,contact_number) VALUES (%s, %s, %s, %s, %s, %s)",
            row)

    conn.commit()

cursor.execute("SELECT * FROM cardealer;")
data = cursor.fetchall()
if not data:
    cardealer_data = csv.reader(open('data/dealer.csv'))
    header = next(cardealer_data)
    print('Importing the dealer CSV Files')
    for row in cardealer_data:
        print(row)
        cursor.execute(
            "INSERT INTO cardealer (cardealerId, username,password,email,contact_number,companyName,address, "
            "dealerLicense, rating, experience) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",row)

    conn.commit()

cursor.execute("SELECT * FROM seller;")
data = cursor.fetchall()
if not data:
    seller_data = csv.reader(open('data/seller.csv'))
    header = next(seller_data)
    print('Importing the seller CSV Files')
    for row in seller_data:
        print(row)
        cursor.execute(
            "INSERT INTO seller (username,password,email,contact_number,cardealerId) VALUES ('{0}', '{1}', '{2}', {3}, '{4}')".format(
                row[0],row[1],row[2],int(row[3]),row[4]))

    conn.commit()

cursor.execute("SELECT * FROM vehicle;")
data = cursor.fetchall()
if not data:
    vehicle_data = csv.reader(open('data/vehicles.csv'))
    header = next(vehicle_data)
    print('Importing the vehicle CSV Files')
    for row in vehicle_data:
        print(row)
        cursor.execute(
            "INSERT INTO vehicle(sellerId,manufacturer,model,vehicleType,vehicleCondition,fuelType,mileage,"
            "transmission,colour,price,available,coeLeft,depreciation,mileageConsumption) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', {9}, {10}, '{11}', {12}, {13});"
            .format(int(row[0]),row[1],row[2],row[3],row[4],row[5],int(row[6]),row[7],row[8],int(row[9]),int(row[10]),row[11],int(row[12]),int(row[13])))

    conn.commit()

# Choose preference for login or register
@app.route("/")
def beforeLogin():
    return render_template("beforeLogin.html")


# csv_data = csv.reader('data/buyer.csv')
# next(csv_data)
# for row in csv_data:
#     cursor.execute("INSERT INTO buyer VALUES ('{0}','{1}','{2}',{3},'{4}',{5});".format("", row[0], row[1], int(row[2]), row[3], int(row[4])))
# conn.commit()
# cursor.close()
#

# with open('data/buyer.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=';')
#     sql = "INSERT INTO buyer VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format()
#     for row in csv_reader:
#         print(row)
#         # print(cursor.rowcount, "was inserted.")
#         cursor.executemany(sql, csv_reader)
#         # cursor.execute(sql, row, multi=True)
#         conn.commit()

# Login as buyer
@app.route("/loginBuyer", endpoint="loginBuyer", methods=['GET', 'POST'])
def loginBuyer():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            user_pw = dbReading.login_buyer(username)
            if password == user_pw[0]:
                global buyerId
                buyerId = dbReading.get_buyerId(username)[0]
                return redirect(url_for('buyerHome'))
            else:
                flash('Login unsuccessful. Please check username and password', 'danger')
        except TypeError:
            flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template("buyerLogin.html", title="Buyer Login")


# Login as seller
@app.route("/loginSeller", endpoint="loginSeller", methods=['GET', 'POST'])
def loginSeller():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            user_pw = dbReading.login_seller(username)
            if password == user_pw[0]:
                global sellerId
                sellerId = dbReading.get_sellerId(username)[0]
                return redirect(url_for('sellerHome'))
            else:
                flash('Login unsuccessful. Please check username and password', 'danger')
        except TypeError:
            flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template("sellerLogin.html", title="Seller Login")


# Login as car dealer
@app.route("/loginCarDealer", endpoint="loginCarDealer", methods=['GET', 'POST'])
def loginCarDealer():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            user_pw = dbReading.login_cardealer(username)
            if password == user_pw[0]:
                global cardealerId
                cardealerId = dbReading.get_cardealerId(username)[0]
                return redirect(url_for('carDealerHome'))
            else:
                flash('Login unsuccessful. Please check username and password', 'danger')
        except TypeError:
            flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template("carDealerLogin.html", title="Car Dealer Login")


# Logout
@app.route("/logout", endpoint="logout")
def logout():
    return render_template("logout.html", title="Logout")


# Sign up as buyer
@app.route("/signUpBuyer", endpoint="signUpBuyer")
def signUpBuyer():
    return render_template("buyerSignUp.html", title="Buyer Sign Up")


# Sign up as seller
@app.route("/signUpSeller", endpoint="signUpSeller")
def signUpSeller():
    return render_template("sellerSignUp.html", title="Seller Sign Up")


# Register options as buyer or seller
@app.route("/registerOptions", endpoint="registerOptions")
def registerOptions():
    return render_template("registerOptions.html", title="Register Options")


# Register as buyer
@app.route("/registerBuyer", endpoint="registerBuyer", methods=['GET', 'POST'])
def registerBuyer():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        income = request.form['income']
        contact = request.form['contact']

        dbReading.insert_buyer("", username, password, income, email, contact)

        return render_template("buyerSignUpSuccess.html", title="Register Buyer")
    else:
        return render_template("buyerSignUp.html", title="Register Buyer")


# Register as seller
@app.route("/registerSeller", endpoint="registerSeller", methods=['GET', 'POST'])
def registerSeller():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        contact = request.form['contact']
        # id = uuid.uuid4()

        dbReading.insert_seller(0, username, password, email, contact)

        return render_template("sellerSignUpSuccess.html", title="Register Buyer")
    else:
        return render_template("sellerSignUp.html", title="Register Seller")


# Register as seller
@app.route("/registerCarDealer", endpoint="registerCarDealer", methods=['GET', 'POST'])
def registerCarDealer():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        contact = request.form['contact']
        companyName = request.form['companyName']
        address = request.form['address']
        dealerLicense = request.form['dealerLicense']
        rating = request.form['rating']
        experience = request.form['experience']
        dbReading.insert_carDealer("", username, password, email, contact, companyName, address, dealerLicense,
                                   rating,
                                   experience)

        return render_template("carDealerSignUpSuccess.html", title="Register Buyer")
    else:
        return render_template("carDealerSignUp.html", title="Register Car Dealer")


# Buyer sign up success
@app.route("/buyerSignUpSuccess", endpoint="buyerSignUpSuccess")
def buyerSignUpSuccess():
    return render_template("buyerSignUpSuccess.html", title="Buyer Sign Up Success")


# Seller sign up success
@app.route("/sellerSignUpSuccess", endpoint="sellerSignUpSuccess")
def buyerSignUpSuccess():
    return render_template("sellerSignUpSuccess.html", title="Seller Sign Up Success")


# Car Dealer sign up success
@app.route("/carDealerSignUpSuccess", endpoint="carDealerSignUpSuccess")
def buyerSignUpSuccess():
    return render_template("carDealerSignUpSuccess.html", title="Car Dealer Sign Up Success")


# Seller sign up success
@app.route("/buyerPurchaseCarSuccess", endpoint="buyerPurchaseCarSuccess")
def buyerPurchaseCarSuccess():
    return render_template("buyerPurchaseCarSuccess.html", title="Buyer Purchase Car Success")


# Sign in options as buyer or seller
@app.route("/signInOptions", endpoint="signInOptions")
def signInOptions():
    return render_template("signInOptions.html", title="Sign In Options")


# Buyer homepage
@app.route("/buyerHome", methods=["GET", "POST"], endpoint="buyerHome")
def buyerHome():
    if request.method == "POST":
        if request.form["viewCarDetails"] == "view":
            buyerCarDetails()
    else:
        vehicleData = dbReading.get_vehicleDataForBuyerView()
        model = ['a3', 'a4', '2 series', 'elantra', 'accord']
        fuelType = ['gas', 'hybrid', 'diesel']
        vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
        colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
        price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
                 '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
                 '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
        mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
                   '400000 to 500000km',
                   '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
        mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

        return render_template("buyerHome.html", title="Buyer Homepage", data=vehicleData, model=model,
                               fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                               mileage=mileage, mileageConsumption=mileageConsumption)


# Buyer Car Details
@app.route("/buyerCarDetails", methods=["GET", "POST"], endpoint="buyerCarDetails")
def buyerCarDetails():
    vehicleId = request.args.get('vehicleId')
    sellerId = request.args.get('sellerId')

    carDetails = dbReading.get_vehicleDataForCarDetails(vehicleId)
    cardealerId = dbReading.get_carDealerId_for_contract(sellerId, vehicleId)
    print(cardealerId)
    return render_template("buyerCarDetails.html", title="Buyer Car Details", data=carDetails,
                           info=[buyerId, vehicleId, sellerId, cardealerId])


@app.route("/purchaseCar", methods=["GET", "POST"], endpoint="purchaseCar")
def purchaseCar():
    buyerId = request.args.get('buyerId')
    vehicleId = request.args.get('vehicleId')
    sellerId = request.args.get('sellerId')
    cardealerId = request.args.get('cardealerId')
    contractDate = date.today().isoformat()

    dbReading.insert_contract("", buyerId, cardealerId, sellerId, vehicleId, contractDate)

    return render_template("buyerPurchaseCarSuccess.html")


@app.route("/filterModel", methods=["GET", "POST"], endpoint="filterModel")
def filterModel():
    modelSelected = request.args.get('modelSelected')
    filterModel = dbReading.filterModel(modelSelected)
    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterModel, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


@app.route("/filterFuelType", methods=["GET", "POST"], endpoint="filterFuelType")
def filterFuelType():
    fuelTypeSelected = request.args.get('fuelTypeSelected')
    filterFuelType = dbReading.filterFuelType(fuelTypeSelected)
    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterFuelType, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


@app.route("/filterVehicleType", methods=["GET", "POST"], endpoint="filterVehicleType")
def filterVehicleType():
    vehicleTypeSelected = request.args.get('vehicleTypeSelected')
    filterVehicleType = dbReading.filterVehicleType(vehicleTypeSelected)
    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterVehicleType, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


@app.route("/filterColours", methods=["GET", "POST"], endpoint="filterColours")
def filterColours():
    colourSelected = request.args.get('colourSelected')
    filterColours = dbReading.filterColours(colourSelected)
    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterColours, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


@app.route("/filterPrice", methods=["GET", "POST"], endpoint="filterPrice")
def filterPrice():
    minPrice = request.args.get('minPriceSelected').strip()[1:]
    maxPrice = request.args.get('maxPriceSelected').strip()[1:]
    filterPrice = dbReading.filterPrice(minPrice, maxPrice)

    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterPrice, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


@app.route("/filterMileage", methods=["GET", "POST"], endpoint="filterMileage")
def filterMileage():
    minMileage = request.args.get('minMileageSelected')
    maxMileage = request.args.get('maxMileageSelected').strip()[:6]
    filterMileage = dbReading.filterMileage(minMileage, maxMileage)

    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterMileage, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


@app.route("/filterMileageConsumption", methods=["GET", "POST"], endpoint="filterMileageConsumption")
def filterMileageConsumption():
    manufacturerSelected = request.args.get('manufacturerSelected')
    filterMileageConsumption = dbReading.filterMileageConsumption(manufacturerSelected)
    print(manufacturerSelected)

    model = ['a3', 'a4', '2 series', 'elantra', 'accord']
    fuelType = ['gas', 'hybrid', 'diesel']
    vehicleType = ['hatchback', 'coupe', 'sedan', 'convertible']
    colours = ['black', 'white', 'grey', 'silver', 'red', 'blue', 'green', 'yellow', 'orange', 'pink']
    price = ['$1 to $15000', '$15000 to $30000', '$30000 to $45000', '$45000 to $60000', '$60000 to $75000',
             '$75000 to $90000', '$90000 to $115000', '$115000 to $130000', '$130000 to $145000',
             '$145000 to $160000', '$160000 to $175000', '$175000 to $200000']
    mileage = ['1 to 100000km', '100000 to 200000km', '200000 to 300000km', '300000 to 400000km',
               '400000 to 500000km',
               '500000 to 600000km', '600000 to 700000km', '700000 to 800000km', '800000 to 900000km']
    mileageConsumption = ['hyundai', 'audi', 'toyota', 'honda', 'bmw']

    return render_template("buyerHome.html", title="Buyer Car Details", data=filterMileageConsumption, model=model,
                           fuelType=fuelType, vehicleType=vehicleType, colours=colours, price=price,
                           mileage=mileage,
                           mileageConsumption=mileageConsumption)


# Buyer Profile
@app.route("/buyerProfile", methods=["GET", "POST"], endpoint="buyerProfile")
def buyerProfile():
    buyerProfileDetails = dbReading.get_buyerProfileDetails(buyerId)
    return render_template("buyerProfile.html", data=buyerProfileDetails)


# Buyer edit profile
@app.route("/buyerEditProfile", methods=["GET", "POST"], endpoint="buyerEditProfile")
def buyerEditProfile():
    buyerProfileDetails = dbReading.get_buyerProfileDetailsForEdit(buyerId)
    return render_template("buyerEditProfile.html", title="Buyer Edit Profile", data=buyerProfileDetails)


# For click edit button for buyer edit profile
@app.route("/confirmEditBuyerProfile", methods=["POST"], endpoint="confirmEditBuyerProfile")
def confirmEditBuyerProfile():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        income = request.form['income']

        dbReading.update_editBuyerProfile(buyerId, username, email, password, contact, income)
        return redirect(url_for('buyerProfile'))


# Seller homepage
@app.route("/sellerHome", methods=["GET", "POST"], endpoint="sellerHome")
def sellerHome():
    if request.method == "POST":
        if request.form["edit_Listing"] == "edit":
            editListing()
    else:
        listingHeader = (
            "Model",
            "Vehicle Type",
            "Manufacturer",
            "Fuel Type",
            "Mileage",
            "Colour",
            "Transmission",
            "Consumption",
            "Depreciation",
            "COE Left",
            "Condition",
            "Price",
            "Available",
            "Date Listed"
        )
        vehicleData = dbReading.get_vehicleData(sellerId)
        print(vehicleData)
        return render_template("sellerHome.html", title="Seller Homepage", headings=listingHeader, data=vehicleData)


@app.route("/confirmDeleteListing", methods=["GET", "POST"], endpoint="confirmDeleteListing")
def confirmDeleteListing():
    vehicleId = request.args.get('vehicleId')
    dbReading.deleteListing(vehicleId)
    return redirect(url_for('sellerHome'))


# Car dealer homepage
@app.route("/carDealerHome", endpoint="carDealerHome")
def carDealerHome():
    data = dbReading.viewContract(cardealerId)

    contractDetailsHeader = (
        "Contract ID",
        "Buyer ID",
        "Car Dealer ID",
        "Seller ID",
        "Vehicle ID",
        "Contract Date"
    )
    return render_template("carDealerHome.html", title="Car Dealer Homepage", headings=contractDetailsHeader,
                           data=data)


# Edit listing
@app.route("/editListing", methods=["GET", "POST"], endpoint="editListing")
def editListing():
    vehicleId = request.args.get('vehicleId')
    vehicleData = dbReading.get_vehicleDataForEdit(vehicleId)
    return render_template("editListing.html", title="Seller Create Listing", data=vehicleData)


# For click edit button for editing listing
@app.route("/confirmListing", methods=["POST"], endpoint="confirmListing")
def confirmListing():
    if request.method == "POST":
        vehicleId = request.args.get('vehicleId')
        model = request.form['model']
        vehicleType = request.form['vehicleType']
        manufacturer = request.form['manufacturer']
        fuelType = request.form['fuelType']
        mileage = request.form['mileage']
        colour = request.form['colour']
        transmission = request.form['transmission']
        consumption = request.form['consumption']
        depreciation = request.form['depreciation']
        coeLeft = request.form['coeLeft']
        condition = request.form['condition']
        price = request.form['price']
        available = request.form['available']

        dbReading.update_editListing(vehicleId, model, vehicleType, manufacturer, fuelType, mileage, colour,
                                     transmission, consumption, depreciation, coeLeft, condition, price, available)
        return redirect(url_for('sellerHome'))


# Create listing
@app.route("/createListing", endpoint="createListing", methods=['GET', 'POST'])
def createListing():
    if request.method == "POST":
        model = request.form['model']
        vehicleType = request.form['vehicleType']
        manufacturer = request.form['manufacturer']
        fuelType = request.form['fuelType']
        mileage = request.form['mileage']
        colour = request.form['colour']
        transmission = request.form['transmission']
        consumption = request.form['consumption']
        depreciation = request.form['depreciation']
        coeLeft = request.form['coe']
        condition = request.form['condition']
        price = request.form['price']
        available = request.form['checkAvailable']
        listedDate = date.today().isoformat()

        dbReading.insert_listing("", sellerId, manufacturer, model, vehicleType, condition, fuelType, mileage,
                                 transmission, colour, price, int(available), coeLeft, depreciation, consumption,
                                 listedDate)
        return redirect(url_for('sellerHome'))
    else:
        return render_template("createListing.html", title="Seller Create Listing")


# Seller Profile
@app.route("/sellerProfile", endpoint="sellerProfile", methods=['GET', 'POST'])
def sellerProfile():
    sellerProfileDetails = dbReading.get_sellerProfileDetails(sellerId)

    return render_template("sellerProfile.html", title="Seller Profile", data=sellerProfileDetails)


# Seller Edit Profile
@app.route("/sellerEditProfile", endpoint="sellerEditProfile", methods=["GET", "POST"])
def sellerEditProfile():
    sellerProfileDetails = dbReading.get_sellerProfileDetailsForEdit(sellerId)
    return render_template(
        "sellerEditProfile.html",
        data=sellerProfileDetails,
        title="Seller Edit Profile"
    )


# For click edit button for seller edit profile
@app.route("/confirmEditProfile", methods=["POST"], endpoint="confirmEditProfile")
def confirmEditProfile():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']

        dbReading.update_editSellerProfile(sellerId, username, email, password, contact)
        return redirect(url_for('sellerProfile'))


# Car dealer Profile
@app.route("/carDealerProfile", endpoint="carDealerProfile", methods=["GET", "POST"])
def carDealerProfile():
    cardealerProfileDetails = dbReading.get_cardealerProfileDetails(cardealerId)

    return render_template("carDealerProfile.html", title="Car Dealer Profile", data=cardealerProfileDetails)


# Car Dealer Edit Profile
@app.route("/carDealerEditProfile", endpoint="carDealerEditProfile", methods=["GET", "POST"])
def carDealerEditProfile():
    cardealerProfileDetails = dbReading.get_cardealerProfileDetailsForEdit(cardealerId)

    return render_template("carDealerEditProfile.html", title="Car Dealer Edit Profile",
                           data=cardealerProfileDetails)


# For click edit button for seller edit profile
@app.route("/confirmCardealerEditProfile", methods=["POST"], endpoint="confirmCardealerEditProfile")
def confirmCardealerEditProfile():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']

        dbReading.update_editCardealerProfile(cardealerId, username, email, password, contact)
        return redirect(url_for('carDealerProfile'))


# Car dealer reviews
@app.route("/carDealerReview", endpoint="carDealerReview")
def carDealerReview():
    filter = ['Ascending', 'Descending']
    experience = ['Min', 'Max']
    rating = ['0 to 4', '4 to 7', '7 to 10']

    dealerHeader = (
        "Company Name",
        "Address",
        "License",
        "Contact Number",
        "Rating (Out of 10)",
        "Experience (Years)",
    )

    carDealerData = dbReading.get_carDealerData()
    print(carDealerData)
    return render_template("carDealerReview.html", title="Car Dealer Review", headings=dealerHeader,
                           data=carDealerData,
                           filter=filter, filterExperience=experience, rating=rating)


@app.route("/chooseCarDealer", methods=["GET", "POST"], endpoint="chooseCarDealer")
def chooseCarDealer():
    cardealerId = request.args.get('cardealerId')
    print(cardealerId)
    print(sellerId)
    dbReading.selectCarDealer(cardealerId, sellerId)
    return redirect(url_for('sellerHome'))


@app.route("/filterCompanyName", methods=["GET", "POST"], endpoint="filterCompanyName")
def filterCompanyName():
    sortSelected = request.args.get('sortSelected')
    filterCompany = dbReading.filterCompany(sortSelected)
    filter = ['Ascending', 'Descending']
    experience = ['Min', 'Max']
    rating = ['0 to 4', '4 to 7', '7 to 10']

    dealerHeader = (
        "Company Name",
        "Address",
        "License",
        "Contact Number",
        "Rating (Out of 10)",
        "Experience (Years)",
    )

    return render_template("carDealerReview.html", data=filterCompany, headings=dealerHeader, filter=filter,
                           filterExperience=experience, rating=rating)


@app.route("/filterExperience", methods=["GET", "POST"], endpoint="filterExperience")
def filterExperience():
    experienceSelected = request.args.get('experienceSelected')
    filterExp = dbReading.filterExperience(experienceSelected)
    filter = ['Ascending', 'Descending']
    experience = ['Min', 'Max']
    rating = ['0 to 4', '4 to 7', '7 to 10']

    dealerHeader = (
        "Company Name",
        "Address",
        "License",
        "Contact Number",
        "Rating (Out of 10)",
        "Experience (Years)",
    )

    return render_template("carDealerReview.html", data=filterExp, headings=dealerHeader, filter=filter,
                           filterExperience=experience, rating=rating)


@app.route("/filterRating", methods=["GET", "POST"], endpoint="filterRating")
def filterRating():
    minRating = request.args.get('minRatingSelected').strip()
    maxRating = request.args.get('maxRatingSelected').strip()
    filterRating = dbReading.filterRating(minRating, maxRating)

    filter = ['Ascending', 'Descending']
    experience = ['Min', 'Max']
    rating = ['0 to 4', '4 to 7', '7 to 10']

    dealerHeader = (
        "Company Name",
        "Address",
        "License",
        "Contact Number",
        "Rating (Out of 10)",
        "Experience (Years)",
    )

    return render_template("carDealerReview.html", data=filterRating, headings=dealerHeader, filter=filter,
                           filterExperience=experience, rating=rating)


if __name__ == "__main__":
    # importData()
    app.run()
