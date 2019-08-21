
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import schema, types
from sqlalchemy.orm import backref

Base = declarative_base()

class Inputs(Base):
    __tablename__ = 'Inputs'

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, nullable=False)
    run_name = Column(String(250), nullable=False, index=True)
    basin_id = Column(Integer, nullable=False, index=True)
    date_time = Column(types.DateTime(), nullable=False, index=True)
    variable = Column(String(250), nullable=False)
    function = Column(String(250), nullable=False)
    value = Column(types.Float(), nullable=False)
    unit = Column(String(250), nullable=True)
