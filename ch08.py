from flask import Flask, jsonify, request
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

@app.route('/stocks', methods=['GET'])
def get_stocks():
    return jsonify(df.to_dict(orient='records'))

@app.route('/stock/<int:stock_id>', methods=['GET'])
def get_stock(stock_id):
    stock = df[df['종목코드'] == stock_id]
    if stock.empty:
        return jsonify({'error': 'Stock not found'}), 404
    return jsonify(stock.to_dict(orient='records')[0])

@app.route('/stock', methods=['POST'])
def create_stock():
    global df
    new_stock = request.get_json()
    if not all(key in new_stock for key in ['종목코드', '회사명', '현재가', '거래량', '예측']):
        return jsonify({'error': 'Missing data'}), 400
    
    new_df = pd.DataFrame([new_stock])
    df = pd.concat([df, new_df], ignore_index=True)
    save_df()
    return jsonify(new_stock), 201

@app.route('/stock/<int:stock_id>', methods=['PUT'])
def update_stock(stock_id):
    global df
    if df[df['종목코드'] == stock_id].empty:
        return jsonify({'error': 'Stock not found'}), 404
    
    update_data = request.get_json()
    for key, value in update_data.items():
        if key in df.columns:
            df.loc[df['종목코드'] == stock_id, key] = value
    
    save_df()
    stock = df[df['종목코드'] == stock_id]
    return jsonify(stock.to_dict(orient='records')[0])

@app.route('/stock/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    global df
    if df[df['종목코드'] == stock_id].empty:
        return jsonify({'error': 'Stock not found'}), 404
    
    df = df[df['종목코드'] != stock_id]
    save_df()
    return jsonify({'message': 'Stock deleted'})

if __name__ == '__main__':
    app.run(debug=True)