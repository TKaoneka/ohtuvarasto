from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)


def safe_float(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class VarastoStore:
    def __init__(self):
        self.varastot = {}
        self.next_id = 1

    def add(self, varasto, nimi):
        varasto_id = self.next_id
        self.varastot[varasto_id] = {'varasto': varasto, 'nimi': nimi}
        self.next_id += 1
        return varasto_id

    def get(self, varasto_id):
        return self.varastot.get(varasto_id)

    def delete(self, varasto_id):
        if varasto_id in self.varastot:
            del self.varastot[varasto_id]

    def all_items(self):
        return self.varastot


store = VarastoStore()


@app.route('/')
def index():
    return render_template('index.html', varastot=store.all_items())


@app.route('/create', methods=['GET', 'POST'])
def create_varasto():
    if request.method == 'POST':
        tilavuus = safe_float(request.form.get('tilavuus'), 0)
        alku_saldo = safe_float(request.form.get('alku_saldo'), 0)
        nimi = request.form.get('nimi', f'Varasto {store.next_id}')

        varasto = Varasto(tilavuus, alku_saldo)
        store.add(varasto, nimi)
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/varasto/<int:varasto_id>')
def view_varasto(varasto_id):
    data = store.get(varasto_id)
    if data is None:
        return redirect(url_for('index'))
    return render_template(
        'view.html',
        varasto_id=varasto_id,
        varasto=data['varasto'],
        nimi=data['nimi']
    )


@app.route('/varasto/<int:varasto_id>/add', methods=['POST'])
def add_to_varasto(varasto_id):
    data = store.get(varasto_id)
    if data:
        maara = safe_float(request.form.get('maara'), 0)
        data['varasto'].lisaa_varastoon(maara)
    return redirect(url_for('view_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/remove', methods=['POST'])
def remove_from_varasto(varasto_id):
    data = store.get(varasto_id)
    if data:
        maara = safe_float(request.form.get('maara'), 0)
        data['varasto'].ota_varastosta(maara)
    return redirect(url_for('view_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/delete', methods=['POST'])
def delete_varasto(varasto_id):
    store.delete(varasto_id)
    return redirect(url_for('index'))


@app.route('/varasto/<int:varasto_id>/edit', methods=['GET', 'POST'])
def edit_varasto(varasto_id):
    data = store.get(varasto_id)
    if data is None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        nimi = request.form.get('nimi', data['nimi'])
        data['nimi'] = nimi
        return redirect(url_for('view_varasto', varasto_id=varasto_id))
    return render_template(
        'edit.html',
        varasto_id=varasto_id,
        varasto=data['varasto'],
        nimi=data['nimi']
    )


if __name__ == '__main__':
    app.run(debug=True)
