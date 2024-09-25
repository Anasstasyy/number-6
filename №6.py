import sqlalchemy
from sqlalchemy import ForeignKey, Column, String, Integer, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id_publisher = Column('id_publisher', Integer, primary_key = True)
    name = Column('name', String(length=40))

    def __init__(self, id_publisher, name):
        self.id_publisher = id_publisher
        self.name = name

    def __repr__(self):
        return f'({self.id_publisher}) {self.name}'

class Book(Base):
    __tablename__ = 'book'
    id_book = Column('id_book', Integer, primary_key=True)
    title = Column('title', String(length=40))
    id_publisher = Column('id_publisher', Integer, ForeignKey('publisher.id_publisher'))

    def __init__(self, id_book, title, id_publisher):
        self.id_book = id_book
        self.title = title
        self.id_publisher = id_publisher

    def __repr__(self):
        return f'{self.title}'

class Shop(Base):
    __tablename__ = 'shop'
    id_shop = Column('id_shop', Integer, primary_key=True)
    name = Column('name', String(length=40))

    def __init__(self, id_shop, name):
        self.id_shop = id_shop
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class Stock(Base):
    __tablename__ = 'stock'
    id_stock = Column('id_stock', Integer, primary_key=True)
    id_book = Column('id_book', Integer, ForeignKey('book.id_book'))
    id_shop = Column('id_shop', Integer, ForeignKey('shop.id_shop'))
    count = Column('count', Integer)

    def __init__(self, id_stock, id_book, id_shop, count):
        self.id_stock = id_stock
        self.id_book = id_book
        self.id_shop= id_shop
        self.count = count

class Sale(Base):
    __tablename__ = 'sale'
    id_price = Column('id_price', Integer, primary_key=True)
    price = Column('price', Integer)
    date_sale = Column('date_sale', Date)
    id_stock = Column('id_stock', Integer, ForeignKey('stock.id_stock'))
    count =Column('count', Integer)

    def __init__(self, id_price, price, date_sale, id_stock, count):
        self.id_price = id_price
        self.price =price
        self.date_sale = date_sale
        self.id_stock = id_stock
        self.count = count

    def __repr__(self):
        return f'{self.price} | {self.date_sale}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = "postgresql://postgres:postgres@localhost:5432/book"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind = engine)
session = Session()


publ_1 = Publisher(1, 'Пушкин')
publ_2 = Publisher(2, 'Достоевский')
publ_3 = Publisher(3, 'Лермонтов')

session.add_all([publ_1, publ_2, publ_3])
session.commit()

book_1 = Book(1, 'Капитанская дочка', 1)
book_2 = Book(2, 'Евгений Онегин', 1)
book_3 = Book(3, 'Преступление и наказание', 2)
book_4 = Book(4, 'Бородино', 3)

session.add_all([book_1, book_2, book_3, book_4])
session.commit()

shop_1 = Shop(1, 'Буквоед')
shop_2 = Shop(2, 'Читай город')

session.add_all([shop_1, shop_2])
session.commit()

stock_1 = Stock(1, 1 ,1 ,1)
stock_2 = Stock(2, 2 ,1 ,1)
stock_3 = Stock(3, 3 ,1 ,1)
stock_4 = Stock(4, 4 ,2 ,1)

session.add_all([stock_1, stock_2, stock_3, stock_4])
session.commit()

sale_1 = Sale(1, 399, '09.11.2022', 1, 1)
sale_2 = Sale(2, 259, '08.11.1022', 2, 1)
sale_3 = Sale(3, 379, '05.11.2022', 3, 1)
sale_4 = Sale(4, 299, '02.11.2022', 4, 1)

session.add_all([sale_1, sale_2, sale_3, sale_4])
session.commit()

def get_shops(search = input('введите id или имя')):
    search = search
    if search.isnumeric():
        result = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Publisher, Publisher.id_publisher == Book.id_publisher) \
        .join(Stock, Stock.id_book == Book.id_book) \
            .join(Shop, Shop.id_shop == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id_stock) \
            .filter(search == Publisher.id_publisher).all()
        for book, shop, price, date in result:
            print(f'{book: <40} | {shop: <10} | {price: <8} | {date}')
    else:
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(search == Publisher.name).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <8} | {date}')


session.close()