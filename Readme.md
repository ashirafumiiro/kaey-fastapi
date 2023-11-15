## Kaey Website BE (Fast API version)
This codebase contains the fastapi version of the kaey api backend. It uses mongodb to store the data and cloudinary for image storage.

#### Needed Environment variables
| Variable | Description | 
|----------|:------------|
| MONGODB_URL | This is the mongo Db Url that should be added as an environment variable. It is safer to quote it |
| SECRET_KEY | Secret for JWT token generation |
| ALGORITHM | Algorithm for hashing passwords |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token expiration |
| CLOUD_NAME | Cloudinary Name |
| CLOUD_KEY | Cloudinary API KEY |
| CLOUD_SECRET | Cloudinary API Secret |