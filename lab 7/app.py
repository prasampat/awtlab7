from flask import Flask, request, render_template
import sqlite3

wrong = 0
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def start():

    global wrong
    conn = sqlite3.connect('names.db')
    crsr = conn.cursor()
    crsr.execute(
        'create table if not exists names (name varchar(150), pas varchar(150))')
    conn.commit()

    if(request.method == 'POST'):

        name = request.form['username']
        pas = request.form['password']

        alp_u, alp_l, num = any(el.isupper() for el in pas), any(el.islower()
                                                              for el in pas), any(el.isnumeric() for el in pas)

        alp_uu, alp_lu, num_uu = any(el.isupper() for el in name), any(
            el.islower() for el in name), any(el.isnumeric() for el in name)

        if((alp_u and alp_l and num) and \
            (alp_uu and alp_lu and num_uu)):

            wrong = 0

            crsr.execute('insert into names(name, pas) values(?,?)', [
                str(name), str(pas)])

            conn.commit()

            return render_template('report.html', content=[alp_u, alp_l, num, alp_uu, alp_lu, num_uu])

        else:
            wrong += 1

            if(wrong == 3):

                wrong = 0

                return render_template('index.html', content='3 times wrong')
            else:
                return render_template('report.html', content=[alp_u, alp_l, num, alp_uu, alp_lu, num_uu])

    return render_template('index.html')


app.run(host='localhost', port=5000, debug=True)
