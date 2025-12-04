from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

metadata=MetaData(schema="dbo")
Base=declarative_base(metadata=metadata)