from werkzeug.exceptions import InternalServerError
from sqlalchemy.exc import IntegrityError
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for)
from sqlalchemy import (
    inspect)
from sqlalchemy.sql import sqltypes
import json
from ..models import (
    db
)
from ..functions import (
    QueryTable,
    delete_data,
    make_test_data
)

from web_app.forms.admin_forms import *

DATA = 'Data'
METADATA = 'Metadata'

admin_app = Blueprint("admin_app", __name__, url_prefix="/admin")

param = {'tables': db.metadata.tables.keys(),
         'cur_table': '_',
         'navtabs': [DATA, METADATA],
         'cur_navtab': 'Data',
         'data': False,
         'fields': []}


def get_data(qt):
    return db.session.query(qt.table).all()


def get_metadata(qt):
    dct = {}
    if len(qt.columns) > 0:
        dct['columns'] = qt.table_col
    if len(qt.foreign_keys) > 0:
        dct['foreign_keys'] = qt.foreign_keys
    if len(qt.indexes):
        dct['indexes'] = qt.indexes
    dct['primary_key'] = [qt.primary_key]
    return dct


functions = {DATA: get_data, METADATA: get_metadata}


def columns(table):
    eng = db.get_engine()
    insp = inspect(eng)
    columns = insp.get_columns(table)
    for col in columns:
        if isinstance(col['type'], sqltypes.INTEGER) or isinstance(col['type'], sqltypes.NUMERIC):
            col['type_field'] = 'number'
        elif isinstance(col['type'], sqltypes.DATETIME) or isinstance(col['type'], sqltypes.TIMESTAMP):
            col['type_field'] = 'datetime'
        else:
            col['type_field'] = 'text'
    return columns


@admin_app.route("/", endpoint='index')
def list_tables():
    return render_template("admin/index.html", param=param)


@admin_app.route("/delete_all", endpoint='delete_all')
def delete_all():
    delete_data()
    return redirect(url_for('admin_app.index'))


@admin_app.route("/load_trial", endpoint='load_trial')
def load_data():
    make_test_data()
    return redirect(url_for('admin_app.index'))


@admin_app.route("/<navtab>/<table>", endpoint='table')
def sel_table(table, navtab):
    qt = QueryTable(table)
    param['cur_table'] = table
    param['cur_navtab'] = navtab
    keys = db.metadata.tables.keys()
    if table in keys:
        primary_key = qt.primary_key['constrained_columns']
        param['fields'] = [{'name': col, 'pk': col in primary_key} for col in qt.columns]
        param['data'] = functions[navtab](qt)
        param['exist_pk'] = (len(primary_key) > 0)
    templname = 'admin/' + navtab.lower() + '.html'
    return render_template(templname, param=param)


@admin_app.route("/Data/<table>/<key_fields>/", endpoint="details")
def get_details(table, key_fields):
    templname = 'admin/details.html'
    kf = json.loads(key_fields.replace('{{', '{').replace('}}', '}'))
    qr = QueryTable(table)
    param['fields'] = qr.fields(kf)

    return render_template(templname, param=param)


@admin_app.route("/Data/<table>/<key_fields>/delete", endpoint="delete")
def delete_record(table, key_fields):
    kf = json.loads(key_fields.replace('{{', '{').replace('}}', '}'))
    qt = QueryTable(table)
    qt.delete(kf)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError("could not delete data from the database")
    return redirect(url_for('admin_app.table', table=table, navtab='Data'))
    pass


@admin_app.route("/Data/<table>/add", methods=['GET', 'POST'])
def add(table):
    qr = QueryTable(table)
    form = AddDefault(qr.table_col)
    template = 'admin/' + qr.model.add_templ + '.html'
    if request.method == 'GET':
        return render_template(template, form=form, param=param)

    if form.validate_on_submit():
        qr.add(form)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise InternalServerError("failed to write data to the database")

    return redirect(url_for('admin_app.table', table=table, navtab='Data'))

    pass
