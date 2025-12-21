# Documenting the Chat application paths
In the Property Management System project, a chat and direct communication system between property owners and property seekers is a key feature, allowing any property seeker to communicate directly with the owner to inquire about and negotiate contracts.
To ensure a more flexible and richer experience, this system supports text, images, audio, and video communication.
This document will outline the main endpoints that comprise this system, explaining how to manage the various conversations and messages within the platform.

## Fetch all conversations user
This endpoint is used to fetch all conversations for each user, regardless of whether they are the sender or receiver.
For each conversation, a "last_message" field is displayed, which must not be empty (null) to ensure that no empty conversations appear for the user.
This ensures that only conversations containing actual messages, whether created or received by the user, are displayed.
Any new conversation created when the user composes and sends a message is automatically added to the conversation list when this endpoint is accessed.
````bash
    GET : api/conversations/
    Response : 
    {
        "count": Integer
        "next": String(url)
        "previous": String(url)
        "results": [
            {
                "id": String(uuid)
                "sender": {
                    "id": String(uuid)
                    "username": String
                    "avatar":  String(url)
                },
                "receiver": {
                    "id": String(uuid)
                    "username": String
                    "avatar":  String(url)
                },
                "last_message_preview": String
                "date_last_message": DateTime
                "is_blocked": Boolean
                "blocked_by": String(uuid)
                "unread_count": Integer
                "created_at": DateTime
            }
        ]
    }

````
## Create New Conversation
This path (Endpoint) is for creating a new conversation between any two users:
It receives the ID of the receiving user.
The system first checks if a conversation already exists between the two parties.
If it does, it returns it directly.
If it doesn't exist, it creates a new conversation between the two parties only.
This system ensures that each conversation connects only two parties, and that there cannot be more than two parties in the same conversation, to prevent multiple conversations for the same pair of users.
````bash
    GET : api/conversations/new/?user_id=8ecdccf6-4680-42ff-b745-6047544d8456
    Response :
        {
            "id": String(uuid)
            "sender": {
                "id": String(uuid)
                "username": String
                "avatar":  String(url)
            },
            "receiver": {
                "id": String(uuid)
                "username": String
                "avatar":  String(url)
            },
            "last_message_preview": String
            "date_last_message": DateTime
            "is_blocked": Boolean
            "blocked_by": String(uuid)
            "unread_count": Integer
            "created_at": DateTime
        }
````
## Block Conversation
This feature (Endpoint) is designed for Block Conversation, a crucial feature because it allows any participant in a conversation to temporarily or permanently stop messages from the other participant.
When a block is enabled, the blocked participant will be unable to send messages within the same conversation.
This feature contributes to user protection and ensures a safe and comfortable communication experience on the platform.
````bash
    POST : api/conversations/<uuid:pk>/toggle-block/
````
## Delete Conversation
````bash
    DELETE : api/conversations/<uuid:pk>/delete/
````
## Send New Message
This endpoint is for creating a new message within a specific conversation:
It receives the following data in the request:
Conversation ID (conversation_id)
Receiver ID (receiver_id)
Message text (message)
Video (video) if available
Audio (audio) if available
Images (images) if available
This path allows any user to send messages, either text or multimedia, to the other party within the specified conversation, making communication more flexible and engaging.
````bash
    POST | GET: api/conversations/<uuid:conversation_id>/messages/
    Body : {
        "message": String
        "receiver": String(uuid)
        "conversation": String(uuid)
        "video": File
        "audio": File
        "images_files": Array[Files]
    }
    Response : {
        "id": String(uuid)
        "message": String()
        "video": File()
        "audio": File
        "images": Array[File]
        "sender": String(uuid) # "32e6f6df-d5cd-496d-a3a3-530d74da0896"
        "receiver": String(uuid) # "8ecdccf6-4680-42ff-b745-6047544d8456"
        }
````
## Update Message
This endpoint is for updating existing messages, allowing any user to edit a message they sent if they wish to change its content.
It allows editing the text or media associated with the message.
Access is restricted to the original message sender to ensure data security and control over edits.
````bash
    PUT | PATCH : api/messages/<uuid:pk>/update/
````
## Delete Message
Endpoint Delete Message: Allows the sender to delete any message they have sent within the conversation.
````bash
    DELETE : api/messages/<uuid:pk>/delete/
````
## Read Message
Endpoint Read Message: Allows the recipient to mark the message as read, so that the sender is notified that their message has been read.
````bash
    PUT | PATCH : api/messages/<uuid:pk>/read/
````

## Note:
Generally, the chat system we created is simple and covers the basics, given that this is a pilot project.
In real-world projects, many advanced features can be added, such as:
Group Conversations
Advanced Blocking: If a user blocks another user, the blocked user cannot create any new chats with them.
And other features like timed messages, notifications, end-to-end encryption, and multimedia management.
These additions make the system more flexible and secure, and better suited to the needs of large-scale projects.














