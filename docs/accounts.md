



A brief explanation of user management paths (accounts)

````bash
    GET : ad/users/
````
This path is used to display a list of all users within the system. It is a protected path that can only be accessed after successful authentication using JWT and with administrative privileges. It does not accept any input and returns a list of users containing their basic data, enabling administrators to track and control accounts.

````bash
    POST : ad/user/new/
````
This path is used by the administrator to create a new user after verifying authentication and permissions. It receives user data such as **phone** , **password**, **confirm_password** , **username**, **email** , **first_name**, **last_name** , **groups**  and returns the successfully created user's data, allowing for the addition of new accounts in an organized and secure manner.

````bash
    DELETE : ad/user/uuid:pk/delete/
````
This path is used to **delete** a specific user based on their unique identifier. It requires JWT authentication and administrative privileges, accepts only the user ID, and returns a message confirming successful deletion, thus protecting the system from unauthorized deletion.

````bash
    PUT | PATCH : ad/user/uuid:pk/update/
````
This path allows the administrator to modify the data of a specific user after verifying their permissions. It receives the user ID and the fields to be updated, and returns the modified user data, allowing information to be updated while maintaining system security.

````bash
    GET : ad/user/uuid:pk/
````
This path is used to display the complete details of a specific user within the system. It is user-based and requires authentication and administrative privileges, returning all data associated with the account, thus facilitating monitoring and management.

````bash
    PATCH : ad/user/uuid:pk/change-status/
````
This path is used to change a user's account status (True or False). It accepts only the user ID, returns the new account status after the operation, and is used to control user access without deleting their accounts.

````bash
    POST : accounts/register/
````
This path is used to automatically register a new user within the system. It receives the **phone** , **password**, **confirm_password** , **username**, **email** , **first_name**, **last_name**, and returns the data of the successfully registered user. Auth codes may be included depending on the system configuration.

````bash
    GET | PUT | PATCH : accounts/profile/
````
This path allows the authenticated user to view or update their profile. It is accessible only after successful authentication and returns the current or updated profile data, allowing the user to securely manage their personal information.
















