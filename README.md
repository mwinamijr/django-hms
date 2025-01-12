# Hospital Management System API 🚑

A robust and scalable **Hospital Management System API** built with **Django** and **Django REST Framework (DRF)**. This backend system is designed to provide secure and efficient APIs for managing hospital operations such as patients, doctors, appointments, and medical records. Authentication is handled using **JWT (JSON Web Tokens)** to ensure secure access.

## Features 🌟
- **Patient Management API**: Endpoints to create, update, and retrieve patient records.
- **Doctor Management API**: Endpoints to manage doctor profiles, specializations, and schedules.
- **Appointment Scheduling API**: APIs to book and manage appointments.
- **Medical Records API**: Endpoints for maintaining and accessing detailed medical histories and prescriptions.
- **Role-Based Access Control**: Secure APIs with role-specific permissions for administrators, doctors, and staff.
- **JWT Authentication**: Secure token-based authentication for all endpoints.

## Tech Stack 🛠️
- **Backend**: Django (Python)
- **API Framework**: Django REST Framework (DRF)
- **Authentication**: JSON Web Tokens (JWT)
- **Database**: PostgreSQL
- **Deployment**: Configured for deployment on platforms like Heroku or AWS.

## Setup Instructions 🖥️

Follow these steps to set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-hms.git
   ```

2. Navigate to the project directory:
   ```bash
   cd django-hms
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate # On Windows: env\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure the database in the `settings.py` file to connect to PostgreSQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your-database-name',
           'USER': 'your-database-user',
           'PASSWORD': 'your-database-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser account to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

9. Access the API at `http://127.0.0.1:8000`.

## API Documentation 📜
This project uses Django REST Framework's built-in API documentation or can be extended with tools like Swagger or Postman collections for better visualization.

## Contributing 🤝
We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License 📜
This project is licensed under the [MIT License](LICENSE).

## Contact 📧
For questions or feedback, feel free to contact me at [mwinamijr@gmail.com](mwinamijr) or [techdometz@gmail.com](Techdometz).
