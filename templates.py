base_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Flask App{% endblock %}</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <!-- Font Awesome icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <!-- Your custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% block extra_css %}{% endblock %}
    <style>
        /* Custom CSS for base.html */
        body {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
            padding-top: 70px;
        }
        .navbar {
            background-color: #343a40;
            padding: 0.75rem 1rem;
        }
        .navbar-brand {
            font-size: 1.5rem;
            font-weight: bold;
            color: #fff;
        }
        .nav-link {
            color: #fff;
            font-weight: bold;
            padding: 0.75rem 1rem;
        }
        .nav-link:hover {
            color: #ffc107;
        }
        .nav-link.active {
            color: #ffc107;
        }
        .navbar-toggler {
            border: none;
        }
        .navbar-toggler:focus {
            outline: none;
            box-shadow: none;
        }
        .container {
            margin-top: 2rem;
        }
        .footer {
            background-color: #343a40;
            color: #fff;
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .footer p {
            margin-bottom: 0;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">View Labs</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <i class="fas fa-bars"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="/"><i class="fas fa-home mr-1"></i> Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#!"><i class="fas fa-bell mr-1"></i> Notifications</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt mr-1"></i> Logout</a>
                    </li>
                </ul>
                <form class="form-inline my-2 my-lg-0">
                    <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-light my-2 my-sm-0" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>

    <!-- Main content -->
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>

    <!-- Footer -->
    <footer class="footer text-center mt-auto py-3">
        <div class="container">
            <p>&copy; 2024 My Flask App. All rights reserved.</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <!-- Your custom JS -->
    <script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>


'''

index_template = '''
{% extends "base.html" %}

{% block title %}Welcome to My Flask App{% endblock %}

{% block content %}
<section class="vh-100 d-flex align-items-center justify-content-center">
    <div class="jumbotron text-center bg-light shadow p-5">
        <h1 class="display-4">Welcome to View Labs!</h1>
        <p class="lead">This is a simple web application built with Flask.</p>
        <hr class="my-4">
        <p>It allows users to book computers in labs and manage their bookings efficiently.</p>
        {% if form %}
            <div class="mt-4">
                <a class="btn btn-primary btn-lg mr-2" href="/register" role="button">Register</a>
                <a class="btn btn-success btn-lg" href="/login" role="button">Login</a>
            </div>
        {% else %}
            <!-- Handle the case where form is not available -->
            <p class="lead mt-4">
                Please <a href="/login" class="text-primary">login</a> or <a href="/register" class="text-primary">register</a> to access the application.
            </p>
        {% endif %}
    </div>
</section>

<style>
    body {
        background: linear-gradient(120deg, #f6d365 0%, ##F8F9FA 100%);
        font-family: 'Arial', sans-serif;
    }
    .jumbotron {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 40px;
    }
    .jumbotron h1 {
        font-weight: 700;
        color: #333;
    }
    .jumbotron p {
        font-size: 1.2em;
    }
    .btn-lg {
        padding: 10px 20px;
        border-radius: 50px;
        font-size: 1.2em;
        transition: background-color 0.3s ease;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .btn-success {
        background-color: #28a745;
        border: none;
    }
    .btn-success:hover {
        background-color: #218838;
    }
</style>
{% endblock %}


'''

login_template = '''
{% extends "base.html" %}
{% block title %}Login - University Lab Booking{% endblock %}
{% block content %}
<section class="vh-100 d-flex align-items-center justify-content-center">
  <div class="login-container">
    <h2>Login</h2>
    <form method="post">
      {{ form.csrf_token }}
      <!-- Username input -->
      <div class="form-group">
        {{ form.username(class="form-control", placeholder="Username", required=True) }}
      </div>

      <!-- Password input -->
      <div class="form-group">
        {{ form.password(class="form-control", placeholder="Password", required=True) }}
      </div>

      <!-- Remember me checkbox -->
      <div class="form-check mb-3">
        <input class="form-check-input" type="checkbox" id="rememberMe" checked>
        <label class="form-check-label" for="rememberMe">Remember me</label>
      </div>

      <!-- Submit button -->
      <button type="submit" class="btn btn-primary btn-block login-button">Login</button>
    </form>

    <!-- Register link -->
    <p class="register-link mt-3">Don't have an account? <a href="{{ url_for('register') }}">Sign Up</a></p>
    <!-- Forgot password link -->
    
  </div>

  <style>
    body {
      background-color: #f8f9fa;
      font-family: Arial, sans-serif;
    }

    .login-container {
      max-width: 500px;
      width: 100%;
      padding: 30px;
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
    }

    .login-container h2 {
      text-align: center;
      margin-bottom: 30px;
    }

    .form-control {
      border-radius: 20px;
    }

    .login-button {
      border-radius: 20px;
    }

    .register-link {
      text-align: center;
    }
  </style>
</section>
{% endblock %}



'''

register_template = '''
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-6">
        <h2 class="text-center mb-4">Register</h2>
        <form method="post">
            {{ form.csrf_token }}
            <div class="form-group">
                <label for="username">Username:</label>
                {{ form.username(class="form-control", id="username") }}
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                {{ form.email(class="form-control", id="email") }}
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                {{ form.password(class="form-control", id="password") }}
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirm Password:</label>
                {{ form.confirm_password(class="form-control", id="confirm_password") }}
            </div>
            <button type="submit" class="btn btn-primary btn-block">Register</button>
        </form>
    </div>
</div>
{% endblock %}

'''
admin_bookings_view ='''
{% extends "base.html" %}

{% block title %}Admin Bookings{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">All Bookings</h1>
    {% if bookings %}
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Student Username</th>
                    <th>PC Details</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                </tr>
            </thead>
            <tbody>
                {% for booking in bookings %}
                <tr>
                    <td>{{ booking.student.username }}</td>
                    <td>{{ booking.computer.details }}</td>
                    <td>{{ booking.start_time }}</td>
                    <td>{{ booking.end_time }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No bookings found.</p>
    {% endif %}
</div>
{% endblock %}


'''
student_dashboard_template = '''
{% extends "base.html" %}
{% block title %}Student Dashboard{% endblock %}
{% block content %}
<div class="container">
    <h1 class="text-center my-4">Welcome to Student Dashboard</h1>

    <div class="row justify-content-center">
        {% if labs %}
            {% for lab in labs %}
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm border-0">
                        <img src="https://pluspng.com/img-png/computer-lab-png-computer-lab-992.png" class="card-img-top" alt="Computer Lab Image">
                        <div class="card-body text-center">
                            <h5 class="card-title">{{ lab.name }}</h5>
                            <a href="{{ url_for('view_computers_student', lab_id=lab.id) }}" class="btn btn-primary btn-block">View Computers</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <div class="col-12">
                <div class="alert alert-warning text-center" role="alert">
                    No labs found
                </div>
            </div>
        {% endif %}
    </div>
</div>

<style>
    .container {
        margin-top: 2rem;
    }
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .card-img-top {
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    .card-title {
        font-weight: bold;
        color: #343a40;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
        border-radius: 20px;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .alert {
        margin-top: 2rem;
    }
</style>
{% endblock %}

'''

view_computers_student_template = '''
{% extends "base.html" %}

{% block title %}View Computers{% endblock %}

{% block content %}
<div class="container">
    <h1 class="text-center my-4">Computers in {{ lab.name }}</h1>
    <p class="text-center"><strong>Location:</strong> {{ lab.location }}</p>
    <a href="{{ url_for('student_dashboard') }}" class="btn btn-secondary mb-4">Back to Student Dashboard</a>

    <!-- Search Form -->
    <form method="GET" action="{{ url_for('view_computers_student', lab_id=lab.id) }}" class="mb-4">
        <div class="input-group">
            <input type="text" name="search" class="form-control" placeholder="Search for applications..." value="{{ request.args.get('search', '') }}">
            <div class="input-group-append">
                <button class="btn btn-primary" type="submit">Search</button>
            </div>
        </div>
    </form>

    {% if computers %}
        <div class="row justify-content-center">
            {% for computer in computers %}
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm border-0">
                        <img src="https://t3.ftcdn.net/jpg/01/14/34/28/360_F_114342835_4xUSqvc7Sy5uKWxDc4tnYYXYbrh6ShLN.jpg" class="card-img-top" alt="Computer Image">
                        <div class="card-body text-center">
                            <h5 class="card-title">Computer Number: {{ computer.number }}</h5>
                            <p class="card-text"><strong>Applications:</strong> {{ computer.applications }}</p>
                            <p class="card-text"><strong>Status:</strong> {% if computer.booked %} Booked {% else %} Available {% endif %}</p>
                            {% if not computer.booked %}
                            <form action="{{ url_for('book_computer', computer_id=computer.id) }}" method="post">
                                <button type="submit" class="btn btn-primary">Book</button>
                            </form>
                            {% else %}
                                <button class="btn btn-secondary" disabled>Booked</button>
                            {% endif %}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-warning text-center" role="alert">
            No computers found in this lab.
        </div>
    {% endif %}
</div>

<style>
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .btn {
        border-radius: 20px;
    }
</style>
{% endblock %}


'''

view_applications_template = '''
{% extends "base.html" %}

{% block title %}View Applications{% endblock %}

{% block content %}
<div class="container">
    <h1 class="text-center my-4">Applications on Computer {{ computer_name }}</h1>
    <div class="row justify-content-center">
        <div class="col-md-8">
            <ul class="list-group">
                {% for app in applications %}
                    <li class="list-group-item">{{ app }}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
</div>
{% endblock %}
'''

lecturer_dashboard_template = '''
{% extends "base_template" %}
{% block content %}
<h1>Lecturer Dashboard</h1>
<p>This is the lecturer dashboard page.</p>
<!-- Dashboard content for lecturers goes here -->
{% endblock %}
'''

add_lab_template = '''
{% extends "base.html" %}
{% block title %}Add Lab{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-8">
        <h2 class="text-center mb-4">Add Lab</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.name.label(class="form-control-label") }}
                {{ form.name(class="form-control") }}
                {% for error in form.name.errors %}
                    <span class="text-danger">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.location.label(class="form-control-label") }}
                {{ form.location(class="form-control") }}
                {% for error in form.location.errors %}
                    <span class="text-danger">{{ error }}</span>
                {% endfor %}
            </div>
            <button type="submit" class="btn btn-primary">Add Lab</button>
        </form>
    </div>
</div>
{% endblock %}

'''

add_computer_template = '''
{% extends "base.html" %}

{% block title %}Add Computer{% endblock %}

{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-8">
        <h2 class="text-center mb-4">Add Computer to {{ lab.name }}</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.number.label(class="form-control-label") }}
                {{ form.number(class="form-control") }}
                {% for error in form.number.errors %}
                    <span class="text-danger">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.applications.label(class="form-control-label") }}
                {{ form.applications(class="form-control") }}
                {% for error in form.applications.errors %}
                    <span class="text-danger">{{ error }}</span>
                {% endfor %}
            </div>
            <button type="submit" class="btn btn-primary">Add Computer</button>
        </form>
    </div>
</div>
{% endblock %}



'''
view_computers_template= '''
{% extends "base.html" %}

{% block title %}View Computers - {{ lab.name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">{{ lab.name }} - Computers</h1>
    <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to Admin Panel</a>
    {% if computers %}
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Computer ID</th>
                    <th>Details</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for computer in computers %}
                <tr>
                    <td>{{ computer.id }}</td>
                    <td>{{ computer.details }}</td>
                    <td>
                        <a href="{{ url_for('edit_computer', computer_id=computer.id) }}" class="btn btn-primary btn-sm">Edit</a>
                        <form method="post" action="{{ url_for('delete_computer', computer_id=computer.id) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No computers found in this lab.</p>
    {% endif %}
    <a href="{{ url_for('add_computer', lab_id=lab.id) }}" class="btn btn-primary mt-3">Add Computer</a>
</div>
{% endblock %}





'''
admin_panel_template = '''
{% extends "base.html" %}

{% block title %}Admin Panel{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <h2 class="text-center mb-4">Admin Panel</h2>
            {% if current_user.is_authenticated and current_user.role == 'admin' %}
            <div class="mb-4 text-center">
                <a href="{{ url_for('admin_bookings') }}" class="btn btn-info">View All Bookings</a>
            </div>
            {% if labs %}
                {% for lab in labs %}
                    <div class="card mb-3 shadow-sm border-0">
                        <div class="row no-gutters">
                            <div class="col-md-4">
                                <img src="https://pluspng.com/img-png/computer-lab-png-computer-lab-992.png" class="card-img" alt="{{ lab.name }}">
                            </div>
                            <div class="col-md-8">
                                <div class="card-body">
                                    <h5 class="card-title font-weight-bold">{{ lab.name }}</h5>
                                    <p class="card-text">{{ lab.location }}</p>
                                    <div class="d-flex justify-content-between">
                                        <a href="{{ url_for('admin_computers', lab_id=lab.id) }}" class="btn btn-primary btn-sm">View Computers</a>
                                        <a href="{{ url_for('add_computer', lab_id=lab.id) }}" class="btn btn-secondary btn-sm">Add Computer</a>
                                        <form method="post" action="{{ url_for('remove_lab', lab_id=lab.id) }}" style="display: inline;">
                                            <button type="submit" class="btn btn-danger btn-sm">Remove Lab</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-warning text-center" role="alert">
                    No labs found. Please add labs first.
                </div>
            {% endif %}
            <div class="text-center">
                <a href="{{ url_for('add_lab') }}" class="btn btn-success mb-2">Add Lab</a>
                {% if labs %}
                    <a href="{{ url_for('add_computer', lab_id=labs[0].id) }}" class="btn btn-secondary mb-2">Add Computer</a>
                {% endif %}
            </div>
            {% else %}
            <div class="alert alert-danger text-center" role="alert">
                Access denied. You need to be logged in as an admin to access this page.
            </div>
            {% endif %}
        </div>
    </div>
</div>

<style>
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .btn {
        border-radius: 20px;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
    }
    .btn-secondary {
        background-color: #6c757d;
        border: none;
    }
    .btn-danger {
        background-color: #dc3545;
        border: none;
    }
    .btn-info {
        background-color: #17a2b8;
        border: none;
    }
    .btn-success {
        background-color: #28a745;
        border: none;
    }
</style>
{% endblock %}




'''

remove_lab_template = '''
{% extends "base.html" %}
{% block title %}Remove Lab{% endblock %}
{% block content %}
<div class="container">
    <h2 class="text-center my-4">Remove Lab</h2>
    <p>Are you sure you want to remove this lab?</p>
    <form action="{{ url_for('remove_lab', lab_id=lab.id) }}" method="post">
        <button type="submit" class="btn btn-danger">Confirm Removal</button>
    </form>
</div>
{% endblock %}

'''
add_computer_admin = '''
{% extends "base.html" %}

{% block title %}Add Computer{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Add Computer</h1>
    <form method="post">
        <div class="form-group">
            <label for="details">Computer Details</label>
            <input type="text" class="form-control" id="details" name="details" required>
        </div>
        <button type="submit" class="btn btn-primary">Add Computer</button>
    </form>
</div>
{% endblock %}


'''
edit_computer_template='''
{% extends "base.html" %}

{% block title %}Edit Computer{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Edit Computer</h1>
    <form method="post">
        <div class="form-group">
            <label for="details">Computer Details</label>
            <input type="text" class="form-control" id="details" name="details" value="{{ computer.details }}" required>
        </div>
        <button type="submit" class="btn btn-primary">Update</button>
    </form>
</div>
{% endblock %}

'''
remove_computer_template = '''
{% extends "base.html" %}
{% block title %}Remove Computer{% endblock %}
{% block content %}
<div class="container">
    <h2 class="text-center my-4">Remove Computer</h2>
    <p>Are you sure you want to remove this computer?</p>
    <form action="{{ url_for('remove_computer', lab_id=lab.id, computer_id=computer.id) }}" method="post">
        <button type="submit" class="btn btn-danger">Confirm Removal</button>
    </form>
</div>
{% endblock %}

'''

error_403_template = '''
{% extends "base.html" %}

{% block title %}
    403 Forbidden
{% endblock %}

{% block content %}
    <div class="container">
        <h1>403 - Forbidden</h1>
        <p>Sorry, you are not authorized to access this page.</p>
        <p>Return to <a href="{{ url_for('index') }}">home</a>.</p>
    </div>
{% endblock %}
'''

error_404_template = '''
{% extends "base.html" %}

{% block title %}
    404 Not Found
{% endblock %}

{% block content %}
    <div class="container">
        <h1>404 - Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <p>Return to <a href="{{ url_for('index') }}">home</a>.</p>
    </div>
{% endblock %}

'''

error_500_template = '''
{% extends "base.html" %}

{% block title %}
    500 Internal Server Error
{% endblock %}

{% block content %}
    <div class="container">
        <h1>500 - Internal Server Error</h1>
        <p>Sorry, something went wrong on the server.</p>
        <p>Please try again later.</p>
        <p>Return to <a href="{{ url_for('index') }}">home</a>.</p>
    </div>
{% endblock %}

'''

error_template='''
{% extends "base.html" %}

{% block title %}Error{% endblock %}

{% block content %}
    <h2>Error</h2>
    <p>{{ error_message }}</p>
{% endblock %}


'''