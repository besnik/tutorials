# BASIC TYPES

from sqlalchemy import Integer          # INT
from sqlalchemy import String           # VARCHAR
from sqlalchemy import Unicode          # VARCHAR, NVARCHAR depending on db
from sqlalchemy import Boolean          # BOOLEAN, INT, TINYINT
from sqlalchemy import DateTime         # DATETIME, TIMESTAMP, returns python datetime() object
from sqlalchemy import Float            # FLOAT
from sqlalchemy import Numeric          # returns python Decimal() object

from sqlalchemy import UnicodeText      # VARCHAR, NVARCHAR