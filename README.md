# 🏗️ SmartBuild Hub

SmartBuild Hub is a **Django-based construction management platform** that connects clients with contractors. Clients can create construction projects, contractors can submit bids, and clients can compare bids and select the most suitable contractor.

## 🌐 Live Demo

🚀 **[Visit SmartBuild Hub Live Demo](https://smart-build-hub-navy.vercel.app)**



## ✨ Features

* 👤 Client registration and login
* 👷 Contractor registration and login
* 🏠 Create and manage construction projects
* 📋 Contractors can view available projects
* 💰 Contractor bidding system
* 🤝 Compare contractor bids
* ✅ Select a contractor
* 📊 Track project progress
* 📈 Client and contractor dashboards
* 🔐 Authentication and authorization
* 🛠️ Django Admin panel
* 📱 Responsive Bootstrap design

## 🔄 How It Works

```text
Client
  ↓
Register / Login
  ↓
Create Construction Project
  ↓
Contractors View Project
  ↓
Contractors Submit Bids
  ↓
Client Compares Bids
  ↓
Client Selects Contractor
  ↓
Project Starts
  ↓
Contractor Updates Progress
  ↓
Client Tracks Progress
```

## 🛠️ Tech Stack

**Frontend**

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Bootstrap Icons
* AOS

**Backend**

* Python
* Django

**Database**

* SQLite
* SQL

**Tools**

* VS Code
* Git
* GitHub
* Vercel

## 👥 User Roles

### 👤 Client

* Register and log in
* Create construction projects
* View contractor bids
* Compare prices
* Select contractors
* Track project progress

### 👷 Contractor

* Register and log in
* View available projects
* Submit project bids
* Manage assigned projects
* Update project progress

### 👨‍💼 Super Admin

* Manage users
* Manage contractors
* Manage projects
* Monitor platform activities
* Manage application data through Django Admin

## 📂 Project Structure

```text
SmartBuild-Hub/
│
├── manage.py
├── requirements.txt
├── vercel.json
│
├── smartbuild/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
└── README.md
```

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/akashchauhan1230/SmartBuild-Hub.git
cd SmartBuild-Hub
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run the Project

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🚀 Deployment

The project can be deployed using **Vercel** with the required Django configuration, `requirements.txt`, and `vercel.json`.

## 🔮 Future Enhancements

* 💳 Online payment integration
* 🔔 Real-time notifications
* 💬 Client-contractor chat
* ⭐ Contractor ratings and reviews
* 📧 Email notifications
* 🗺️ Google Maps integration
* 📄 Project document management
* 📊 Advanced analytics

## 🎯 Project Objective

The main objective of SmartBuild Hub is to **simplify construction project management by providing a centralized platform where clients can find contractors, receive competitive bids, select contractors, and monitor project progress.**

## 👨‍💻 Developer

**Akash Chauhan**

* GitHub: https://github.com/akashchauhan1230
* LinkedIn: https://www.linkedin.com/in/akash-chauhan-762319357/

## 📄 License

This project was developed for **educational and portfolio purposes**.

---

⭐ **If you like this project, consider giving the repository a star!**

