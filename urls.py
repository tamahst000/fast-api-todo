from controllers import *

app.add_api_route("/", index)
app.add_api_route("/admin", admin, methods=["GET", "POST"])
app.add_api_route("/register", register, methods=["GET", "POST"])
app.add_api_route("/todo/{username}/{year}/{month}/{day}", detail)
app.add_api_route("/done", done, methods=["POST"])
app.add_api_route("/add", add, methods=["POST"])
app.add_api_route("/delete/{t_id}", delete)

app.add_api_route("/get", get)
app.add_api_route("/add_task", insert, methods=["POST"])
