# personal_blog
- **django Personal Blog application API using REST FameWork**

Creating Custom AppUser ,Serializer , and its Validation
using AuthToken Authentication ,

Testing the APIs On Postman


**Features V1:**
  - User `Account app`
    - Login and get AppUser Token
    - get user profile by user name /username
    - logout the authorized user
    - Register/Create New AppUser
    - validation using Regex 
      - Email build-in validation 
      - phone number validation only Egyptian numbers like +/010,012,..
      - username validation must be lowercase alpha  digits,- ,.
      - confirm Password Validation

  - User ` Blog App`
    - Post,Comment,Like ,Category, and Tag Models
    - CRUD for Post,Category, and Tags
    - User can un/like post and comment to it
    - authorized for Delete/update/post Methods
    - validation Post data 
    - only owners or admin can delete the post/comment
    - link likes and comment count to post serializers 
    - using dynamic serializers to custom return data
    - create custom permissions IsOwnerOrAdmin
   


**Tools**
- PyCharm
- VS Code
- Workbench MySQL , Sqlite
- Postman for Testing


**Contact Information:**

For any inquiries or collaboration opportunities, you can reach out to me:

- **LinkedIn**: [LinkedIn Profile](https://www.linkedin.com/in/m7mmed-sayed/)
- **Email**: mohamedsayed1167@gmail.com