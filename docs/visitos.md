
# Ducomentation App Visitors
Visitors are a crucial component of any website or application project, enabling the recording and tracking of user visits and the processing of associated data. Through the Visitors application, the system can gather information about visits, visitor activities, and analyze their behavior, which helps improve performance and user experience.

This document will clearly and systematically document the Visitors application endpoints to facilitate the recording, tracking, and management of visitor data within the project.

## Register & Track New Visitor
The process of registering or tracking a new visitor is automatic and simple, requiring no data entry or button clicks. Once a user logs into the site or submits a visit request to their designated Endpoints, the system automatically generates a unique code for each user to register as a new visitor and links all their future visits to this code.

If the same user returns, the system checks if they are already registered. If 24 hours have passed since their last visit, a new visit is recorded instead of updating the old record, ensuring that each visit is accurately and separately accounted for.
````bash
    GET : api/visitors/track/
    Response : 
        {
            "success": Boolean
            "visitor": {
                "id": String(uuid) # "id": "c41c7863-4256-4c4b-9ffa-c577768d8754"
                "key": String(key) # "92e200046cd492ec4efc25293cf2e4e71e9192e7f6014baa0605b55566c68481"
                "ip_address": String(ip) # 453.654.8677.567
                "device_type": String   # Desktop
                "browser_agent": String # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "browser": String  # Chrome
                "country": String   # morrocco
                "first_visit": DataeTime
                "last_visit": DateTime
            },
            "is_new_visitor": Boolean    # if are new visitor retuen her True if not return False
            "is_new_visit": Boolean    # if is new visit retuen her True if not return False
        }
````

## Fetch all visitors in admin panel
This endpoint is dedicated to displaying a list of all visitors registered in the database. This process is only relevant to users with platform access privileges, allowing them to securely and systematically retrieve (Fetch) all visitors via dedicated endpoints, ensuring that important data is displayed without affecting the privileges or privacy of other users.
````bash
    GET : api/ad/visitors/
    Response : 
        {
            "count": Integer
            "next": String(url)
            "previous": String(url)
            "results":[{
                "id": Stringuuid(uuid)
                "ip_address": String(ip)
                "browser_agent": String
                "browser": String
                "device_type": String
                "country": String
                "first_visit": DateTime
                "last_visit": DateTime
                "visits":[
                    {
                        "id": String(uuid)
                        "page_url": String(url)
                        "page_title": String
                        "referrer": String(URL)
                        "visit_time": DataeTime
                        "visit_date": Date
                        "visitor": String(uuid)
                    }....]
                }....]
        }
````

## Fetch Signal Visitor 
This endpoint is dedicated to displaying data for a specific visitor, including all associated visits. Access to this endpoint is restricted to authorized users, who can only view the information if they have the appropriate permissions, ensuring security and control over access to sensitive data.
````bash
    GET : api/ad/visitors/
    Response : 
        {
            "id": Stringuuid(uuid)
            "ip_address": String(ip)
            "browser_agent": String
            "browser": String
            "device_type": String
            "country": String
            "first_visit": DateTime
            "last_visit": DateTime
            "visits":[
                {
                    "id": String(uuid)
                    "page_url": String(url)
                    "page_title": String
                    "referrer": String(URL)
                    "visit_time": DataeTime
                    "visit_date": Date
                    "visitor": String(uuid)
                }....]
            }
        }
````

## Deelete Visitor
This point is dedicated to displaying information for a specific visitor, and access to it is permitted only to authorized users who have been granted direct permission, to ensure full control over security and protection of visitor data.
````bash
    DELETE : api/ad/visitors/<uuid:pk>/delete/
````

