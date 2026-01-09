from flask import Flask, render_template, request, redirect
from supabase import create_client

app = Flask(__name__)

# 🔑 SUPABASE CONFIG
SUPABASE_URL = "https://rklkyvbfnurytzetfkfr.supabase.co"
SUPABASE_KEY = "sb_secret_3Pat1CorkTamoV5hgxewXA_2GRv-_Qa"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
if supabase:
    print("ok")


# BMI category logic
def get_bmi_category(bmi):
    if bmi < 18.5:
        return 1, "Underweight"
    elif bmi < 25:
        return 2, "Normal"
    elif bmi < 30:
        return 3, "Overweight"
    else:
        return 4, "Obese"




@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("login.html")

    # POST data
    name = request.form["name"]
    email = request.form["email"]
    age = int(request.form["age"])
    gender = request.form["gender"]

    try:
        supabase.table("users").insert({
            "name": name,
            "email": email,
            "age": age,
            "gender": gender
        }).execute()

        return redirect("/bmi")

    except Exception as e:
        return f"Error: {e}"


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/bmi", methods=["GET", "POST"])
def calculate_bmi():
    if request.method == "GET":
        return render_template("value.html")

    height = float(request.form["height"])
    weight = float(request.form["weight"])

    bmi = round(weight / ((height / 100) ** 2), 2)
    category_id, category_name = get_bmi_category(bmi)

    response = supabase.table("food_menu") \
        .select("*") \
        .eq("category_id", category_id) \
        .execute()

    menu_items = response.data

    return render_template(
        "result.html",
        bmi=bmi,
        category=category_name,
        menu=menu_items
    )


if __name__ == "__main__":
    app.run(debug=True)
