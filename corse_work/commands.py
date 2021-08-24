from app import app
from datetime import datetime
from web_app.models import Price, db
from web_app.orders.orders import rows

# def make_test_data():
#     with open("./dataJSON.json", "r", encoding='utf-8-sig') as read_file:
#         data = json.load(read_file)
#     for tbl in db.metadata.sorted_tables:
# #    for tb in data:
#         tb = tbl.name
#         print(tb)
#         qt = QueryTable(tb)
#         pk = qt.primary_key['constrained_columns']
#         for rec in data[tb]:
#             if len(pk) > 0:
#                 st = {col: rec[col] for col in pk}
#             else:
#                 st = rec
#             if qt.query(st) is None:
#                 qt.add(rec)
#     try:
#         db.session.commit()
#     except IntegrityError:
#         db.session.rollback()
#         raise InternalServerError("failed to write data to the database")


if __name__ == '__main__':
    # with app.app_context():
    #     #        make_test_data()
    #     dt = datetime.now()
    #     product_id = 2
    #     pt_id = 1
    #     prices = db.session.query(Price).filter(Price.pt_id == pt_id, Price.product_id == product_id,
    #                                             Price.date <= dt).order_by(Price.date.desc()).all()
    #     price = db.session.query(Price).filter(Price.pt_id == pt_id, Price.product_id == product_id,
    #                                             Price.date <= dt).order_by(Price.date.desc()).first()
    #     print(price.id, price.date, price.product.product_name, price.price)
    #     print('======================')
    #     for price in prices:
    #         print(price.id, price.date, price.product.product_name, price.price)
    #     print(type(rows))
    pass
