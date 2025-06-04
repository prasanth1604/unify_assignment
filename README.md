# 🏋️‍♀️ CultFit(not so cultfit) – Your Personal Fitness Class Scheduler

Welcome to **CultFit**, a Django-powered REST API app where clients can explore, book, and manage their fitness class schedule effortlessly. From yoga at sunrise to HIIT at sunset – we've got your fitness goals covered!

---

## 🚀 Features

- 🗓️ View all available fitness classes with real-time slot tracking  
- 👤 Register for a class with your name and email  
- 📩 Check all your booked classes using just your email  
- 🔐 Input validation ensures clean and secure data  
- 🌍 Timezone-aware – shows correct class times based on your local timezone  
- ⚙️ Built with Django + Django REST Framework  

---

## 📦 API Endpoints

### `GET /classes/`  
Returns a list of all upcoming classes with available slots.  
✅ Filters out fully-booked classes.

---

### `POST /book/`  
Registers a client for a class.  
📌 Request JSON:
```json
{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```
### `GET /bookings/<email-id>/`
Example url: /bookings/rohith@gmail.com




# INSTRUCTIONS TO RUN THIS APPLICATION

## Backend( Django )

#### Installing

open terminal and type

```
git clone https://github.com/prasanth1604/cult_assignment.git
```
#### Creating virtual environment is highly recommended. Follow steps from the link given below
#### https://docs.python.org/3/library/venv.html#creating-virtual-environments

#### Now, Navigate to the project folder

#### Requirements

To install requirements type

```
pip install -r requirements.txt
```

Navigate to main folder
```
cd cultfit
```


To migrate the database open terminal in project directory and type

```
python manage.py makemigrations
python manage.py migrate
```

To run the program in local server use the following command

```
python manage.py runserver
```



## Frontend( React ) --> For better user experience

#### Installing

open terminal and type

Navigate to cultfit/frontend


#### Requirements

```
cd cultfit/frontend
```

To install requirements type

```
npm install react react-router-dom axios cors
```

```
npm install
```

To migrate the database open terminal in project directory and type

```
npm run dev
```

## Now the frontend page runs at localhost:5173
