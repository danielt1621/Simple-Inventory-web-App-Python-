from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = '0000'  # secret key for sessions no reason for encryption yet

FILE_PATH = 'inventory_data.json'

def load_inventory():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {'items': []}
    return {'items': []}

def save_inventory(inventory):
    with open(FILE_PATH, 'w') as file:
        json.dump(inventory, file)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def check_stock_by_category(category_filter=None, exclude_consumables=False):
    inventory = load_inventory()

     # Filter based on the exclude_consumables flag
    if exclude_consumables:
        inventory['items'] = [item for item in inventory['items'] if item['category'] != 'Consumables']
    elif category_filter:
        inventory['items'] = [item for item in inventory['items'] if item['category'] == category_filter]

    # Separate items into low stock and out of stock categories
    low_stock_items = [item for item in inventory['items'] if 1 <= item['quantity'] <= 2]
    out_of_stock_items = [item for item in inventory['items'] if item['quantity'] == 0]

    return low_stock_items, out_of_stock_items

SMTP_SERVER = 'smtp.office365.com'  # E.g., 'smtp.gmail.com'
SMTP_PORT = 587  # Use 465 for SSL or 587 for TLS
EMAIL_ADDRESS = 'tdanny162108@outlook.com'
EMAIL_PASSWORD = 'onjvxdsxxyavvtoe'

def send_email(subject, body, is_html=False):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject

    #msg.attach(MIMEText(body, 'plain')) Use for simple plain email content

    if is_html:
        msg.attach(MIMEText(body, 'html'))  # Send as HTML  
    else:
        msg.attach(MIMEText(body, 'plain'))  # Send as plain text

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

 
def scheduled_task_consumables():
    low_stock_items, out_of_stock_items = check_stock_by_category('Consumables')

       # Create HTML table for low stock items with inline CSS
    if low_stock_items:
        low_stock_body = '''
        <html>
        <body style="background-color: #f8f7ed;">
        <h2><strong>The following Consumables are <u style="color: #ff9800; text-decoration: none;">low</u> on stock:</strong></h2>
        <table style="width: 100%; border-collapse: collapse; ">
            <thead>
                <tr style="background-color: #f44336; color: white; ">
                    <th style="padding: 8px; text-align: left;">Name</th>
                    <th style="padding: 8px; text-align: left;">Quantity</th>
                    <th style="padding: 8px; text-align: left;">Assigned To</th>
                    <th style="padding: 8px; text-align: left;">Category</th>
                </tr>
            </thead>
            <tbody>
        '''
        # Alternate row background color (even rows will have gray background)
        for i, item in enumerate(low_stock_items):
            background_color = "#f2f2f2" if i % 2 == 0 else "white"
            low_stock_body += f'''
            <tr style="background-color: {background_color};">
                <td style="padding: 8px;">{item['name']}</td>
                <td style="padding: 8px;">{item['quantity']}</td>
                <td style="padding: 8px;">{item['assignedTo']}</td>
                <td style="padding: 8px;">{item['category']}</td>
            </tr>
            '''
        low_stock_body += '''
            </tbody>
        </table>
        </body>
        </html>
        '''
        send_email('Low Stock Alert for Consumables', low_stock_body, is_html=True)

    # Create HTML table for out of stock items with inline CSS
    if out_of_stock_items:
        out_of_stock_body = '''
        <html>
        <body style="background-color: #f8f7ed;">
        <h2><strong>The following Consumables are <u style="color: red; text-decoration: none;">out</u> of stock:</strong></h2>
        <table style="width: 100%; border-collapse: collapse; ">
            <thead>
                <tr style="background-color: #f44336; color: white; ">
                    <th style="padding: 8px; text-align: left;">Name</th>
                    <th style="padding: 8px; text-align: left;">Quantity</th>
                    <th style="padding: 8px; text-align: left;">Assigned To</th>
                    <th style="padding: 8px; text-align: left;">Category</th>
                </tr>
            </thead>
            <tbody>
        '''
        # Alternate row background color (even rows will have gray background)
        for i, item in enumerate(out_of_stock_items):
            background_color = "#f2f2f2" if i % 2 == 0 else "white"
            out_of_stock_body += f'''
            <tr style="background-color: {background_color};">
                <td style="padding: 8px;">{item['name']}</td>
                <td style="padding: 8px;">{item['quantity']}</td>
                <td style="padding: 8px;">{item['assignedTo']}</td>
                <td style="padding: 8px;">{item['category']}</td>
            </tr>
            '''
        out_of_stock_body += '''
            </tbody>
        </table>
        </body>
        </html>
        '''
        send_email('Out of Stock Alert for Consumables', out_of_stock_body, is_html=True)



def scheduled_task_others():
   # Check for all items except those in the "Consumables" category
    low_stock_items, out_of_stock_items = check_stock_by_category(exclude_consumables=True)

     # Create HTML table for low stock items with inline CSS
    if low_stock_items:
        low_stock_body = '''
        <html>
        <body style="background-color: #f8f7ed;">
        <h2><strong>The following items are <u style="color: #ff9800; text-decoration: none;">low</u> on stock:</strong></h2>
        <table style="width: 100%; border-collapse: collapse; ">
            <thead>
                <tr style="background-color: #3c83f6; color: white; ">
                    <th style="padding: 8px; text-align: left;">Name</th>
                    <th style="padding: 8px; text-align: left;">Quantity</th>
                    <th style="padding: 8px; text-align: left;">Assigned To</th>
                    <th style="padding: 8px; text-align: left;">Category</th>
                </tr>
            </thead>
            <tbody>
        '''
        # Alternate row background color (even rows will have gray background)
        for i, item in enumerate(low_stock_items):
            background_color = "#f2f2f2" if i % 2 == 0 else "white"
            low_stock_body += f'''
            <tr style="background-color: {background_color};">
                <td style="padding: 8px;">{item['name']}</td>
                <td style="padding: 8px;">{item['quantity']}</td>
                <td style="padding: 8px;">{item['assignedTo']}</td>
                <td style="padding: 8px;">{item['category']}</td>
            </tr>
            '''
        low_stock_body += '''
            </tbody>
        </table>
        </body>
        </html>
        '''
        send_email('Low Stock Alert for Items', low_stock_body, is_html=True)

    # Create HTML table for out of stock items with inline CSS
    if out_of_stock_items:
        out_of_stock_body = '''
        <html>
        <body style="background-color: #f8f7ed;">
        <h2><strong>The following items are <u style="color: red; text-decoration: none;">out</u> of stock:</strong></h2>
        <table style="width: 100%; border-collapse: collapse; ">
            <thead>
                <tr style="background-color: #3c83f6;  color: white; ">
                    <th style="padding: 8px; text-align: left;">Name</th>
                    <th style="padding: 8px; text-align: left;">Quantity</th>
                    <th style="padding: 8px; text-align: left;">Assigned To</th>
                    <th style="padding: 8px; text-align: left;">Category</th>
                </tr>
            </thead>
            <tbody>
        '''
        # Alternate row background color (even rows will have gray background)
        for i, item in enumerate(out_of_stock_items):
            background_color = "#f2f2f2" if i % 2 == 0 else "white"
            out_of_stock_body += f'''
            <tr style="background-color: {background_color};">
                <td style="padding: 8px;">{item['name']}</td>
                <td style="padding: 8px;">{item['quantity']}</td>
                <td style="padding: 8px;">{item['assignedTo']}</td>
                <td style="padding: 8px;">{item['category']}</td>
            </tr>
            '''
        out_of_stock_body += '''
            </tbody>
        </table>
        </body>
        </html>
        '''
        send_email('Out of Stock Alert for Items', out_of_stock_body, is_html=True)


scheduler = BackgroundScheduler() 
scheduler.add_job(scheduled_task_consumables, 'cron', hour=10, minute=0)  # Check consumables every day at 10am
scheduler.add_job(scheduled_task_others, 'interval', days=3, start_date='2024-01-01 10:05:00')  # Check non-consumables every 3 days at 11am
scheduler.start()
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.route('/trigger_email')
def trigger_email():
    scheduled_task_consumables()
    scheduled_task_others()  # Manually trigger the low stock email check
    return "Email triggered! "# Test code to manually trigger the email

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '0000':
                session['logged_in'] = True
                return redirect(url_for('index'))
        else:
            error = 'Invalid password. If you forgot your password, contact your admin.'
            return render_template('login.html', error=error)
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
    

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        return jsonify(load_inventory())
    elif request.method == 'POST':
        inventory = load_inventory()
        new_item = request.json
        new_item['id'] = max([item['id'] for item in inventory['items']] + [0]) + 1
        inventory['items'].append(new_item)
        save_inventory(inventory)
        return jsonify({"message": "Item added successfully!", "id": new_item['id']})

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item(item_id):
    inventory = load_inventory()
    item_index = next((index for (index, d) in enumerate(inventory['items']) if d["id"] == item_id), None)
    
    if item_index is None:
        return jsonify({"error": "Item not found"}), 404

    if request.method == 'GET':
        return jsonify(inventory['items'][item_index])
    
    elif request.method == 'PUT':
        updated_item = request.json
        inventory['items'][item_index].update(updated_item)
        save_inventory(inventory)
        return jsonify({"message": "Item updated successfully!"})
    
    elif request.method == 'DELETE':
        del inventory['items'][item_index]
        save_inventory(inventory)
        return jsonify({"message": "Item deleted successfully!"})

if __name__ == '__main__':
    '''app.run(debug=True)'''
    app.run(host='0.0.0.0', port=5000, debug=True)
