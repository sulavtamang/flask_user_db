from flask import Flask, jsonify, request
from db_operations import DBOperations


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<--------server is running------->"


@app.route('/init-db', methods=['GET'])
def init_db():
    if not DBOperations.table_exists('users'):
        DBOperations.create_table('users')
        return jsonify({'message' : 'users table successfully created in the database.'})
    return jsonify({'message' : 'users table already in the database'})


@app.route('/clear-users-table', methods=['GET'])
def clear_table():
    if not DBOperations.table_exists('users'):
        return jsonify({'message' : 'users table not in the database'})

    DBOperations.clear_table('users')
    return jsonify({'message' : f'users table successfully cleared'})



@app.route('/rm-users-table', methods=['GET'])
def remove_table():
    if not DBOperations.table_exists('users'):
        return jsonify({'message' : 'users table does not exist in the database.'})
    
    DBOperations.drop_table('users')
    return jsonify({'message' : 'users table successfully removed from the database.'})



@app.route('/fetch-all-users', methods=['GET'])
def get_users():
    if not DBOperations.table_exists('users'):
        return jsonify({'message' : 'database not initiated'})
    
    users = DBOperations.get_all_users()

    if not users:
        return jsonify({'message' : 'empty database'})
    
    return jsonify(users)


@app.route('/search-user')
def search_user():
    try:
        name = request.args.get('name', '').strip()
        address = request.args.get('address', '').strip()

        if not name or not address:
            return jsonify({'message' : 'both name and address field must be filled'})
        
        elif not DBOperations.table_exists('users'):
            return jsonify({'message' : 'database not initiated'})
        
        elif not DBOperations.user_exists(name, address):
            return jsonify({'message' : f'Given user {name} not found.'})
        
        else:
            users = DBOperations.get_user(name, address)
            return jsonify(users)
    
    except Exception as e:
        return jsonify({'message' : str(e)})


@app.route('/add-user', methods=['GET'])
def add_user():
    try:
        name = request.args.get('name')
        address = request.args.get('address')

        if not name or not address:
            return jsonify({'message' : f'please provide name and address'})
        
        elif not DBOperations.table_exists('users'):
            return jsonify({'message' : 'users table not initiated'})
        else:
            DBOperations.insert_user(name, address)
            
            if DBOperations.user_exists(name, address):
                return jsonify({'message' : f'user {name} successfully added.'})
            return jsonify({'message' : f'error occured while inserting user into the database'})
    
    except Exception as e:
        return jsonify({'message' : str(e)})
    

@app.route('/rm-user', methods=['GET'])
def remove_user():
    name = request.args.get('name')
    address = request.args.get('address')

    if not name or not address:
        return jsonify({'message' : 'please provide both name and address'})

    elif not DBOperations.table_exists('users'):
        return jsonify({'message' : 'users table not in the database'})
    
    elif not DBOperations.user_exists(name, address):
        return jsonify({'message' : f'user {name} of address {address} not in the database'})
    
    else:
        DBOperations.remove_user(name, address)

        return jsonify({'message' : f'user {name} successfully removed from the table'})
    


if __name__ == '__main__':
    app.run(debug=True)