
## Authentication and Permissions System
The Property Management System relies on a secure authentication mechanism to verify user identity and grant appropriate permissions after successful login. This system ensures the protection of sensitive endpoints and prevents unauthorized access, allowing only authenticated users to perform interactions and operations within the system.

### How it Works
Users are verified via their **phone** number and **password**. Upon successful authentication, the user receives JWT tokens that allow them to browse other protected endpoints and perform only authorized interactions.

### Phone Number Authentication
Authentication in this system is dedicated to using the **phone** & **number** as the primary identifier, simplifying the login process and enhancing system reliability and security.

### Endpoints
````bash
   POST : api/auth/token/
````
This endpoint implements the Django REST Framework's JWT authentication system. It receives the **phone** number and **password** and returns the access token and refresh token to protect the other endpoints.

````bash
    POST : api/auth/login/
````
This endpoint is dedicated to login. It receives the phone number and password and returns the user's basic credentials along with the access and refresh tokens.



