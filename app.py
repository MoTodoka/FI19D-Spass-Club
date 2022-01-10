import flask
from flask import Flask, render_template, request
from sqlite3 import IntegrityError
from werkzeug.exceptions import MethodNotAllowed, HTTPException, Conflict

from python.services.database_connection_service import Connection

from python.data.generic_data import DataService, Data

from python.data.activity import ActivityService
from python.data.event import EventService
from python.data.location import LocationService
from python.data.match import MatchService
from python.data.player import PlayerService
from python.data.score import ScoreService

app = Flask(__name__)


def get_service_by_table_name(key) -> DataService:
    """Gibt für einen key (str) die Instanz eines DataService zurück."""
    switcher = {
        "activity": ActivityService(),
        "event": EventService(),
        "location": LocationService(),
        "match": MatchService(),
        "player": PlayerService(),
        "score": ScoreService()
    }
    return switcher.get(key)


@app.before_first_request
def before_first_request():
    reset_test_data()


@app.route("/")
def index_view():
    """
    Leitet beim Aufrufen der Route "/" auf das Dashboard um.
    """
    return flask.redirect("/dashboard")


@app.route("/dashboard")
def dashboard_view():
    """
    Zeigt Dashboard an.\n
    """

    return render_template("dashboard.html",
                           match_service=MatchService(),
                           score_service=ScoreService(),
                           player_service=PlayerService(),
                           event_service=EventService())


@app.route("/list/<element_type>")
def list_view(element_type: str):
    """
    Zeigt eine Liste von Elementen in tabellarischer Form an.\n
    Der Elementtyp wird über die URL gewählt.
    """

    service: DataService = get_service_by_table_name(element_type)
    element_list: [Data] = service.get_all()

    return render_template("list.html",
                           service=service,
                           element_type=element_type,
                           title=element_list[0].get_title(),
                           dict_list=[element.__dict__ for element in element_list])


@app.route("/element/<element_type>/<uid>", methods=['GET', 'POST', 'DELETE'])
def element_view(element_type, uid):
    """
    Element anzeigen ("GET"), erstellen/ändern oder löschen ("POST")\n
    Elementtyp und Element werden über die URL gewählt.
    """

    service: DataService = get_service_by_table_name(element_type)
    if request.method == 'GET':
        # Element anzeigen.\n
        # Neues Element: UID == 0
        if uid == "0":
            element = service.get_new()
        else:
            element = service.get_by_uid(uid)
        return render_template("element.html",
                               element_type=element_type,
                               title=element.get_title(),
                               element=element.__dict__)

    if request.method == 'POST':
        try:
            if request.form.get("edit"):
                # Element erstellen/bearbeiten
                data: Data = service.converter().get_data_from_dictionary(request.form)
                if uid == "0":
                    # Element erstellen
                    service.insert(data)
                else:
                    # Element bearbeiten
                    service.update(data)
                return flask.redirect("/list/{0}".format(element_type))

            elif request.form.get("delete"):
                # Element löschen
                if uid == "0":
                    raise MethodNotAllowed()
                else:
                    service.delete(uid)
                return flask.redirect("/list/{0}".format(element_type))

            else:
                raise MethodNotAllowed()
        except IntegrityError:
            raise Conflict()
    else:
        # POST Error 405 Method Not Allowed
        raise MethodNotAllowed()


@app.route("/reset_test_data")
def reset_test_data():
    """
    Tabellen neu erzeugen und Testdaten laden.
    """
    print("Datenbank/Testdaten neu erzeugen.")
    con = Connection()
    con.reset_database()
    con.load_test_data()
    return flask.redirect("/")


@app.errorhandler(HTTPException)
def error(e):
    """
    Errorhandler. Fängt alle geworfenen HTTPExceptions und zeigt Informationen an.
    """
    return render_template("error.html", error=e), e.code


if __name__ == '__main__':
    # WebApp starten.
    app.run()
