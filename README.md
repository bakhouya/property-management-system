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
    pipenv install -r requierments.txt
````










| Method                            | Description | 
| :---------------------------------| :---------- | 
| [Auth](docs/auth.md)              | The Auth.md file briefly documents authentication endpoints, such as custom login and the use of JWT Token to protect the API and verify user identity. |
| [Accounts](docs/accounts.md)      | Creates a new blog, automatically linking it to the authenticated user via the token. |
| [Groups](docs/roles.md)           | Deletes a specific blog. Only the owner of the blog is authorized to delete it. |
| [Properties](docs/properties.md)  | Updates a specific blog (e.g., incrementing likes). |

