

# Properties & Price Types App Documentation
The Properties & Price Types app is responsible for managing price types, properties, and comments within the system. All paths are protected and require JWT authentication, with appropriate permissions applied to both administrators and regular users.

## Price Types (Admin)
### Fetch All List Price Type
Displays a list of all price types within the system. It requires no input and returns a list of price types.
````bash
    GET : api/ad/price-types/
    Response : 
        {
            "pagination":{
                "next": String(URL)
                "previous": String(URL)
                "count": Integer,
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
            }
            "results":[{
                id: String(uuid)
                "name": String
                "description": String
                status: Boolean
                created_at: DateTime
                updated_at: DateTime
            }...]
           
        }
````

### Fetch All Active Price Type
Displays a list of active types only and is used to display available price types.
````bash
    POST : api/ad/price-types/active/
    Response :
    #   Some thing in Fetch All List
````

### Create New Price Type
Used to create a new price type. It receives the **name** & ***description** and returns the data after creation.
````bash
    POST : api/ad/price-types/create/
    Body :
        {
           "name": String
            "description": String
        }
    Response :
        {
            id: String(uuid)
            "name": String
            "description": String
            status: Boolean
            created_at: DateTime
            updated_at: DateTime
        }
````
### Fetch Item Price Type 
Displays details of a specific price type based on its identifier.
````bash
    GET : api/ad/price-types/uuid:pk/
    Response :
        {
            id: String(uuid)
            "name": String
            "description": String
            status: Boolean
            created_at: DateTime
            updated_at: DateTime
        }
````

### Update Price Type
Allows modification of data for a specific price type. It receives the fields to be modified and returns the type data after the update.
````bash
    PUT | PATCH : api/ad/price-types/uuid:pk/update/
    Body :
        {
           "name": String
            "description": String
        }
    Response :
        {
            id: String(uuid)
            "name": String
            "description": String
            status: Boolean
            created_at: DateTime
            updated_at: DateTime
        }
````

### Delete Price Type
Used to delete a specific price type 
````bash
    DELETE : api/ad/price-types/uuid:pk/delete/
````



## Properties & Comments (Admin)
### Property Object Schema & Response Structure
````bash
    id: String(uuid)
    "title": String
    "description": String
    "city": String(uuid)
    "address": String
    "area": String
    "is_owner": Boolean
    "price": String
    "price_type": String(uuid)
    "status": Boolean
    "is_blocked": Bollean
    "views_count": Integer
    "likes_count": Integer
    "comments_count": Integer
    "created_at": DateTime
    "images": Array(String(URL))
    "user":{  "id": String(uuid), "username": String, "avatar": String(Image) }
    "category_type":{ "id":  String(uuid), "title": String }
    "main_category":{ "id":  String(uuid), "title": String }
    "sub_category":{ "id":  String(uuid), "title": String }
````

### Fteching All Active Properties & Not Blocked
This API is a public and open window for browsing available properties. It is specifically designed to fetch and display a comprehensive list of all active and reliable real estate units that meet the ideal display criteria (status active and not blocked). It is available for public access without the need for identity verification, ensuring that real estate content and its precise details are displayed to all visitors and potential clients with complete clarity and transparency.
````bash
    GET : api/ad/properties/
    Response : 
        {
            "pagination":{
                "next": String(URL)
                "previous": String(URL)
                "count": Integer, # Count Items 
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
            }
            "results":[{
                #  Property Object Schema & Response Structure 

            }...]
            
        }
````

### Create New Property
This API represents the exclusive gateway dedicated to enabling individual users to list their new properties on the platform. It imposes a strict identity verification system that requires prior login to ensure the security of operations. The interface receives the basic data of the property, such as the address and description, via a POST request. Upon successful completion of the process, it creates the property record and restructures the complete data of the newly created property, providing the user with immediate and accurate confirmation of the quality and completeness of their listing.
````bash
    POST : api/properties/create/
    Body : 
        {
            "title": String
            "description": String
            "category_type": String(uuid)
            "main_category": String(uuid)
            "sub_category": String(uuid)
            "city": String(uuuid)
            "address": String
            "area": Damicel
            "price": Integer
            "price_type": String(uuid)
            "images": Array(File)
        }
    Response :
        {
           # Property Object Schema & Response Structure
        }
````

### Fetching A Signal Item Property 
This software interface is dedicated to retrieving detailed data for a specific property, operating via the GET protocol to provide a complete and comprehensive file of the required item. The interface not only displays the technical and spatial specifications of the property, but also extends to include the record of comments associated with it and all related interactions, allowing the user to have a panoramic view that combines the property's characteristics with the opinions and questions of interested parties in one integrated graphic response.
````bash
    GET : api/properties/<uuid:pk>/
    Response :
        {
           # Property Object Schema & Response Structure
           "comments":[
                {
                    "id": String(uuid)
                    "user":{
                        "id": String(uuid)
                        "username": String
                        "avatar": String(URL)
                    },
                    "property": String(uuid)
                    "comment": String
                    "parent": String(uuid) 
                    "status": Boolean
                    "replies":[
                        {
                            "id": String(uuid)
                            "user":{
                                "id": String(uuid)
                                "username": String
                                "avatar": String(url)
                            },
                        "property": String(uuid)
                        "comment": String
                        "parent": String(uuid)
                        "status": Boolean
                        "replies": Array[], # Replies this array should be empty
                        "created_at": DateTime
                        "updated_at": DateTime
                    }],
                    "created_at": DateTime
                    "updated_at": DateTime
                }],
        }
````

### Update Property
This software interface provides a secure and reliable mechanism to enable users to update their existing property data. It is subject to a dual protection protocol that requires first the authentication of the user’s identity, and second the verification of their actual ownership of the property to be modified. The interface receives the data to be changed via a PATCH/PUT request, and upon successful completion of the process, it returns the complete and updated property data, ensuring the accuracy of the information and its real-time conformity with the new modifications made by the owner.
````bash
    PUT | PATCH : api/properties/<uuid:pk>/update/
    Body : 
        {
            "title": String
            "description": String
            "category_type": String(uuid)
            "main_category": String(uuid)
            "sub_category": String(uuid)
            "city": String(uuuid)
            "address": String
            "area": Damicel
            "price": Integer
            "price_type": String(uuid)
            "images": Array(File)
        }
    Response :
        {
           # Property Object Schema & Response Structure
        }
````

### Delete Item Property 
This API is dedicated to completing the final deletion of the property from the database. It is protected by a strict security layer that requires user authentication and firm verification that the user is the actual owner of the targeted property. This process ensures the secure removal of all records associated with the property, and the process is not completed until ownership privileges have been checked to prevent any unauthorized interference with user data.
````bash
    DELETE : api/properties/<uuid:pk>/delete/
````

### Change Status Property 
This API provides a smart mechanism to control the property's display status on the platform, allowing the actual owner to switch the property's status (between active and inactive) by sending a POST request that includes the property's unique ID in the link. This point acts as a secure control key that ensures the user can hide or show their listing at any time, while requiring identity authentication and verification of ownership to ensure that no external parties tamper with the property's display status.
````bash
    POST : api/properties/<uuid:pk>/change-status/
    Response : 
        {
           "message": String
           "status": Boolean # A New status of this property
        }
````

### Toggle Like Action for Property 
This API is dedicated to managing real-time interaction with properties through the "Smart Like" (Like Toggle) system, which allows all registered users to express their interest in the property regardless of their ownership of it. The interface operates with precise reciprocal logic, so if a user sends a request and has previously registered a like, the like is automatically canceled, and if there is no previous like, it is registered immediately, which ensures a dynamic update of interaction statistics and provides an interactive and seamless user experience.
````bash
    POST : api/properties/<uuid:pk>/like/
    Response : 
        {
           "action": String # "like"
           "status": Boolean # if "False" mean remove like count, if "True" mean add Like count
           "count": Integer
        }
````

### Toggle favorite Action for Property 
This API is dedicated to managing the user's "favorite properties" list, allowing them to organize and track properties that interest them through a smart switching mechanism. Once a request is sent for the specified route, the system checks the user's records. If the property is already on their favorites list, it is immediately excluded. If it is not, it is added to the list, providing a flexible and efficient way for users to quickly access their favorite options at any time.
````bash
    POST : api/properties/<uuid:pk>/favorite/
    Response : 
        {
           "action": String # "favorite"
           "status": Boolean # if "False" mean remove favorite count, if "True" mean add favorite count
           "count": Integer
        }
````

### Fetch Properties any User (anothers)
This API is dedicated to viewing a specific user's real estate portfolio, operating according to a smart filtering mechanism based on the inquirer's identity. If the user requests access to their own property list, the API retrieves all their real estate records without exception or restrictions. However, if they request to view another user's properties, it imposes a strict protection system that limits the display of active and publicly available properties only (those with an active and non-blocked status), thus ensuring the preservation of the privacy of data not ready for publication while providing a secure and fully transparent browsing experience for available offers.
````bash
    GET : api/properties/user/<uuid:user_id>/all/
    Response : 
        {
        #   Basic
        }
````

### Fetch Properties For Auth User (myself)
This software interface is dedicated to providing full and direct access for the registered user to their personal real estate inventory, where it acts as a private control panel that retrieves all of their real estate records without exception. This point is distinguished by not imposing any restrictions or filters on the retrieved data, as all properties are displayed regardless of their status (whether active, inactive, or even blocked), giving the user a comprehensive view that enables them to manage and monitor the status of all their real estate listings and accounts with the utmost accuracy and transparency.
````bash
    GET : api/properties/user/properties/
       Response : 
        {
            "pagination":{
                "next": String(URL)
                "previous": String(URL)
                "count": Integer, # Count Items 
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
            }
            "results":[{
                #  Property Object Schema & Response Structure 

            }...]
            
        }
````

### Fetch favorites Properties For Auth User (myself)
This API is dedicated to displaying a specific user's "favorite properties" list, providing access to the collection of offers that the user has previously identified and shown interest in. This point is distinguished by being a channel for retrieving personal interests, as it is not limited to properties owned by the user himself, but includes all properties belonging to other users that have been marked as "favorites," thus providing a complete reference guide that reflects the user's taste and preferred choices within the platform.
````bash
    GET : api/properties/user/favorites/
       Response : 
        {
            "pagination":{
                "next": String(URL)
                "previous": String(URL)
                "count": Integer, # Count Items 
                "total_pages": Integer
                "current_page": Integer
                "page_size": Integer
            }
            "results":[{
                #  Property Object Schema & Response Structure 

            }...]
            
        }
````

### Fetch All Comments by Property Item
This API is dedicated to retrieving all comments associated with a specific property via its unique ID. It adopts a structured and organized display system that arranges interactions in a sequential (JSON) list format. The interface is distinguished by its ability to organizationally separate parent comments from their branched responses (children/nested comments), allowing users to logically and easily track dialogue threads and discussions, and providing developers with a data structure ready to build interactive interfaces that support a multi-level response system.
````bash
    GET : api/properties/<uuid:property_id>/comments/
    Response : 
        {
        "pagination":{
            "next":null,
            "previous":null,
            "count":1,
            "total_pages":1,
            "current_page":1,
            "page_size":10
        },
        "results":[{
            "id": String(uuid)
            "user":{
                "id": String(uuid)
                "username": String
                "avatar": String(URL)
            },
            "property": String(uuid)
            "comment": String
            "parent": String(uuid)
            "status": Boolean
            "replies":[{
                "id": String(uuid)
                "user":{
                    "id": String(uuid)
                    "username": String
                    "avatar": String(url)
                },
                "property": String(uuid)
                "comment": String
                "parent": String(uuid)
                "status": Boolean
                "replies":Array[],
                "created_at": DateTime
                "updated_at": DateTime
            }],
            "created_at": DateTime
            "updated_at": DateTime
        }]
        }
````

### Create Comment
This API is designed to enable users to interact directly with real estate listings by adding new comments. It receives the comment content and the ID of the targeted property in the request body. The API processes the data and links it to the identity of the currently registered user. Upon success, it returns a complete object containing the comment text, timestamp, and the user's identification data, ensuring an immediate update to the discussion thread and providing technical confirmation of the successful completion of the posting process.
````bash
    POST : api/properties/comments/create/
    Body : 
        {
            "comment": String
            "property": String(uuid)
        }
    Response : 
        {
            "id": String(uuid)
            "user":{
                "id": String(uuid)
                "username": String
                "avatar": String(url)
            },
            "property": String(uuid)
            "comment": String
            "parent": String(uuid)
            "status": Boolean
            "replies":Array[],
            "created_at": DateTime
            "updated_at": DateTime
        }
````

### Update Comment
This API is designed to enable users to edit and correct the content of their previous comments, as it imposes a layer of protection that ensures that the right to edit is restricted to the original commenter only. The interface receives the new text to be updated via a PATCH/PUT request, and after verifying the identity and ownership, it updates the comment record and returns the updated data, giving users complete flexibility in managing their textual contributions and interactions while maintaining the accuracy and credibility of the discussions about real estate.

````bash
    PUT | PATCH : api/properties/comments/<uuid:pk>/update/
````

### Delete Comment
This API is dedicated to completing the final deletion of comments, giving users the ability to completely remove their textual contributions from the property records. The interface operates according to strict security standards that ensure that the deletion authority is limited to the original commenter only after verifying their digital identity. When the process is successful, the database is updated and the statistics of comments associated with the property are automatically reset, ensuring that the user's privacy and full control over the content they publish are maintained.
````bash
    DELETE : api/properties/comments/<uuid:pk>/delete/
````










