from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.exceptions import abort
from flask_login import login_required, current_user
import sqlite3

from .forms import ProductForm

main = Blueprint('main', __name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_product(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?',
                        (product_id,)).fetchone()
    conn.close()
    if product is None:
        abort(404)
    return product

@main.route('/')
@main.route('/index')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products[:3])

@main.route('/<int:product_id>', methods=["GET", "POST"])
def product(product_id):
    if request.method == "POST":
        conn = get_db_connection()
        if not current_user.admin:
            conn.execute("INSERT INTO cart (product_id, user_id) VALUES (?, ?)",
                    (product_id, current_user.id,)
                    )
            conn.commit()
            conn.close()
        else:
            conn.execute("DELETE FROM products where id = ?",
                    (product_id,)
                    )
            conn.commit()
            conn.close()
            return redirect(url_for('main.index'))
    product = get_product(product_id)

    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews where product_id = ?',
                           (product_id,)).fetchall()
    conn.close()
    return render_template('product.html', product=product, reviews=reviews)

@main.route("/search_res", methods=["GET", "POST"])
def search_res():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        s_q = search_query
        search_query = search_query.split()
        conn = get_db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        results = []
        conn.close()
        process = "Process:      "
        for p in products:
            process += "p = " + str(p['name']) + "    "
            res = False
            for sq in search_query:
                if sq.lower() in str(p['name']).lower():
                    res = True
                else:
                    process
            if res:
                results.append(p)
    return render_template("search_res.html", search_query=s_q, products=results)

@main.route('/search_res/<category>')
def search_category(category):
    search_query = str(category).split()
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    results = []
    conn.close()
    process = "Process:      "
    for p in products:
        process += "p = " + str(p['name']) + "    "
        res = False
        for sq in search_query:
            if sq.lower() in str(p['name']).lower():
                res = True
            else:
                process
        if res:
            results.append(p)
    return render_template('category.html', products=results, search_query=str(category))

@main.route('/order/<int:order_id>')
@login_required
def order(order_id):
    if current_user.is_authenticated:
        if not current_user.admin:
            return render_template('404.html')
    conn = get_db_connection()
    product_order = conn.execute('SELECT * FROM product_order where order_id = ?',
                              (order_id,)).fetchall()
    order = conn.execute('SELECT * FROM orders where id = ?',
                              (order_id,)).fetchone()
    products = []
    for po in product_order:
        p = get_product(int(po['product_id']))
        products.append(p)
    conn.close()
    if order['ready'] == 1:
        ready = 'YES'
    else:
        ready = 'NO'
    if order['shipped'] == 1:
        shipped = 'YES'
    else:
        shipped = 'NO'
    cost = order['cost']

    address = ["2488  Crummit Lane, NY, 12450",
               "4822  Blackwell Street, 68547",
               "Beffe Eikstraat 208, 19893"]
    # a = random.randint(0, 2)
    return render_template('order.html', products=products, order_id=order_id,
                           ready=ready, shipped=shipped, cost=cost, address=address[0])

@main.route('/orders')
@login_required
def orders():
    if current_user.is_authenticated:
        if not current_user.admin:
            return render_template('404.html')
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    orders_new = []
    for o in orders:
        if o['ready'] == 1:
            ready = 'YES'
        else:
            ready = 'NO'
        if o['shipped'] == 1:
            shipped = 'YES'
        else:
            shipped = 'NO'
        order = {
            'id': o['id'],
            'ready': ready,
            'shipped': shipped,
            'cost': o['cost'],
            'priority': o['priority']
        }
        orders_new.append(order)
    return render_template('orders.html', orders=orders_new)

def change_ready_status(order_id, ready):
    conn = get_db_connection()
    if ready == 0:
        conn.execute("UPDATE orders SET ready=0 WHERE id = ?", (order_id,))
    else:
        conn.execute("UPDATE orders SET ready=1 WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()


def change_shipped_status(order_id, shipped):
    conn = get_db_connection()
    if shipped == 0:
        conn.execute("UPDATE orders SET shipped=0 WHERE id = ?", (order_id,))
    else:
        conn.execute("UPDATE orders SET shipped=1 WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

@main.route('/order/edit/<int:order_id>', methods=["GET", "POST"])
@login_required
def order_edit(order_id):
    if current_user.is_authenticated:
        if not current_user.admin:
            return render_template('404.html')
    if request.method == "POST":
        # ready and shipped
        ready = request.form.get("ready")
        shipped = request.form.get("shipped")
        if ready:
            change_ready_status(order_id, 1)
        else:
            change_ready_status(order_id, 0)
        if shipped:
            change_shipped_status(order_id, 1)
        else:
            change_shipped_status(order_id, 0)

    conn = get_db_connection()
    product_order = conn.execute('SELECT * FROM product_order where order_id = ?',
                              (order_id,)).fetchall()
    order = conn.execute('SELECT * FROM orders where id = ?',
                              (order_id,)).fetchone()
    products = []
    for po in product_order:
        p = get_product(int(po['product_id']))
        products.append(p)
    conn.close()
    return render_template('edit.html', order_id=order_id, products=products, order=order)

@main.route('/cart', methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "POST":
        conn = get_db_connection()
        conn.execute("DELETE FROM cart where user_id = ?",
                                 (current_user.id,))
        conn.commit()
        conn.close()
    user_id = current_user.id
    conn = get_db_connection()
    cart = conn.execute('SELECT * FROM cart where user_id = ?',
                                 (user_id,)).fetchall()
    str_cart = ""
    products = []
    for each in cart:
        str_cart += str(each['user_id']) + str(each['product_id'])
        products.append(get_product(each['product_id']))
    conn.close()
    return render_template('cart.html', name=current_user.name, products=products)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/shipping')
def shipping():
    return render_template('shipping.html')

@main.route('/faq')
def faq():
    return render_template('faq.html')

@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/addorder', methods=["POST"])
@login_required
def add_order():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM cart where user_id = ?",
                                 (current_user.id,)).fetchall()
    cost = 0.0
    for each in products:
        p_id = each['product_id']
        product_c = conn.execute('SELECT * FROM products WHERE id = ?',
                               (p_id,)).fetchone()
        cost += product_c['cost']

    conn.execute("INSERT INTO orders (ready, shipped, cost, priority) VALUES (?, ?, ?, ?)",
                (0, 0, cost, 1)
                )
    conn.commit()
    conn.close()
    conn = get_db_connection()
    order_id = conn.execute("SELECT * from orders WHERE id = (SELECT MAX(id) FROM orders)").fetchone()
    order_id = order_id['id']
    for each in products:
        conn.execute("INSERT INTO product_order (product_id, order_id) VALUES (?, ?)",
                     (each['product_id'], order_id)
                     )
    conn.execute("INSERT INTO user_order (user_id, order_id) VALUES (?, ?)",
                 (current_user.id, order_id)
                 )
    conn.commit()
    orders = conn.execute("SELECT * FROM orders where id = ?",
                                 (order_id,)).fetchall()
    conn.close()
    orders_new = []
    for o in orders:
        if o['ready'] == 1:
            ready = 'YES'
        else:
            ready = 'NO'
        if o['shipped'] == 1:
            shipped = 'YES'
        else:
            shipped = 'NO'
        order = {
            'id': o['id'],
            'ready': ready,
            'shipped': shipped,
            'cost': o['cost'],
            'priority': o['priority']
        }
        orders_new.append(order)
    return render_template('myorders.html', orders=orders_new, title_="New Order")

@main.route('/my_orders')
@login_required
def my_orders():
    conn = get_db_connection()
    orders_ids = conn.execute("SELECT * FROM user_order where user_id = ?",
                          (current_user.id,)).fetchall()
    orders = []
    for each in orders_ids:
        orders.append(
            conn.execute("SELECT * from orders WHERE id = ?",
                         (each['order_id'],)).fetchone())
    conn.close()
    orders_new = []
    for o in orders:
        if o['ready'] == 1:
            ready = 'YES'
        else:
            ready = 'NO'
        if o['shipped'] == 1:
            shipped = 'YES'
        else:
            shipped = 'NO'
        order = {
            'id': o['id'],
            'ready': ready,
            'shipped': shipped,
            'cost': o['cost'],
            'priority': o['priority']
        }
        orders_new.append(order)
    return render_template('myorders.html', orders=orders_new, title_="My Orders")

@main.route('/add_product', methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        cost = float(request.form.get('cost'))
        description = request.form.get('description')
        image = request.form.get('image')
        category = request.form.get('category')
        conn = get_db_connection()
        conn.execute("INSERT INTO products (name, cost, image, description, category) VALUES (?, ?, ?, ?, ?)",
                    (name, cost, image, description, category)
                    )
        conn.commit()
        conn.close()
        return redirect(url_for('main.index'))
    return render_template('add_product.html', form=form, title="Add Product")


@main.route('/filter_orders')
@login_required
def filter_orders():
    if current_user.is_authenticated:
        if not current_user.admin:
            return render_template('404.html')
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders where shipped = 0 OR ready = 0').fetchall()
    conn.close()
    orders_new = []
    for o in orders:
        if o['ready'] == 1:
            ready = 'YES'
        else:
            ready = 'NO'
        if o['shipped'] == 1:
            shipped = 'YES'
        else:
            shipped = 'NO'
        order = {
            'id': o['id'],
            'ready': ready,
            'shipped': shipped,
            'cost': o['cost'],
            'priority': o['priority']
        }
        orders_new.append(order)
    return render_template('orders.html', orders=orders_new)