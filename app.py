from flask import Flask, jsonify, request , render_template , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder="static")

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Device model
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date=db.Column(db.Date())
    class_section = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    condition_remark = db.Column(db.String(200))
    serial_no = db.Column(db.String(100), nullable=False)
    school_serial_no = db.Column(db.String(100), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/credits')
def credits():
    return render_template('credits.html')

@app.route('/adddevice')
def add():
    return render_template('add_device.html')
# Get all devices
@app.route('/api/devices', methods=['GET'])
def get_devices():
    class_section = request.args.get('class_section', None)
    
    if class_section:
        devices = Device.query.filter_by(class_section=class_section).all()
    else:
        devices = Device.query.all()
    
    return jsonify([{
        'id': device.id,
        'description': device.description,
        'date': device.date.strftime('%Y-%m-%d') if device.date else None,
        'class_section': device.class_section,
        'make': device.make,
        'condition': device.condition,
        'condition_remark': device.condition_remark,
        'serial_no': device.serial_no,
        'school_serial_no': device.school_serial_no
    } for device in devices])



@app.route('/api/devices/<int:id>', methods=['GET'])
def get_device(id):
    device = Device.query.get_or_404(id)
    
    # Convert device data to JSON
    device_data = {
        'id': device.id,
        'description': device.description,
        'date': device.date.strftime('%Y-%m-%d'),  # Format the date as a string
        'class_section': device.class_section,
        'make': device.make,
        'condition': device.condition,
        'condition_remark': device.condition_remark,
        'serial_no': device.serial_no,
        'school_serial_no': device.school_serial_no
    }
    
    return jsonify(device_data)

# Add a new device

from datetime import datetime

@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.json
    date_str = data.get('date')
    
    # Convert date from string to Python datetime object
    device_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    new_device = Device(
        description=data['description'],
        date=device_date,  # Save the parsed date
        class_section=data['class_section'],
        make=data['make'],
        condition=data['condition'],
        condition_remark=data.get('condition_remark', ''),
        serial_no=data['serial_no'],
        school_serial_no=data['school_serial_no']
    )

    db.session.add(new_device)
    db.session.commit()

    return jsonify({'message': 'Device added successfully!'}), 201


# Edit a device
@app.route('/api/devices/<int:id>', methods=['PUT'])
def edit_device(id):
    device = Device.query.get_or_404(id)
    data = request.json
    date_str = data.get('date')

    # Parse the date string if provided
    device.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else device.date

    device.description = data['description']
    device.class_section = data['class_section']
    device.make = data['make']
    device.condition = data['condition']
    device.condition_remark = data.get('condition_remark', '')
    device.serial_no = data['serial_no']
    device.school_serial_no = data['school_serial_no']
    
    db.session.commit()
    return jsonify({'message': 'Device updated successfully!'})

# Delete a device
@app.route('/api/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
