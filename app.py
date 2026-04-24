from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

# Product data with images
products = [
    {"id": 1, "name": "Urea Fertilizer", "price": 300,
     "image": "https://via.placeholder.com/150?text=Urea"},
    {"id": 2, "name": "DAP Fertilizer", "price": 1200,
     "image": "https://via.placeholder.com/150?text=DAP"},
    {"id": 3, "name": "Potash Fertilizer", "price": 800,
     "image": "https://via.placeholder.com/150?text=Potash"},
    {"id": 4, "name": "NPK Fertilizer", "price": 950,
     "image": "https://via.placeholder.com/150?text=NPK"},
    {"id": 5, "name": "Organic Compost", "price": 500,
     "image": "https://via.placeholder.com/150?text=Compost"},
    {"id": 6, "name": "Vermicompost", "price": 600,
     "image": "https://via.placeholder.com/150?text=Vermi"},
]

cart = []

@app.route("/")
def home():
    html = """
    <h1>🌱 Fertilizer Store</h1>
    <a href="/cart">🛒 View Cart</a>
    <hr>
    <div style="display:flex; flex-wrap:wrap;">
    {% for p in products %}
        <div style="border:1px solid #ccc; padding:10px; margin:10px; width:200px;">
            <img src="{{p.image}}" width="150" height="150"><br>
            <h4>{{p.name}}</h4>
            <p>Price: ₹{{p.price}}</p>
            <a href="/add/{{p.id}}">Add to Cart</a>
        </div>
    {% endfor %}
    </div>
    """
    return render_template_string(html, products=products)

@app.route("/add/<int:id>")
def add_to_cart(id):
    for p in products:
        if p["id"] == id:
            cart.append(p)
    return redirect(url_for('home'))

@app.route("/cart")
def view_cart():
    total = sum(item["price"] for item in cart)
    html = """
    <h1>🛒 Your Cart</h1>
    {% for item in cart %}
        <p>{{item.name}} - ₹{{item.price}}</p>
    {% endfor %}
    <h3>Total: ₹{{total}}</h3>
    <a href="/">⬅ Back to Home</a>
    """
    return render_template_string(html, cart=cart, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
