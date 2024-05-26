import psycopg2

from PgSQL.connect import get_connection, release_connection
from flask import Flask, request, jsonify
from flask_mail import Mail