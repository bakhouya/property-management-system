



### Fetch All User In admin panel 
This path is used to display a list of all users within the system. It is a protected path that can only be accessed after successful authentication using JWT and with administrative privileges. It does not accept any input and returns a list of users containing their basic data, enabling administrators to track and control accounts.
````bash
    GET : ad/users/
````

### Create New User
This path is used by the administrator to create a new user after verifying authentication and permissions. It receives user data such as **phone** , **password**, **confirm_password** , **username**, **email** , **first_name**, **last_name** , **groups**  and returns the successfully created user's data, allowing for the addition of new accounts in an organized and secure manner.
````bash
    POST : ad/user/new/
    Body :  application/json
        {
            "id": String(uuid)
            "username": String
            "email": String(email)
            "phone": String
            "first_name": String
            "last_name": String
            "is_active": Boolean
            "avatar": String(URL)
            "groups": Array[],
        }
    Response : 
        {
            "id": String(uuid)
            "username": String
            "email": String(email)
            "phone": String
            "first_name": String
            "last_name": String
            "account_type": String
            "is_active": Boolean
            "is_staff": Boolean
            "avatar": String(URL)
            "groups": Array[],
            "permissions": Array[],
        }
````

### Delete User
This path is used to **delete** a specific user based on their unique identifier. It requires JWT authentication and administrative privileges, accepts only the user ID, thus protecting the system from unauthorized deletion.
````bash
    DELETE : ad/user/uuid:pk/delete/
````

### Update User from admin panel 
This path allows the administrator to modify the data of a specific user after verifying their permissions. It receives the user ID and the fields to be updated, and returns the modified user data, allowing information to be updated while maintaining system security.
````bash
    PUT | PATCH : ad/user/uuid:pk/update/
    Response : 
        "data":
            {
                "id": String(uuid)
                "username": String
                "email": String(email)
                "phone": String
                "first_name": String
                "last_name": String
                "account_type": String
                "is_active": Boolean
                "is_staff": Boolean
                "avatar": String(URL)
                "groups": Array[],
                "permissions": Array[],
            }
````

### Fetch data User By pk 
This path is used to display the complete details of a specific user within the system. It is user-based and requires authentication and administrative privileges, returning all data associated with the account, thus facilitating monitoring and management.
````bash
    GET : ad/user/uuid:pk/
    Response : 
        "data":
            {
                "id": String(uuid)
                "username": String
                "email": String(email)
                "phone": String
                "first_name": String
                "last_name": String
                "account_type": String
                "is_active": Boolean
                "is_staff": Boolean
                "avatar": String(URL)
                "groups": Array[],
                "permissions": Array[],
            }
````

### Chnage status User from admin panel
This path is used to change a user's account status (True or False). It accepts only the user ID, returns the new account status after the operation, and is used to control user access without deleting their accounts.
````bash
    PATCH : ad/user/uuid:pk/change-status/
    Response : 
        "data":
            {
                "id": String(uuid)
                "username": String
                "email": String(email)
                "phone": String
                "first_name": String
                "last_name": String
                "account_type": String
                "is_active": Boolean
                "is_staff": Boolean
                "avatar": String(URL)
                "groups": Array[],
                "permissions": Array[],
            }
````

### Register A personal User (Clients)
This path is used to automatically register a new user within the system. It receives the **phone** , **password**, **confirm_password** , **username**, **email** , **first_name**, **last_name**, and returns the data of the successfully registered user. Auth codes may be included depending on the system configuration.
````bash
    POST : accounts/register/
    Body : application/json
        {
            "username": String
            "email": String(email)
            "phone": String
            "first_name": String
            "last_name": String 
            "password": String
            "is_active": String
            "confirm_password": String
            "visitor": String(uuid)
        }
    Response : 
        {
            "data": {
                "user": {
                    "id": String(uuid)
                    "username": String
                    "email": String(email)
                    "phone": String
                    "avatar": String(URL)
                    "first_name": String
                    "last_name": String
                    "account_type": String
                    "is_staff": Boolean,
                    "is_active": Boolean,
                    "visitor": String(uuid)
                    "created_at": String(datatime)
                    "updated_at": String(datatime)
                },
                "tokens": {
                    "refresh": String(token)
                    "access": String(token)
                }
            }
        }
````

### fatche data user & updated 
This path allows the authenticated user to view or update their profile. It is accessible only after successful authentication and returns the current or updated profile data, allowing the user to securely manage their personal information.
````bash
    GET | PUT | PATCH : accounts/profile/

    Body | Response : 
    {
        "data":{
            "id": String(uuid)
            "username": String
            "email": String(email)
            "phone": String
            "first_name": String
            "last_name": String
            "avatar": String(URL)
            "account_type": String
            "is_active": Boolean
            "is_staff": Boolean
            "groups_info": Array[],
            "permissions": Array[],
            "created_at": String(datatime)
            "updated_at": String(datatime)
        }
    }
````

















