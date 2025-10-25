from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Path to the Excel file
EXCEL_FILE = 'data.xlsx'

def get_data():
    """Reads data from the Excel file."""
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=['ID', 'Name', 'Age'])

def save_data(df):
    """Saves the DataFrame to the Excel file."""
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    df = get_data()

    # Search
    search_query = request.args.get('search', '')
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    # Sorting
    sort_by = request.args.get('sort_by', 'ID')
    sort_order = request.args.get('sort_order', 'asc')
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 5
    total_rows = len(df)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = df.iloc[start:end]

    return render_template('index.html',
                           data=paginated_data.to_dict('records'),
                           columns=df.columns.tolist(),
                           page=page,
                           per_page=per_page,
                           total_rows=total_rows,
                           sort_by=sort_by,
                           sort_order=sort_order,
                           search_query=search_query)

@app.route('/add', methods=['POST'])
def add():
    df = get_data()
    new_id = df['ID'].max() + 1 if not df.empty else 1
    new_row = {'ID': new_id, 'Name': request.form['name'], 'Age': request.form['age']}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    df = get_data()
    if id in df['ID'].values:
        idx = df[df['ID'] == id].index[0]
        df.at[idx, 'Name'] = request.form['name']
        df.at[idx, 'Age'] = request.form['age']
        save_data(df)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    df = get_data()
    df = df[df['ID'] != id]
    save_data(df)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
