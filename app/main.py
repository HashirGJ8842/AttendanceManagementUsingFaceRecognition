from datetime import timedelta, date, datetime

from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import RegistrationForm, LoginForm, AdminRegister, AddLocationForm
import calendar
from flask_pymongo import PyMongo
import Employee as emp
from Employee import Employee, getAttendanceByDate, collection
from flask_bcrypt import Bcrypt
from Location import Location, getAll
import Location
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '8924989289289289'


@app.route("/")
def index():
    return render_template('home.html')


# Register Employee Route
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = emp.Employee(int(form.employee_id.data))
        request = employee.addUser(form.firstName.data, form.lastName.data)
        if request is True:
            flash('Account created for {}!'.format(form.employee_id.data), 'success')
            return redirect(url_for('viewAll'))
        else:
            return redirect(url_for('register'))
    return render_template('register.html', form=form)


# Register Employee Route
@app.route("/employee")
def viewAll():
    data = emp.getAll()

    return render_template('view_all.html', data=data, calendar=calendar, title="Employee", Employee=Employee)


# Display employee Information here
@app.route("/employee/<employee_id>", methods=['POST', 'GET'])
def userInfo(employee_id):
    if request.method=='POST':
        req = request.form.get('offDay')
        Employee(int(employee_id)).setOffDay(int(req))
        penalty = request.form.get('penalty')
        if penalty != "None":
            Employee(int(employee_id)).addPenalty(int(penalty))
            print(penalty)
    employee_id = int(employee_id)
    data = emp.Employee(employee_id)
    penaltyList = list(collection.find({"emp_id":employee_id}))
    attendances = list(data.viewAttendance())[0]['attendance']
    return render_template('userinfo.html', emp_id=employee_id, data=data, attendances=attendances, calendar=calendar,penaltyList=penaltyList)


# Display Location Information here
@app.route("/location/<int:location_id>", methods=['POST', 'GET'])
def locationInfo(location_id):
    if request.method == 'POST':
        min = int(request.form.get('min'))
        max = int(request.form.get('max'))
        Location.collection.update(
            {"locationID":location_id},

            {
                "$set":
                {
                    "minimum":min,
                    "maximum":max
                }
            }
        )
    location_id = int(location_id)
    LocationData = Location.collection.find({"locationID":location_id}).sort('locationID')
    dailyData  = list(collection.find({"attendance.location":location_id}))
    return render_template('locationInfo.html', data=LocationData,dailyData=dailyData,location_id=location_id)







# Login Page Route
@app.route("/login")
def login():
    return render_template('login.html')


# Add Locations
@app.route("/locations/add", methods=['GET', 'POST'])
def addLocation():
    locationForm = AddLocationForm()
    if locationForm.validate_on_submit():

        location = Location(int(locationForm.location_id.data))
        request = location.addLocation(locationForm.name.data, locationForm.minimum_required.data,
                                       locationForm.maximum_required.data)
        if request is True:
            return redirect(url_for('viewLocations'))

    return render_template("location.html", form=locationForm)


# Daily Attendance
@app.route("/attendance/<date>")
def attendanceByDate(date):
    # dateStr = date[:4] + '-' + date[4:6] + '-' + date[6:8]
    data = (collection.find({"attendance.date": date}))
    return render_template("attendanceByDate.html", data=data, dateStr=date)


# View Locations
@app.route("/locations/view_all")
def viewLocations():
    data = getAll().sort('locationID')
    return render_template('view_all_locations.html', data=data, calendar=calendar, title="Locations")


# API CALL
@app.route("/api")
def getEmployeeInformation():
    x = list(emp.getAll())
    data = []
    for value in x:
        data.append({"emp_id": value['emp_id']})

    return jsonify({"result": data})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')




