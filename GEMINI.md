# GEMINI

## Flask + Excel CRUD with Pagination, Sorting, and Search

This guide explains how to create a Flask web application that performs CRUD (Create, Read, Update, Delete) operations on an Excel file. The application includes features like pagination, sorting, and searching, and is styled using Bootstrap.

### Project Structure

First, create the following folder and file structure for your project:

```
/your-project-folder
|-- /templates
|   |-- index.html
|-- app.py
|-- data.xlsx
```

### `data.xlsx` Setup

Create an Excel file named `data.xlsx` in the root of your project folder. Add the following columns and some sample data:

| ID | Name    | Age |
|----|---------|-----|
| 1  | Alice   | 24  |
| 2  | Bob     | 27  |
| 3  | Charlie | 22  |
| 4  | David   | 32  |
| 5  | Eve     | 28  |

### `app.py`

This is the main application file. It uses Flask for the web framework and pandas to interact with the Excel file.

**Installation:**

Before running the app, you need to install the required Python libraries:

```bash
pip install Flask pandas openpyxl
```

**Code:**

```python
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
```

### `templates/index.html`

This file contains the HTML structure and uses Bootstrap for styling. It also includes the logic for displaying data, pagination, sorting, and search.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Excel CRUD</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="mb-4">Flask Excel CRUD</h1>

        <!-- Search Form -->
        <form method="GET" action="{{ url_for('index') }}" class="mb-3">
            <div class="input-group">
                <input type="text" class="form-control" name="search" placeholder="Search..." value="{{ search_query }}">
                <button class="btn btn-outline-secondary" type="submit">Search</button>
            </div>
        </form>

        <!-- Add Data Form -->
        <div class="card mb-4">
            <div class="card-header">
                Add New Record
            </div>
            <div class="card-body">
                <form action="{{ url_for('add') }}" method="POST">
                    <div class="row">
                        <div class="col">
                            <input type="text" class="form-control" name="name" placeholder="Name" required>
                        </div>
                        <div class="col">
                            <input type="number" class="form-control" name="age" placeholder="Age" required>
                        </div>
                        <div class="col">
                            <button type="submit" class="btn btn-primary">Add</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <!-- Data Table -->
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    {% for col in columns %}
                    <th>
                        <a href="{{ url_for('index', sort_by=col, sort_order='asc' if sort_by != col or sort_order == 'desc' else 'desc', search=search_query) }}">
                            {{ col }}
                            {% if sort_by == col %}
                                {% if sort_order == 'asc' %}▲{% else %}▼{% endif %}
                            {% endif %}
                        </a>
                    </th>
                    {% endfor %}
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    <form action="{{ url_for('edit', id=row.ID) }}" method="POST">
                        <td>{{ row.ID }}</td>
                        <td><input type="text" class="form-control" name="name" value="{{ row.Name }}"></td>
                        <td><input type="number" class="form-control" name="age" value="{{ row.Age }}"></td>
                        <td>
                            <button type="submit" class="btn btn-sm btn-warning">Save</button>geo
                            <a href="{{ url_for('delete', id=row.ID) }}" class="btn btn-sm btn-danger">Delete</a>
                        </td>
                    </form>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Pagination -->
        <nav>
            <ul class="pagination">
                {% for i in range(1, (total_rows // per_page) + 2) %}
                <li class="page-item {% if i == page %}active{% endif %}">
                    <a class="page-link" href="{{ url_for('index', page=i, sort_by=sort_by, sort_order=sort_order, search=search_query) }}">{{ i }}</a>
                </li>
                {% endfor %}
            </ul>
        </nav>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### How to Run the Application

1.  Make sure you have created the `data.xlsx` file and the `templates` folder with `index.html` inside.
2.  Open your terminal or command prompt.
3.  Navigate to your project folder.
4.  Run the following command:

    ```bash
    python app.py
    ```

5.  Open your web browser and go to `http://127.0.0.1:5000`.

You should now see the web application running, displaying the data from your Excel file. You can add, edit, delete, search, and sort the data.
