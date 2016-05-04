from app import db
from . import lm
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

@lm.user_loader
def load_user(sotrudnik_id):
    return Sotrudnik.query.get(int(sotrudnik_id))

class Sotrudnik(db.Model):
    __tablename__ = 'sotrudniki'
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(120), index=True, unique=True)
    Dolznost = db.Column(db.String(64), index=True, unique=True)
    Vozrast = db.Column(db.Integer, index=True)
    Telefon = db.Column(db.String(20), index=True)
    Otdel = db.Column(db.String(40), index=True,)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    rol_id = db.Column(db.Integer, db.ForeignKey('roly.id'))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        #try:
            #return unicode(self.id)  # python 2
        #except NameError:
        return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/{}?d=mm&s={}'.\
            format(md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<Sotrudnik {}>'.format(self.FIO)


class Rol (db.Model):  #!!!!!!!!!!!!!!!
    __tablename__ = 'roly'
    id = db.Column(db.Integer, primary_key=True)
    Imya = db.Column(db.String(64), unique=True)
    access_level = db.Column(db.Integer)
    sotrudniki = db.relationship('Sotrudnik', backref = 'rol')


class Klient(db.Model):
    __tablename__ = 'klienty'
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(120), index=True, unique=True)
    Vozrast = db.Column(db.Integer, index=True)
    Adres = db.Column(db.String(64), index=True, unique=True)
    Email = db.Column(db.String(120), index=True, unique=True)
    Telefon = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Klient {}>'.format(self.FIO)


class Zayavka(db.Model):
    __tablename__ = 'zayavki'
    id = db.Column(db.Integer, primary_key=True)
    FIO_sotr = db.Column(db.String(120), index=True, unique=True)
    FIO_kl = db.Column(db.String(120), index=True, unique=True)
    Nazv_izd = db.Column(db.String(60), index=True)
    Data = db.Column(db.Date, index=True)
    Avans = db.Column(db.Numeric(precision=8.3), index=True)
    klient_id = db.Column(db.Integer, db.ForeignKey('klienty.id'))
    sotrudnik_id = db.Column(db.Integer, db.ForeignKey('sotrudniki.id'))
    izdelie_id = db.Column(db.Integer, db.ForeignKey('izdeliya.id'))

sostav_m = db.Table('sostav_m',
                db.Column('izdelie_id', db.Integer, db.ForeignKey('izdeliya.id')),
                db.Column('aterial_id', db.Integer, db.ForeignKey('materialy.id'))
                    )

sostav_z = db.Table('sostav_z',
                  db.Column('izdelie_id', db.Integer, db.ForeignKey('izdeliya.id')),
                  db.Column('polufabricat_id', db.Integer, db.ForeignKey('zagotovki.id')),
                  )


class Izdelie(db.Model):
    __tablename__ = 'izdeliya'
    id = db.Column(db.Integer, primary_key=True)
    Imya_iz = db.Column(db.String(60), index=True)
    Kol_vo = db.Column(db.Integer, index=True)
    Razmer_kubm = db.Column(db.Integer, index=True)
    Cena_iz = db.Column(db.Numeric(precision=8.3), index=True)
    Chertez = db.Column(db.String(255))
    Eskiz = db.Column(db.String(255))
    Sert = db.Column(db.String(255))
    rabota_id = db.Column(db.Integer, db.ForeignKey('raboty.id'))
    Imya_z = db.relationship('zagotovka',
                             secondary=sostav_z,
                             backref=db.backref('Imya_iz', lazy='dynamic'),
                             lazy='dynamic')
    Imya_m = db.relationship('material',
                             secondary=sostav_m,
                             backref=db.backref('Imya_iz', lazy='dynamic'),
                             lazy='dynamic')

    def __repr__(self):
        return '<Izdelie {}>'.format(self.Imya_iz)


class Zagotovka(db.Model):
    __tablename__ = 'zagotovki'
    id = db.Column(db.Integer, primary_key=True)
    Imya_z = db.Column(db.String(60), index=True)
    Tip_proiz = db.Column(db.String(60), index=True)
    Kol_vo = db.Column(db.Integer, index=True)
    Dlina = db.Column(db.Integer, index=True)
    Shirina = db.Column(db.Integer, index=True)
    Vysota = db.Column(db.Integer, index=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materialy.id'))
    rabota_id = db.Column(db.Integer, db.ForeignKey('raboty.id'))

    def __repr__(self):
        return '<Polufabricat {}>'.format(self.Imya_p)


class Material(db.Model):
    __tablename__ = 'materialy'
    id = db.Column(db.Integer, primary_key=True)
    Imya_m = db.Column(db.String(60), index=True)
    Kol_vo = db.Column(db.Integer, index=True)
    Cena_m = db.Column(db.Numeric(precision=8.3), index=True)
    postavka_id = db.Column(db.Integer, db.ForeignKey('postavki.id'))

    def __repr__(self):
        return '<Material {}>'.format(self.Imya_m)


class Rabota(db.Model):
    __tablename__ = 'raboty'
    id = db.Column(db.Integer, primary_key=True)
    Imya_r = db.Column(db.String(60), index=True)
    Koeff = db.Column(db.Integer, index=True)
    Proiz = db.Column(db.Integer, index=True)
    Cena_r = db.Column(db.Numeric(precision=8.3), index=True)
    Ed_izm = db.Column(db.Numeric(precision=8.3), index=True)
    Izdelie = db.relationship('Izdelie', backref='rabota', lazy='dynamic')
    Zagotovka = db.relationship('Zagotovka', backref='rabota', lazy='dynamic')

class Postavschik(db.Model):
     __tablename__ = 'postavschiki'
     id = db.Column(db.Integer, primary_key=True)
     Imya = db.Column(db.String(60), index=True)
     Telefon = db.Column(db.String(20), index=True)
     Postavka = db.relationship('Postavka', backref='postavschik', lazy='dynamic')

     def __repr__(self):
        return '<Postavschik {}>'.format(self.Imya)

class Postavka(db.Model):
    __tablename__ = 'postavki'
    id = db.Column(db.Integer, primary_key=True)
    Postavschik = db.Column(db.String(60), index=True)
    Material = db.Column(db.String(60), index=True)
    Cena_dost = db.Column(db.Numeric(precision=8.3), index=True)
    Data = db.Column(db.Date, index=True)
    Kol_vo = db.Column(db.Integer, index=True)
    postavschik_id = db.Column(db.Integer, db.ForeignKey('postavschiki.id'))