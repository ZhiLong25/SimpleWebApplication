from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from Forms import CreateAdminForm, CreateCustomerForm, SearchProduct, CreateProductForm, IndivProductForm, delivery_info

from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename
from os import path
import pandas as pd

import shelve, Customer, Admin, Products, Delivery, Cart

app = Flask(__name__)
app.config["SECRET_KEY"] = "randomkey123"
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads' # SET DESTINATION FILE


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos) # STORE IN THE APP

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/createProducts', methods=['GET', 'POST'])
def upload():
    product_form = CreateProductForm()

    if product_form.validate_on_submit():

        print("STORE")
        # STORING PRODUCT INTO DB
        products_dict = {}
        prod_list = []
        db = shelve.open('products.db', 'c')

        try:
            products_dict = db['Products']

        except:
            print("Error in retrieving Products from products.db.")

        for key in products_dict:
            prod = products_dict.get(key)
            prod_list.append(prod)

        prod_ref = product_form.ref_no.data

        #DICTIONARY IS EMPTY
        if products_dict == False:
            products = Products.Products(product_form.photo.data.filename, product_form.prod_name.data, product_form.description.data, product_form.price.data,
                                     product_form.stock.data, product_form.ref_no.data)
            products_dict[products.get_reference()] = products
            db['Products'] = products_dict

            filename = secure_filename(product_form.photo.data.filename)
            product_form.photo.data.save('uploads/' + filename)
        else:
            if prod_ref in products_dict:

                flash("Product reference already exists, Please enter another reference no.")

                return redirect(url_for('upload'))
            else:

                products = Products.Products(product_form.photo.data.filename, product_form.prod_name.data, product_form.description.data, product_form.price.data,
                                     product_form.stock.data, product_form.ref_no.data)
                products_dict[products.get_reference()] = products
                db['Products'] = products_dict

                filename = secure_filename(product_form.photo.data.filename)
                product_form.photo.data.save('uploads/' + filename)

                # df = pd.read_excel('inventory.xlsx')
                #
                # current_prod = []
                # current_prod.append([product_form.photo.data.filename, product_form.prod_name.data, product_form.description.data, product_form.price.data,
                #                      product_form.stock.data, product_form.ref_no.data])
                #
                #
                # print(current_prod)
                # print("list")
                #
                # rows = df.shape[0]
                #
                # df.append(current_prod)
                # print(df)

                # df.loc[int(rows)+1] = [(product_form.photo.data.filename, product_form.prod_name.data, product_form.description.data, product_form.price.data,
                #                      product_form.stock.data, product_form.ref_no.data)]
                # df.to_excel('inventory.xlsx',index=False)

        db.close()

        print("Stored Product")



        return redirect(url_for('retrieve_products'))

    return render_template('createProducts.html', form=product_form)

@app.route('/retrieveProd', methods=['GET', 'POST'])
def retrieve_products():
    product_list = []
    product_dict = {}
    db = shelve.open('products.db', 'r')
    product_dict = db['Products']
    db.close()

    print(product_dict)
    for key in product_dict:
        product = product_dict.get(key)
        product_list.append(product)

    return render_template('retrieveProducts.html', prod_count=len(product_list), prod_list=product_list)


@app.route('/updateProducts/<int:id>', methods=['GET', 'POST'])
def update_products(id):
        update_product_form = CreateProductForm()
        if request.method == 'POST' and update_product_form.validate():
            prod_dict = {}
            db = shelve.open('products.db', 'w')
            prod_dict = db['Products']

            prod_ref = update_product_form.ref_no.data
            if prod_ref in prod_dict:
                print("exist")
                flash("Product reference already exists, Please enter another reference no.")
                return redirect(request.url)
            else:
                product = prod_dict.get(id)

                product.set_image(update_product_form.photo.data.filename)

                product.set_name(update_product_form.prod_name.data)
                product.set_description(update_product_form.description.data)
                product.set_price(update_product_form.price.data)
                product.set_stock(update_product_form.stock.data)
                product.set_reference(update_product_form.ref_no.data)

                db['Products'] = prod_dict
                db.close()

                return redirect("retrieve_products")
        else:
            prod_dict = {}
            db = shelve.open('products.db', 'w')
            prod_dict = db['Products']
            db.close()

            product = prod_dict.get(id)
            product_id = product.get_product_id()

            image = product.get_image()

            update_product_form.photo.data = product.get_image()
            update_product_form.prod_name.data = product.get_name()
            update_product_form.description.data = product.get_description()
            update_product_form.price.data = product.get_price()
            update_product_form.stock.data = product.get_stock()
            update_product_form.ref_no.data = product.get_reference()


        return render_template('updateProducts.html', form=update_product_form, prod_id=product_id, image=image)


@app.route('/individualProducts/<int:id>', methods=['GET', 'POST'])
def individual_prod(id):
    form = IndivProductForm(request.form)

    # RETRIEVE ALL PRODUCTS
    db = shelve.open('products.db', 'r')
    prod_dict = db['Products']
    db.close()
    product = prod_dict.get(id)
    product_id = product.get_product_id()
    prod_image = product.get_image()
    prod_name = product.get_name()
    description = product.get_description()
    prod_price = product.get_price()

    prod_quan = form.quantity.data

    # IF CUSTOMER ADDED PRODUCTS INTO CART
    if request.method == 'POST' and form.validate():
        cart_dict = {}
        currentUser = "Sample@johndoe.com"
        dbext = ".db"
        currentdb = currentUser + dbext


        if path.exists(currentdb):
            print("exist")

        else:
            print("no")
            db = shelve.open(currentUser+dbext, 'c', writeback=True)
            try:
                cart_dict = db[currentUser]

            except:
                print("Error retrieving data from db")

            # CHECK IF PRODUCT ALREADY EXISTS IN CART
            if prod_name in cart_dict:
                # ADD 1 IF ALREADY EXISTS IN CART
                prod = cart_dict.get(prod_name)
                cart_amt = int(prod.get_prodquan())

                cart_amt += prod_quan

                itemList = Cart.Cart(product_id,prod_image, prod_name, prod_price, cart_amt)
                cart_dict[prod_name] = itemList
                db[currentUser] = cart_dict

                return redirect(url_for("shoppingCart"))
            else:
                print("not in dict")
                # ADD IN DICTIONARY NORMALLY
                itemList = Cart.Cart(product_id,prod_image, prod_name, prod_price, prod_quan)
                cart_dict[prod_name] = itemList
                db[currentUser] = cart_dict

                return redirect(url_for("shoppingCart"))

            db.close()
    return render_template('individualProducts.html', form=form, image=prod_image, prod_name=prod_name, desc=description, price=prod_price)

# CART
@app.route('/shoppingCart', methods=['POST', 'GET'])
def shoppingCart():
    form = IndivProductForm(request.form)

    currentUser = "Sample@johndoe.com"
    dbext = ".db"
    currentdb = currentUser + dbext

    shop_list = []
    cart_dict = {}

    db = shelve.open(currentdb, 'r')
    cart_dict = db[currentUser]

    db.close()

    total = 0
    for key in cart_dict:
        prod = cart_dict.get(key)
        shop_list.append(prod)

        product_total = prod.get_prodquan() * prod.get_prodprice()
        total += float(product_total)
        ftotal = f'{total:.2f}'
    if request.method == 'POST':
        if request.form['submit'] == 'Checkout':
            return redirect(url_for('checkout'))



    return render_template('shoppingCart.html', prod_list=shop_list, form=form, total=ftotal)


@app.route('/updatecart/<int:id>', methods=['POST'])
def updatecart(id):
    form = IndivProductForm(request.form)
    if request.method == 'POST' and form.validate():
        quantity = request.form.get('quantity')
        print(quantity)

        currentUser = "Sample@johndoe.com"
        dbext = ".db"
        currentdb = currentUser + dbext

        cart_dict = {}

        db = shelve.open(currentdb, 'w')
        cart_dict = db[currentUser]

        for key in cart_dict:
            product = cart_dict.get(key)
            prod_id = product.get_product_id()
            print("here")
            print(prod_id)
            if prod_id == id:
                product.set_prodquan(quantity)
                print("cart updated")
                break

        db[currentUser] = cart_dict
        db.close()

        return redirect(url_for('shoppingCart'))

@app.route('/deleteCart/<int:id>', methods=['POST'])
def cart_delete(id):

    currentUser = "Sample@johndoe.com"
    dbext = ".db"
    currentdb = currentUser + dbext

    cart_dict = {}

    db = shelve.open(currentdb, 'w')
    cart_dict = db[currentUser]

    print(id)
    for key in cart_dict:
        product = cart_dict.get(key)
        prod_id = product.get_product_id()
        print(prod_id)
        if prod_id == id:
            cart_dict.pop(key)
            print("Removed from cart")
            break

    db[currentUser] = cart_dict
    db.close()

    return redirect(url_for('shoppingCart'))

# SUMMARY PAGE
@app.route('/summaryPage')
def summary():

    return render_template('summaryPage.html')

@app.route('/checkoutPage', methods=['POST', 'GET'])
def checkout():
    delivery_info_form = delivery_info(request.form)

    if request.method == 'POST' and delivery_info_form.validate():
        print("success")

    else:
        # return redirect(url_for('summary'))
        print("n")

    return render_template('checkoutPage.html', form=delivery_info_form)

@app.route('/deleteProducts/<int:id>', methods=['POST'])
def delete_products(id):

    prod_dict = {}
    db = shelve.open('products.db', 'w')
    prod_dict = db['Products']
    prod_dict.pop(id)
    db['Products'] = prod_dict
    db.close()
    return redirect(url_for('home'))

@app.route('/displayProducts')
def display_prod():
    prod_list = []
    product_dict = {}
    db = shelve.open('products.db', 'r')
    product_dict = db['Products']
    db.close()

    for key in product_dict:
        product = product_dict.get(key)
        prod_list.append(product)

    return render_template('displayProducts.html', prod_list=prod_list)


@app.route('/home', methods=['GET', 'POST'])
def home():
    # SEARCH FUNCTION
    form = SearchProduct(request.form)
    prod_dict = {}

    # SEARCH FUNCTION
    if request.method == 'POST':
        if request.form['submit'] == 'Search':

            db = shelve.open('products.db', 'r')
            prod_dict = db['Products']
            db.close()
            print(prod_dict)

            search = form.product.data.lower()
            print(search)

            searched = []
            for products in prod_dict:
                value = prod_dict.get(products)
                prod = value.get_name().lower()
                print(prod)

                if search in prod:

                    found_prod = prod_dict.get(products)
                    searched.append(found_prod)
                    print("Found")

                else:
                    print("Not found")
                    print(search)


            return render_template('searchResults.html', form=form, prod_list=searched)

    return render_template('home.html', form=form)

@app.route('/')
def start():
    return render_template('admin.html')  # STARTUP


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_customer_form = CreateCustomerForm(request.form)
    create_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Create Customer':

            if request.method == 'POST' and create_customer_form.validate():
                customers_dict = {}
                db = shelve.open('customer.db', 'c')

                try:
                    customers_dict = db['Customers']    # STORE VALUE IN LOCAL DICT
                except:
                    print("Error in retrieving Customers from customer.db.")
                    customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                                 create_customer_form.gender.data, create_customer_form.username.data,
                                                 create_customer_form.password.data, create_customer_form.email.data,
                                                 create_customer_form.phoneno.data, create_customer_form.date_joined.data,
                                                 create_customer_form.membership.data)
                    customers_dict[customer.get_customer_id()] = customer # ADD VALUE INTO DICTONARY
                    db['Customers'] = customers_dict    # UPDATE NEW DICTIONARY

                # ADD WHEN TRY STATEMENT PASS
                customer1 = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                             create_customer_form.gender.data, create_customer_form.username.data,
                                             create_customer_form.password.data, create_customer_form.email.data,
                                             create_customer_form.phoneno.data, create_customer_form.date_joined.data,
                                             create_customer_form.membership.data)
                customers_dict[customer1.get_customer_id()] = customer1
                db['Customers'] = customers_dict

                db.close()

                return redirect(url_for('create_user'))


        elif request.form['submit'] == 'Create Admin':
            # ADMIN SEGMENT
            print('Admin')
            if request.method == 'POST' and create_admin_form.validate():
                admin_dict = {}
                db = shelve.open('admin.db', 'c')

                try:
                    admin_dict = db['Admin']
                except:
                    print("Error in retrieving Users from admin.db.")

                    admin = Admin.Admin(create_admin_form.first_name.data, create_admin_form.last_name.data,
                                        create_admin_form.gender.data,
                                        create_admin_form.username.data, create_admin_form.password.data,
                                        create_admin_form.email.data, create_admin_form.phoneno.data,
                                        create_admin_form.role.data)
                    admin_dict[admin.get_user_id()] = admin
                    db['Admin'] = admin_dict


                admin = Admin.Admin(create_admin_form.first_name.data, create_admin_form.last_name.data,
                        create_admin_form.gender.data,
                        create_admin_form.username.data, create_admin_form.password.data,
                        create_admin_form.email.data, create_admin_form.phoneno.data,
                        create_admin_form.role.data)

                admin_dict[admin.get_user_id()] = admin
                db['Admin'] = admin_dict

                db.close()

                return redirect(url_for('create_user'))

    return render_template('createUser.html', cust_form=create_customer_form, admin_form=create_admin_form)


@app.route('/retrieveUsers', methods=['GET', 'POST'])
def retrieve_users():
    customer_list = []
    admin_list = []
    selected = "customer"

    if request.method == 'POST':
        if request.form['submit'] == 'Retrieve Customer':
            selected = "customer"
            customer_dict = {}
            db = shelve.open('customer.db', 'r')
            customer_dict = db['Customers']

            db.close()

            for key in customer_dict:
                user = customer_dict.get(key)
                customer_list.append(user)

        elif request.form['submit'] == 'Retrieve Admin':
            selected = "admin"
            admin_dict = {}
            db = shelve.open('admin.db', 'r')
            admin_dict = db['Admin']

            db.close()

            for key in admin_dict:
                user = admin_dict.get(key)
                admin_list.append(user)


    return render_template('retrieveUsers.html', cust_count=len(customer_list), admin_count=len(admin_list),
                           cust_list=customer_list, admin_list=admin_list, select=selected)


@app.route('/updateUser/<int:id>/<selected>', methods=['GET', 'POST'])
def update_user(id, selected):
    if selected == 'customer':
        select = "customer"
        update_cust_form = CreateCustomerForm(request.form)
        if request.method == 'POST' and update_cust_form.validate():

            cust_dict = {}
            db = shelve.open('customer.db', 'w')
            cust_dict = db['Customers']

            for customer in cust_dict.values():
                if customer.get_username() == update_cust_form.username.data:
                    print("exist")
                    flash("Customer Username already exists. Please choose a different username.", "danger")
                    return redirect(request.url)

                else:
                    customer = cust_dict.get(id)
                    customer.set_first_name(update_cust_form.first_name.data)
                    customer.set_last_name(update_cust_form.last_name.data)
                    customer.set_gender(update_cust_form.gender.data)
                    customer.set_email(update_cust_form.email.data)
                    customer.set_username(update_cust_form.username.data)
                    customer.set_password(update_cust_form.password.data)
                    customer.set_phone_number(update_cust_form.phoneno.data)
                    customer.set_membership(update_cust_form.membership.data)

                    db['Customers'] = cust_dict
                    db.close()

            return redirect(url_for('retrieve_users'))
        else:
            cust_dict = {}
            db = shelve.open('customer.db', 'r')
            cust_dict = db['Customers']
            db.close()

            customer = cust_dict.get(id)
            print(customer)
            cust_id = customer.get_customer_id()

            update_cust_form.first_name.data = customer.get_first_name()
            update_cust_form.last_name.data = customer.get_last_name()
            update_cust_form.email.data = customer.get_email()
            update_cust_form.gender.data = customer.get_gender()
            update_cust_form.username.data = customer.get_username()
            update_cust_form.password.data = customer.get_password()
            update_cust_form.phoneno.data = customer.get_phone_number()
            update_cust_form.membership.data = customer.get_membership()

        return render_template('updateUser.html', cust_form=update_cust_form, cust_id=cust_id, select=select)

    elif selected == 'admin':
        select = "admin"
        print('admin')
        update_admin_form = CreateAdminForm(request.form)
        if request.method == 'POST' and update_admin_form.validate():

            admin_dict = {}
            db = shelve.open('admin.db', 'w')
            admin_dict = db['Admin']
            admin = admin_dict.get(id)

            for admin in admin_dict.values():
                if admin.get_username() == update_admin_form.username.data:
                    flash("Admin Username already exists. Please choose a different username.", "danger")

                else:
                    admin.set_first_name(update_admin_form.first_name.data)
                    admin.set_last_name(update_admin_form.last_name.data)
                    admin.set_gender(update_admin_form.gender.data)
                    admin.set_email(update_admin_form.email.data)
                    admin.set_username(update_admin_form.username.data)
                    admin.set_password(update_admin_form.password.data)
                    admin.set_phone_number(update_admin_form.phoneno.data)
                    admin.set_role(update_admin_form.role.data)

                    db['Admin'] = admin_dict
                    db.close()

            return redirect(url_for('retrieve_users'))
        else:
            admin_dict = {}
            db = shelve.open('admin.db', 'r')
            admin_dict = db['Admin']
            db.close()

            admin = admin_dict.get(id)
            admin_id = admin.get_user_id()

            update_admin_form.first_name.data = admin.get_first_name()
            update_admin_form.last_name.data = admin.get_last_name()
            update_admin_form.email.data = admin.get_email()
            update_admin_form.gender.data = admin.get_gender()
            update_admin_form.username.data = admin.get_username()
            update_admin_form.password.data = admin.get_password()
            update_admin_form.phoneno.data = admin.get_phone_number()
            update_admin_form.role.data = admin.get_role()

        return render_template('updateUser.html', admin_form=update_admin_form, admin_id=admin_id, select=select)


@app.route('/deleteUser/<int:id>/<select>', methods=['POST'])
def delete_user(id, select):

    if select == "customer":
        cust_dict = {}
        db = shelve.open('customer.db', 'w')
        cust_dict = db['Customers']
        cust_dict.pop(id)
        db['Customers'] = cust_dict
        db.close()
    elif select == "admin":
        admin_dict = {}
        db = shelve.open('admin.db', 'w')
        admin_dict = db['Admin']
        admin_dict.pop(id)
        db['Admin'] = admin_dict
        db.close()

    return redirect(url_for('retrieve_users'))


if __name__ == '__main__':
    app.run()
