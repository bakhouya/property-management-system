
## Authentication and Permissions System
The Property Management System relies on a secure authentication mechanism to verify user identity and grant appropriate permissions after successful login. This system ensures the protection of sensitive endpoints and prevents unauthorized access, allowing only authenticated users to perform interactions and operations within the system.

### How it Works
Users are verified via their **phone** number and **password**. Upon successful authentication, the user receives JWT tokens that allow them to browse other protected endpoints and perform only authorized interactions.

### Phone Number Authentication
Authentication in this system is dedicated to using the **phone** & **number** as the primary identifier, simplifying the login process and enhancing system reliability and security.

### Endpoints

### Default Auth JWT
This endpoint implements the Django REST Framework's JWT authentication system. It receives the **phone** number and **password** and returns the access token and refresh token to protect the other endpoints.
````bash
   POST : api/auth/token/
   Body : application/json 
        {
            "phone": String ,  # 0612975634
            "password": String  # test@gmail
        }
    Response:
        {
            "refresh": String(token),
            "access": String(token),
        }
````

### Custom Auth 
This endpoint is dedicated to login. It receives the phone number and password and returns the user's basic credentials along with the access and refresh tokens.
````bash
    POST : api/auth/login/
    Body : application/json 
        {
            "phone": String 
            "password": String 
        }
    Response:
        {
            "refresh": String(token)
            "access": String(token)
            "user":{
                "id": String(uuid)
                "username": String
                "email": String(email)
                "phone": String
                "first_name": String
                "last_name": String 
                "account_type": String
                "is_active": Boolean
                "is_blocked": Boolean
                "groups": Array[]
                "permissions": Array[]
            }
        }
````

## Refrash Token 
Refresh Token 

````bash
    POST :  api/auth/refresh/
    Body : application/json 
        {
            "refresh": String(token)
        }
    Response 
        {
            "access": String(token)
        }
````

