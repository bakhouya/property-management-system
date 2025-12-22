# analytics Documentation
Statistics and analytics are essential features for continuously monitoring website traffic and analyzing its performance. This section aims to provide a comprehensive and accurate view of user behavior and their interaction with various system components, contributing to improved overall website performance and informed decision-making based on clear and reliable data.

In the Property Management System project, a dedicated statistics and analytics section was created. Despite its simplicity, it relies on key performance indicators (KPIs) to understand website performance and analyze usage. This section focuses on the most influential aspects that directly contribute to evaluating system effectiveness and enhancing the user experience.

This document outlines the key aspects of the statistics and analytics system used in the project, explaining its role in performance tracking, improving service quality, and supporting future system development.

## Get statistic Source Visitors
This endpoint is used to analyze the sources of traffic to a website, providing accurate data on the channels from which visitors come, whether through direct visits, search engines like Google, or social media platforms like Facebook, TikTok, and others.
This endpoint provides detailed statistics for each source, including:
The total number of visits from each source.
The percentage of each source compared to the total number of visits.
A detailed breakdown showing the distribution of traffic within each source.
This data is crucial for analyzing website performance and understanding user behavior. It also plays a pivotal role in guiding advertising campaigns and making marketing decisions based on accurate and reliable data, contributing to improved return on investment (ROI) and the development of a comprehensive digital marketing strategy for the project.
````bash
    GET : api/analytics/visists/sources/
    Response :
        {
             "detailed_analysis": {
                "direct": {
                    "total": 1, 
                    "percentage": 100.0,
                    "breakdown": {
                        "general": {
                            "visits": 1,
                            "percentage": 100.0
                        }
                    }
                }
                ....
            }
        }
````
## Get Overall Traffic Statistics
This endpoint is used to retrieve general and daily statistics about system traffic, providing a comprehensive overview of overall site activity at a specific time.
This path displays a range of key metrics, including:
Total number of registered users.
Number of users registered today.
Total number of visitors.
Number of visitors today.
Total number of properties listed on the system.
Number of properties added today.
Date and time of creation of the statistic.
These statistics are crucial for monitoring overall site performance, measuring daily system engagement and growth, and enabling platform administrators to make timely, data-driven decisions, improve content management, and track system usage over time.
````bash
    GET : api/dashboard/simple-stats/
    Response :
        {
            "users_count": 0,
            "today_registered_users": 0,
            "all_visitors": 1,
            "today_visitors": 1,
            "all_properties": 0,
            "today_properties": 0,
            "date": "2025-12-22",
            "timestamp": "2025-12-22T14:01:21.189366+00:00"
        }
````
## Get Visitors & Visits Statistics
This endpoint is used to track website visitor statistics and traffic, providing accurate data to help monitor site performance daily.
This endpoint offers a range of key metrics, including:
Total number of visitors.
Total number of visits.
Number of visits recorded today.
Percentage of daily visits compared to total visits.
Date of statistics.
These statistics are essential for analyzing website performance and understanding daily user engagement levels. They also contribute to evaluating platform growth, identifying periods of high activity, and making data-driven optimization decisions.
````bash
    GET : api/stats/visits/
    Response :
        {
            "total_visitors": 1,
            "total_visits": 1,
            "today_visits": 1,
            "today_percentage": 100.0,
            "date": "2025-12-22"
        }
````





