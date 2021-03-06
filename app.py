from flask import Flask, url_for, render_template, redirect, request, flash
from forms import OrderForm
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

_SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = _SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/order.db'
db = SQLAlchemy(app)


class CMaggi(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    count = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Integer, nullable=False)

    def __init__(self, id, count, done=0):
        self.id = id
        self.count = count
        self.done = done


class PMaggi(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    count = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Integer, nullable=False)

    def __init__(self, id, count, done=0):
        self.id = id
        self.count = count
        self.done = done


class MDosa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    count = db.Column(db.Integer, nullable=False)
    done = db.Column(db.Integer, nullable=False)

    def __init__(self, id, count, done=0):
        self.id = id
        self.count = count
        self.done = done


db.create_all()
db.session.commit()

_INDEX = len(MDosa.query.all()) + 1

cmag_queue = []
pmag_queue = []
mdos_queue = []


@app.route('/', methods=('GET', 'POST'))
def contact():
    global _INDEX
    form = OrderForm(request.form)
    if request.method == 'POST':

        cmag = form.cheeseMaggie.data
        pmag = form.plainMaggie.data
        mdos = form.masalaDosa.data

        if cmag is None:
            cmag = 0
        if pmag is None:
            pmag = 0
        if mdos is None:
            mdos = 0

        _INDEX += 1
        os.environ['_INDEX'] = str(_INDEX)
        cmaggi = CMaggi(_INDEX, cmag)
        pmaggi = PMaggi(_INDEX, pmag)
        mdosa = MDosa(_INDEX, mdos)

        for i in range(cmag):
            cmag_queue.append(_INDEX)
        for i in range(pmag):
            pmag_queue.append(_INDEX)
        for i in range(mdos):
            mdos_queue.append(_INDEX)

        db.session.add(cmaggi)
        db.session.add(pmaggi)
        db.session.add(mdosa)
        db.session.commit()
        return redirect(url_for('order', id=_INDEX))
    else:
        return render_template('contact.html', form=form)


@app.route('/rcmag')
def remove_cmaggie():
    if len(cmag_queue) is not 0:
        top = cmag_queue.pop()
        curr = CMaggi.query.filter(CMaggi.id == top).first()
        curr.count -= 1
        curr.done += 1
        db.session.commit()
    return redirect(url_for('contact'))


@app.route('/rpmag')
def remove_pmaggie():
    if len(pmag_queue) is not 0:
        top = pmag_queue.pop()
        curr = PMaggi.query.filter(PMaggi.id == top).first()
        curr.count -= 1
        curr.done += 1
        db.session.commit()
    return redirect(url_for('contact'))


@app.route('/rmdos')
def remove_mdosa():
    if len(mdos_queue) is not 0:
        top = mdos_queue.pop()
        curr = MDosa.query.filter(MDosa.id == top).first()
        curr.count -= 1
        curr.done += 1
        db.session.commit()
    return redirect(url_for('contact'))


@app.route('/<id>')
def order(id):
    cmaggi = CMaggi.query.filter(CMaggi.id == id).first()
    pmaggi = PMaggi.query.filter(PMaggi.id == id).first()
    mdosa = MDosa.query.filter(CMaggi.id == id).first()

    done_cmag = cmaggi.done
    done_pcmag = pmaggi.done
    done_mdos = mdosa.done

    if cmaggi is None:
        cmaggi = 0
    else:
        cmaggi = cmaggi.count

    if pmaggi is None:
        pmaggi = 0
    else:
        pmaggi = pmaggi.count

    if mdosa is None:
        mdosa = 0
    else:
        mdosa = mdosa.count

    return render_template('list.html', id=id, cleft=cmaggi, pleft=pmaggi, mleft=mdosa, cdone=done_cmag, pdone=done_pcmag, mdone=done_mdos)


if __name__ == '__main__':
    app.run(debug=True)
