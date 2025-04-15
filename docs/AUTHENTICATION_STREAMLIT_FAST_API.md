# Authentication System Integration Guide (Issue #3)

This document outlines the implementation of the authentication system that integrates FastAPI's built-in security with Streamlit's frontend for the AI Math Tutor application.

## Overview

Instead of building a complete custom authentication system from scratch, this implementation:

1. Uses FastAPI's built-in OAuth2 security utilities for token-based authentication
2. Leverages Streamlit's session state for managing authentication on the frontend
3. Creates a seamless integration between the two platforms

This approach provides several advantages:
- Uses established, well-tested security patterns
- Reduces the need for custom security code
- Simplifies maintenance
- Provides good security with minimal implementation effort

## Components 

### Backend (FastAPI)

1. **User Model**: Basic user model with username, email, hashed password, and grade level
2. **Authentication Endpoints**:
   - Registration: `/api/auth/register`
   - Form-based OAuth2 Login: `/api/auth/login`
   - JSON-based Login (for Streamlit): `/api/auth/login-json`
   - User Profile: `/api/auth/user`
3. **Security Utilities**:
   - JWT token generation and verification
   - Password hashing with bcrypt
   - `get_current_user` dependency for protected routes

### Frontend (Streamlit)

1. **Authentication Component**: Reusable login/registration form
2. **Session Management**: Utilities to manage authentication state
3. **API Utilities**: Functions to communicate with the backend
4. **Protected Pages**: Components that require authentication

## How It Works

1. **User Registration**:
   - User enters details in the Streamlit registration form
   - Data is sent to the FastAPI backend
   - Backend validates, creates the user, and returns a JWT token
   - Streamlit stores the token in session state

2. **User Login**:
   - User enters credentials in the Streamlit login form
   - Credentials are sent to the FastAPI backend
   - Backend validates and returns a JWT token
   - Streamlit stores the token in session state

3. **Protected Routes**:
   - When accessing protected pages, Streamlit checks if a valid token exists
   - If not, it redirects to the login form
   - API requests include the token in the Authorization header
   - FastAPI verifies the token before processing requests

4. **Session Management**:
   - Token expiration is managed both on the backend and frontend
   - Session state ensures persistent login across page navigation

## Implementation Details

### FastAPI Authentication

The backend uses FastAPI's OAuth2PasswordBearer for token authentication:

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> models.User:
    """Get the current user from the token."""
    # Verify token and return user
```

JWT tokens are created with an expiration time:

```python
def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token for the user"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
```

### Streamlit Authentication Flow

The frontend uses Streamlit's session state to manage authentication:

```python
# Initialize authentication state
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_token" not in st.session_state:
    st.session_state.user_token = None
```

The `require_auth()` function ensures users are logged in before accessing protected pages:

```python
def require_auth():
    """Require authentication to access a page"""
    init_auth_state()
    if not st.session_state.user_authenticated:
        st.warning("Please log in to access this page")
        login_form()
        st.stop()  # Stop execution if not authenticated
```

### API Communication

The frontend communicates with the backend using simple utility functions:

```python
def api_get(endpoint, params=None):
    """Make a GET request to the API with authentication"""
    try:
        response = requests.get(
            f"{get_api_url()}{endpoint}",
            params=params,
            headers=get_auth_header()
        )
        return response.json(), response.status_code
    except Exception as e:
        st.error(f"API error: {str(e)}")
        return {"error": str(e)}, 500
```

## Usage Example

To protect a Streamlit page:

```python
# At the top of your Streamlit page
from frontend.components.authentication import require_auth

# Check authentication
require_auth()

# Rest of the page code (only executed if user is authenticated)
st.title("Protected Page")
```

To make authenticated API requests:

```python
from frontend.utils.api import api_get

# Get user profile
profile_data, status_code = api_get("/api/auth/user")
if status_code == 200:
    st.write(f"Welcome, {profile_data['username']}!")
```

## Security Considerations

1. **JWT Secret Key**: Ensure the `SECRET_KEY` in settings is properly secured and not hardcoded
2. **Token Expiration**: JWT tokens have a configurable expiration time
3. **Password Hashing**: Passwords are hashed with bcrypt before storage
4. **HTTPS**: In production, all communication should be over HTTPS
5. **Cross-Origin Requests**: CORS is configured to allow only specific origins

## Future Improvements

1. **Email Verification**: Add email verification during registration
2. **Password Reset**: Implement password reset functionality
3. **OAuth Integration**: Add support for Google, GitHub, etc. login
4. **Role-Based Access Control**: Add user roles and permissions
5. **Refresh Tokens**: Implement token refresh for longer sessions