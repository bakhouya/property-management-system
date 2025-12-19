
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





