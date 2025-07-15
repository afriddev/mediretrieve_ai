from pymongo import MongoClient
from typing import Any, cast

mongoClient = cast(Any, MongoClient("mongodb://localhost:27017/"))
