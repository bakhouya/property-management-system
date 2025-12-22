
## Roles & Permissions App Documentation
The Roles & Permissions app is responsible for managing permissions and groups within the system. All paths are protected and require JWT authentication and administrative privileges.

### Fetch All Permissions
displays a list of all available permissions within the system. It requires no input and returns a list of permissions, enabling the administrator to see all applicable permissions.
````bash
    GET : api/ad/permissions/
````

### Fetch All Groups (Roles)
Displays a list of all groups (Roles) in the system. Relies on JWT authentication and administrator privileges, and returns a list of groups with brief details for each.
 
````bash
    GET : api/ad/groups/
````

### Create New Group (Role)
This path is used to create a new group. It receives group data (name, description, and associated privileges), returns the group data after creation, and allows the administrator to add new roles in an organized and secure manner.
````bash
    POST : api/ad/groups/create/
    Body :
        {
            "name": String
            "permissions": Array(id, String)
        }
    Response :
        {
            "data":{
            "id": Integer
            "name": String
            "permissions": Array()
            "permissions_count": Integer
            "users_count": Integer
            }
        }
````

### Fetch A Signal Group (Role)
Displays details of a specific group based on its ID. Requires authentication and administrative permissions, and returns detailed information about the group, including the permissions applied to it.
````bash
    GET : api/ad/groups/int:id/
    Response :
        {
            "data":{
            "id": Integer
            "name": String
            "permissions": Array()
            "permissions_count": Integer
            "users_count": Integer
            }
        }
````

### Update Group (Role)
This path allows modification of a specific group's data. It receives the group ID and the fields to be modified, and returns the updated group data, allowing for secure modification of permissions or the group name.
````bash
    PUT | PATCH : api/ad/groups/int:id/update/
    Body :
        {
            "name": String
            "permissions": Array(id, String)
        }
    Response :
        {
            "data":{
            "id": Integer
            "name": String
            "permissions": Array()
            "permissions_count": Integer
            "users_count": Integer
            }
        }
````

### Delete Group (Role)
This is used to delete a specific group from the system. It receives the group ID, while maintaining system security and preventing unauthorized deletion.
````bash
    DELETE : api/ad/groups/int:id/delete/
````


### General Note
All paths are protected by the JWT system and the user must be authenticated and have appropriate permissions, to ensure that any modification or display of groups and permissions is done in a secure and orderly manner.









