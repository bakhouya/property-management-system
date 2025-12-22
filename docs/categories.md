# Documenting the Categories application paths
No project is complete without categories, whether simple or complex. In our project, we implemented three layers of categories to achieve greater organizational flexibility. This document will outline the role and implementation paths of Categories within the system.

## Category types
Category Types are general classifications that form the core of the project concept. In this system, they indicate the type of transaction associated with the property, where each property is intended for either sale or rent.

### Basic structure data json category type
````bash
"id": String(uuid)
"title": String
"description": String
"image": String(url)
"status": Boolean
"created_at": DateTime
"updated_at": DateTime
````

### Fetch All List Category Type 
This endpoint is used to fetch all Category Types and returns a complete list of available types.
Access is protected by an authentication and permissions system and is restricted to authorized administrative users to ensure data protection and access control.
````bash
    GET : api/ad/categories/types/
    Response :
        {
            "pagination":{
                "next": String(url)
                "previous": String(url)
                "count": Integer
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
                },
            "results":[{
                "sub_categories_count": Integer
                "properties_count": Integer
                # Basic structure data json category type
                }...]
        }
````
### Create A New Category Type
This path is for creating a new Category Type, and the request body will contain the following fields:
**title**, **description**, **image**, **status**.
This path is protected by an authentication and **authorization** system and can only be accessed by users who have **permission** to add Category Types.
````bash
    POST : api/ad/categories/types/create/
    Body :
        {
            "title": String
            "description": String
            "image": String(url)
            "status": Boolean
        }
    Response :
        {
            # Basic structure data json category type
        }
````
### Fetch Signal Category Type
This path is for fetching a single item (Single Category Type) and displaying its full details, and is only available to authorized administrative users, to ensure control over access to category data.
````bash
    GET : api/ad/categories/types/<uuid:pk>/
    Response :
        {
            "sub_categories_count": Integer
            "properties_count": Integer
            # Basic structure data json category type
        }
````
### Update Category Type
This endpoint is used to update the data of a specific Category Type item.
It accepts any of the following fields in the body: title, description, status, and image.
Editing is performed using PUT or PATCH.
After updating, it returns the updated data for the item.
The path is protected by an authentication system and restricted to users with Update privileges to ensure data security and access control.
````bash
    PUT | PATCH : api/ad/categories/types/<uuid:pk>/update/
    Body :
        {
            "title": String
            "description": String
            "image": String(url)
            "status": Boolean
        }
    Response :
        {
            # Basic structure data json category type
        }
````
### Delete Category Type
This endpoint is used to delete an item of a Category Type from the database.
The path is protected by an authentication and authorization system and can only be accessed by users with Delete privileges to ensure data security and system protection.
````bash
    DELETE : api/ad/categories/types/<uuid:pk>/delete/
````
### Endpoint Clients fetch list and signal category type
````bash
    GET : api/categories/types/
    GET : api/categories/types/<uuid:pk>/
````

## Main Categorories
Main Categories represent the second layer of classifications in the project, and refer to the basic categories that divide properties according to their nature, such as: residential units, commercial units, private units, to facilitate the organization and display of properties according to clear classifications.

### Basic structure data json Main Category
````bash
"id": String(uuid)
"title": String
"description": String
"image": String(url)
"status": Boolean
"created_at": DateTime
"updated_at": DateTime
````
### Fetch All Main Categories
````bash
    GET : api/ad/categories/main/
    Response :
        {
            "pagination":{
                "next": String(url)
                "previous": String(url)
                "count": Integer
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
                },
            "results":[{
                "sub_categories_count": Integer
                "properties_count": Integer
                # Basic structure data json main category 
                }...]
        }
````
### Create A New Main Category
This path is for creating a new Main Category, and the request body will contain the following fields:
**title**, **description**, **image**, **status**.
This path is protected by an authentication and **authorization** system and can only be accessed by users who have **permission** to add Category Types.
````bash
    POST : api/ad/categories/main/create/
    Body :
        {
            "title": String
            "description": String
            "image": String(url)
            "status": Boolean
        }
    Response :
        {
            # Basic structure data json main category 
        }
````
### Fetch Signal Main Category
This path is for fetching a single item (Single Main Category) and displaying its full details, and is only available to authorized administrative users, to ensure control over access to category data.
````bash
    GET : api/ad/categories/main/<uuid:pk>/
    Response :
        {
            "sub_categories_count": Integer
            "properties_count": Integer
            # Basic structure data json main category 
        }
````
### Update Main Category
This endpoint is used to update the data of a specific main category item.
It accepts any of the following fields in the body: title, description, status, and image.
Editing is performed using PUT or PATCH.
After updating, it returns the updated data for the item.
The path is protected by an authentication system and restricted to users with Update privileges to ensure data security and access control.
````bash
    PUT | PATCH : api/ad/categories/main/<uuid:pk>/update/
    Body :
        {
            "title": String
            "description": String
            "image": String(url)
            "status": Boolean
        }
    Response :
        {
            # Basic structure data json main category
        }
````

### Delete Main Category 
This endpoint is used to delete an item of a Main Category from the database.
The path is protected by an authentication and authorization system and can only be accessed by users with Delete privileges to ensure data security and system protection.
````bash
    DELETE : api/ad/categories/main/<uuid:pk>/delete/
````
### Endpoint Clients fetch list and signal Main category 
````bash
    GET : api/categories/main/
    GET : api/categories/main/<uuid:pk>/
````

## Sub Categories
Sub Categories represent the third and final layer of classifications in the system. These are subcategories that divide properties according to type, such as: apartments, villas, buildings, private lands, to provide more precise organization and facilitate searching and filtering within the platform.

### Basic structure data json Sub Category
````bash
"id": String(uuid)
"main": String(uuid) # ket main category
"title": String
"description": String
"image": String(url)
"status": Boolean
"created_at": DateTime
"updated_at": DateTime
"types": Array[]
````
### Fetch All List Category Type 
This endpoint is used to fetch all sub Category and returns a complete list of available types.
Access is protected by an authentication and permissions system and is restricted to authorized administrative users to ensure data protection and access control.
````bash
    GET : api/ad/categories/sub/
    Response :
        {
            "pagination":{
                "next": String(url)
                "previous": String(url)
                "count": Integer
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
                },
            "results":[{
                "properties_count": Integer
                # Basic structure data json category type
                }...]
        }
````
### Create A New Sub Category
This path is for creating a new Sub Category, and the request body will contain the following fields:
**title**, **description**, **image**, **status**,  **main**, **types**.
This path is protected by an authentication and **authorization** system and can only be accessed by users who have **permission** to add Category Types.
````bash
    POST : api/ad/categories/sub/create/
    Body :
        {
            "title": String
            "description": String
            "image": String(url)
            "status": Boolean
            "main": String(uuid) # id main category
            "types": Array[] # ids categories types
        }
    Response :
        {
            # Basic structure data json sub category
        }
````
### Fetch Signal Sub Category
This path is for fetching a single item (Single sub Category) and displaying its full details, and is only available to authorized administrative users, to ensure control over access to category data.
````bash
    GET : api/ad/categories/sub/<uuid:pk>/
    Response :
        {
            "properties_count": Integer
            # Basic structure data json sub category 
        }
````
### Update Sub Category
This endpoint is used to update the data of a specific Sub category item.
It accepts any of the following fields in the body: title, description, status, and image.
Editing is performed using PUT or PATCH.
After updating, it returns the updated data for the item.
The path is protected by an authentication system and restricted to users with Update privileges to ensure data security and access control.
````bash
    PUT | PATCH : api/ad/categories/sub/<uuid:pk>/update/
    Body :
        {
            "title": String
            "description": String
            "image": String(url)
            "status": Boolean
            "main": String(uuid)
            "types": Array[]
        }
    Response :
        {
            # Basic structure data json sub category
        }
````

### Delete Sub Category 
This endpoint is used to delete an item of a Sub Category from the database.
The path is protected by an authentication and authorization system and can only be accessed by users with Delete privileges to ensure data security and system protection.
````bash
    DELETE : api/ad/categories/sub/<uuid:pk>/delete/
````
### Endpoint Clients fetch list and signal Sub category 
````bash
    GET : api/categories/sub/
    GET : api/categories/sub/<uuid:pk>/
````

### Fetch all sub categories by main and types relationship
````bash
    GET : api/types/<uuid:type_id>/main/<uuid:main_id>/sub/all/
````





















