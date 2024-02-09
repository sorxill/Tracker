import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME_TEST = os.environ["DB_NAME_TEST"]
DB_HOST_TEST = os.environ["DB_HOST_TEST"]
DB_PORT_TEST = os.environ["DB_PORT_TEST"]
DB_USER_TEST = os.environ["DB_USER_TEST"]
DB_PASS_TEST = os.environ["DB_PASS_TEST"]
PRIVATE_KEY_JWT = os.environ["PRIVATE_KEY_JWT"]
PUBLIC_KEY_JWT = os.environ["PUBLIC_KEY_JWT"]
ALGORITHM_JWT = os.environ["ALGORITHM_JWT"]
EXPIRE_MINUTES_JWT = os.environ["EXPIRE_MINUTES_JWT"]
