"""
Account Service

This microservice handles the lifecycle of Accounts
"""
from flask import jsonify, request, make_response, abort, url_for
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Flask app


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# Root Index
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return jsonify(
        name="Account REST API Service",
        version="1.0"
    ), status.HTTP_200_OK


######################################################################
# CREATE ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_account():
    """Creates a new Account"""
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for("read_account", account_id=account.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})


######################################################################
# LIST ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """Lists all Accounts"""
    accounts = [account.serialize() for account in Account.all()]
    return make_response(jsonify(accounts), status.HTTP_200_OK)


######################################################################
# READ ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Reads an Account by id"""
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id {account_id} not found")
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)


######################################################################
# UPDATE ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Updates an Account by id"""
    check_content_type("application/json")
    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id {account_id} not found")
    account.deserialize(request.get_json())
    account.update()
    return make_response(jsonify(account.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Deletes an Account by id"""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# UTILITY FUNCTION
######################################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type != media_type:
        app.logger.error("Invalid Content-Type: %s", content_type)
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {media_type}")
