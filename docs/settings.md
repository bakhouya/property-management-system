
# Ducomentation App Settings
Any website typically contains numerous settings, ranging from simple to complex, to customize the platform's appearance and functionality.
In our Property Management System project, we need to implement a Settings application to manage key settings, such as:
##### General Platform Settings: Logo, Title, Description
##### Security Settings
##### SEO Settings
##### Forms/Q&A Settings
##### Media Settings
##### Cities/Locations
##### User-specific Settings

This document will outline the most important endpoints related to these settings, demonstrating how to manage and configure the system in a structured and seamless manner.

## fetch & Update  platform Settings
The Platform Settings endpoint is dedicated to managing essential platform data such as the **logo**, **title**, and **description**.
This endpoint performs the following functions:
**GET**: Fetches the current platform settings data.
**PUT/PATCH**: Updates this data as needed.
Access to this endpoint is restricted to authorized users to ensure data security and protection. It is a critical endpoint within the system.
````bash
    GET | PUT | PATCH : api/ad/settings/platform/
    Respnse : 
        {"data":
            {
                "id": String(uuid)
                "dark_logo": String(url)
                "light_logo": String(url)
                "favicon": String(url)
                "title": String
                "description": String
                "contact_email": String(email)
                "support_email": String(email)
                "phone": String(phone)
                "timezone": String(TIMEZONE)
                "currency": String
                "currency_symbol": String
                "maintenance_mode": Boolean
                "allow_registration": Boolean
                "updated_at": DateTime
            }
        }
````

## Fetch & Update Social Media 
This endpoint is dedicated to managing social media data:
**GET**: To fetch current social media data.
**PUT/PATCH**: To update this data as needed.
Access is restricted to authorized users to ensure platform security and protect sensitive information.
````bash
    GET | PUT | PATCH : api/ad/settings/socialmedia/
    Respnse : 
        {"data":
            {
                "id": String(uuid)
                "facebook": String(Url)
                "whatsapp": String(Url)
                "twitter": String(Url)
                "instagram": String(Url)
                "linkedin": String(Url)
                "tiktok": String(Url)
                "telegram": String(Url)
                "youtube": String(Url)
                "updated_at": DateTime
            }
        }
````

## Fetch & Update Seo Settings
This endpoint is dedicated to managing search engine optimization (**SEO**) data, where you can:
**GET**: Fetch current SEO settings.
**PUT/PATCH**: Update these settings as needed.
Access is restricted to authorized users to ensure the security and protection of platform data.
````bash
    GET | PUT | PATCH : api/ad/settings/seo/
    Respnse : 
        {"data":
            {
                "id": String(uuid)
                "title": String
                "description": String
                "keywords": String
                "google_analytics_id": String(id)
                "facebook_pixel_id": String(id)
                "tiktok_pixel_id": String(id)
                "updated_at": DateTime
            }
        }
````

## Fetch & Update Security Settings
This endpoint is used to manage security settings data, where you can:
**GET**: Fetch the current security settings.
**PUT**: Update these settings as needed.
Security settings consist of:
`enable_cors (Boolean):` Specifies whether the site allows all sites to access the platform's API.
`allowed_cors (String List):` A list of sites allowed to access the API when `enable_cors = false` is enabled.
Access to this endpoint is restricted to authorized users to ensure platform security and data protection.
````bash
    GET | PUT | PATCH : api/ad/settings/security/
    Respnse : 
        {"data":
            {
                "id": String(uuid)
                "enable_cors": Boolean
                "allowed_cors": String
                "updated_at": DateTime
            }
        }
````

## Fetch All Settings 
This endpoint is dedicated to displaying all the platform's general settings at once, allowing for organized and customized browsing on the website.
Access to this endpoint is restricted to authorized users to ensure data security and protect platform settings. It is a critical endpoint within the system.
````bash
    GET : api/settings/
    Respnse : 
        {"data":
        {
            "platform":
            {
                "id": String(uuid)
                "dark_logo": String(url)
                "light_logo": String(url)
                "favicon": String(url)
                "title": String
                "description": String
                "contact_email": String
                "support_email": String(email)
                "phone": String
                "timezone": String(timezone)
                "currency": String
                "currency_symbol": String
                "maintenance_mode": Boolean
                "allow_registration": Boomean
                "updated_at": DateTime
            }
            "social_media":[{
                    "id": String
                    "name": String
                    "url": String(url)
                    "icon_class": String # "fab fa-facebook"
                }...],
            "seo_data":{
                "id": String(uuid)
                "title": String
                "description": String
                "keywords": String
                "google_analytics_id": String(id)
                "facebook_pixel_id": String(id)
                "tiktok_pixel_id": String(id)
                "updated_at": DateTime
            }
        }}
````

## GRUD Cities 
Cities are a fundamental part of our project, given their pivotal role in classifying and allocating real estate. For this purpose, a single URL within the CRUD system has been adopted, encompassing all city management operations: **GET** (to retrieve data), **POST** (to add), **PUT** (to update), and **DELETE** (to delete), thus organizing city processing within the system clearly and efficiently.
````bash
    GET | PUT | PATCH | POST | DELETE : api/ad/cities/
    Body : 
        {
            "name" : String
            "status" : Boolean
        }
    Respnse : 
        {"data":
            {
                "id": String(uuid)
                "name": String
                "status": Boolean
                "created_at": DateTime
                "updated_at": DateTime
            }
        }
````

## Fetch Settings User (myself)
To achieve greater flexibility in our project, we've created custom settings for each user, especially for clients such as property owners and property seekers, enabling them to control certain communication settings.
This endpoint allows each user to:
**GET**: Import their own settings.
**PUT**: Update these settings as needed.
This is all done within a secure framework that ensures each user can only access their own personal settings.
````bash
    GET | PUT  : api/settings/mysettings/
    Respnse : 
        {"data":
            {
                "id": String(uuid)
                "contact_whatsapp": Boolean
                "number_whatsapp": String
                "contact_vocal": Boolean
                "number_vocal": String
                "contact_email": Boolean
                "show_profile": Boolean
                "show_contact_info": Boolean
                "user" : String(uuid)
                "created_at" : DateTime
                "updated_at" : DateTime
            }
        }
````

## Fetch settings User in admin panel 
To ensure complete control within the Admin Panel regarding user settings, dedicated endpoints have been provided for administrators, enabling them to:
Fetch a list of all user settings
Fetch the settings of a specific user
Modify these settings within defined permissions and limits
Access to these endpoints is restricted to administrative users only, with clear modification restrictions in place to maintain system security and prevent any unauthorized changes.
````bash
    GET | PUT  : api/ad/settings/user/<uuid:user_id>/
    GET | PUT  : api/ad/settings/usersettings/ 
````




