# Property Management System

**Property Management System** is a professional project built using **Django REST Framework** to provide a robust platform for property management and services, with a flexible and scalable API for future uses such as web or mobile applications.

## Project Concept
The platform aims to:
- Manage properties completely (CRUD).
- Support user-property interactions (likes, favorites, comments).
- Organize multiple categories (type, main, sub).
- Enable different permissions (Admin/Users) for resource control.
- Ensure secure access and data management.

## Technologies Used
- Python
- Django
- Django REST Framework
- Django Filters
- JWT Authentication
- PostgreSQL (or any supported database)
- PIP/Pipenv for package management



## Installation (Local Setup)
> Make sure you have Python and Pipenv installed

````bash
    git clone https://github.com/bakhouya/property-management-system.git
    cd property-management-system
    pipenv shell
    pipenv install -r requirements.txt
````
## Production API URL 
````bash
    https://bamoos.pythonanywhere.com/api/
````
## Ducomentations Endpoints apps
| Method                            | Description | 
| :---------------------------------| :---------- | 
| [Auth](docs/auth.md)              | The Auth.md file briefly documents authentication endpoints, such as custom login and the use of JWT Token to protect the API and verify user identity. |
| [Accounts](docs/accounts.md)      | accounts.md is a file that documents user endpoints such as registration and profile management in a concise and clear manner |
| [Groups](docs/roles.md)           | Groups.md is a file that documents the application endpoints for roles and permissions in a concise and clear manner. |
| [Properties](docs/properties.md)  | properties.md is a file that documents the application's property endpoints, such as price types, the properties themselves, and comments, in a concise and clear manner. |
| [Visitors](docs/visitos.md)       | visitors.md is a file that documents visitor access points and their visits in a concise and clear manner. |
| [Settings](docs/settings.md)      | settings.md is a file that documents the application's settings endpoints in a concise and organized manner. |
| [Categories](docs/categories.md)  | scategories.md is a file that documents the application's categories endpoints in a concise and organized manner. |
| [Chat](docs/chat.md)              | chat.md is a file that documents the application's Chat endpoints in a concise and organized manner. |
| [Analytics](docs/analytics.md)    | analytics.md is a file that documents the application's Analytics endpoints in a concise and organized manner. |
