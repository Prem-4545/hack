# Hack - Secure Authentication System

A comprehensive user authentication and management system built with Flask. Features user registration, login, profile management, and secure database storage for a robust web application foundation.

## 🎯 Features

- **User Registration** - Create new user accounts with validation
- **Secure Login** - Password-based authentication
- **User Profiles** - View and manage user information
- **Session Management** - Secure session handling
- **Database Integration** - SQLite for persistent data storage
- **Input Validation** - Security checks for all user inputs
- **Responsive UI** - Modern and user-friendly interface
- **Error Handling** - Comprehensive error messages and handling

## 🛠️ Technologies Used

- **Backend:**

  - Python 3.x
  - Flask - Web framework
  - SQLite3 - Database
  - Flask Sessions - Session management

- **Frontend:**
  - HTML5 - Structure and markup
  - CSS3 - Styling and responsive design
  - JavaScript - Client-side interactions

## 📂 Project Structure

```
hack/
├── app.py              # Main Flask application
├── db_utils.py         # Database utility functions
├── index.html          # Home/Registration page
├── profile.html        # User profile page
├── users.db            # SQLite database
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## 📋 Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Modern web browser
- SQLite3 (usually included with Python)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Prem-4545/hack.git
cd hack
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access the Application

Open your browser and navigate to:

```
http://localhost:5000
```

## 📝 Usage Guide

### Registration

1. Navigate to the home page
2. Fill in registration form with:
   - Username (unique)
   - Email address
   - Password (strong recommended)
3. Click "Register"
4. Receive confirmation message

### Login

1. Enter your username and password
2. Click "Login"
3. Access your profile dashboard
4. View and edit your information

### Profile Management

1. View your registered information
2. Update profile details (if enabled)
3. Change password (if enabled)
4. Logout from profile page

## 🔐 Security Features

- **Password Security** - Passwords are securely stored
- **Session Management** - Sessions expire after inactivity
- **Input Validation** - All inputs validated server-side
- **SQL Injection Prevention** - Parameterized queries used
- **XSS Protection** - Proper output encoding

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Change Port

Edit `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

### Customize Database

Modify `db_utils.py` to:

- Add new user fields
- Implement encryption
- Add backup functionality
- Add export features

### Customize UI

Edit HTML files to:

- Change colors and themes
- Modify form fields
- Update branding
- Add new pages

## 📊 API Endpoints

### Register User

```
POST /register
Body: { "username": "user", "email": "user@example.com", "password": "pass" }
Response: { "status": "success", "message": "Registration successful" }
```

### Login

```
POST /login
Body: { "username": "user", "password": "pass" }
Response: { "status": "success", "redirect": "/profile" }
```

### Get Profile

```
GET /profile
Response: { "username": "user", "email": "user@example.com", "created_at": "..." }
```

### Logout

```
GET /logout
Response: Redirect to home page
```

## 🐛 Troubleshooting

### Database Errors

```bash
# Reset database
rm users.db
python app.py
```

### Port Already in Use

```bash
# Use different port
# Edit app.py and change port number
```

### Module Not Found

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Future Enhancements

- ✅ Email verification for registration
- ✅ Password reset functionality
- ✅ Two-factor authentication (2FA)
- ✅ Social media login integration
- ✅ User roles and permissions
- ✅ Admin dashboard
- ✅ Activity logging
- ✅ HTTPS/SSL support

## 🎨 Customization Examples

### Add Remember Me

```python
@app.route('/login', methods=['POST'])
def login():
    # ... authentication code ...
    remember = request.form.get('remember_me')
    # ... set session expiry based on remember ...
```

### Add Email Verification

```python
def send_verification_email(email, token):
    # Send email with verification link
    pass
```

## 📖 Example Usage

```
1. User visits http://localhost:5000
2. Completes registration form
3. User logs in with credentials
4. Views profile page
5. Can update information
6. Logs out securely
```

## 🤝 Contributing

Contributions are welcome! Please:

- Fork the repository
- Create a feature branch
- Commit your changes
- Push to the branch
- Create a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Security Notice

This is an educational project. For production use:

- Use proper password hashing (bcrypt, argon2)
- Enable HTTPS/SSL
- Implement CSRF protection
- Use environment variables for secrets
- Regular security audits
- Keep dependencies updated

## 👤 Author

**Prem-4545**

- GitHub: [@Prem-4545](https://github.com/Prem-4545)
- Email: jpremchand4939@gmail.com

## ⭐ Support

If you find this authentication system helpful, please give it a star! ⭐

---

**Last Updated:** January 6, 2026
**Version:** 1.0
