import cloudinary
from dotenv import load_dotenv
import os


load_dotenv()
cloudinary.config( 
  cloud_name = os.environ['CLOUD_NAME'], 
  api_key = os.environ['CLOUD_KEY'], 
  api_secret = os.environ['CLOUD_SECRET']
)