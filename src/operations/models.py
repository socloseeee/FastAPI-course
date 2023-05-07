from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData

metaData = MetaData()

operation = Table(
    "operation",
    metaData,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)