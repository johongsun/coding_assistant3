from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Excel 파일을 DataFrame으로 읽기
try:
    df = pd.read_excel('stock.xls')
except FileNotFoundError:
    df = pd.DataFrame({'종목코드': [], '회사명': [], '현재가': [], '거래량': [], '예측': []})

# DataFrame을 Excel 파일로 저장
def save_df():
    df.to_excel('stock.xls', index=False)

@app.route('/')
def index():
    stocks = df.to_dict(orient='records')
    return render_template('index.html', stocks=stocks)

@app.route('/add', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        global df
        new_stock = {
            '종목코드': request.form['종목코드'],
            '회사명': request.form['회사명'],
            '현재가': request.form['현재가'],
            '거래량': request.form['거래량'],
            '예측': request.form['예측']
        }
        new_df = pd.DataFrame([new_stock])
        df = pd.concat([df, new_df], ignore_index=True)
        save_df()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_stock(index):
    if request.method == 'POST':
        global df
        df.loc[index, '종목코드'] = request.form['종목코드']
        df.loc[index, '회사명'] = request.form['회사명']
        df.loc[index, '현재가'] = request.form['현재가']
        df.loc[index, '거래량'] = request.form['거래량']
        df.loc[index, '예측'] = request.form['예측']
        save_df()
        return redirect(url_for('index'))
    
    stock = df.loc[index].to_dict()
    return render_template('edit.html', stock=stock, index=index)

@app.route('/delete/<int:index>')
def delete_stock(index):
    global df
    df = df.drop(index).reset_index(drop=True)
    save_df()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
