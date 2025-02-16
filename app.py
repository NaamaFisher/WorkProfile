from flask import Flask, request, Response, jsonify, render_template
from person import Person
from dbcontext import db_add

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["PUT"])
def add():
    body = request.json
    if body is not None:
        app.logger.info("Request to add person with body: %s", body)
        person = Person(0, body["firstName"], body["lastName"], body["age"], body["address"], body["workplace"])
        return db_add(person)
    app.logger.error("Request body is empty")
    return Response(status=404)

@app.route("/health")
def health():
    health_messages = []
    # Simple application health check
    try:
        app.logger.info("Application is running")
        health_messages.append("Application: Healthy")
    except Exception as e:
        app.logger.error(f"Application health check failed: {e}")
        health_messages.append("Application: Not Healthy")

    combined_health_status = "\n".join(health_messages)
    return combined_health_status

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

