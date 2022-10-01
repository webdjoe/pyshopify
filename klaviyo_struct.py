from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Index, Integer, LargeBinary, PrimaryKeyConstraint, SmallInteger, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import TINYINT, UNIQUEIDENTIFIER
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_CampaignExcludes = Table(
    'CampaignExcludes', metadata,
    Column('campaign_id', Unicode(255), nullable=False),
    Column('object', Unicode(255), nullable=False),
    Column('id', Unicode(255), nullable=False),
    Column('name', Unicode(255)),
    Column('list_type', Unicode(255)),
    Column('folder', Unicode(255)),
    Column('person_count', BigInteger),
    Column('campaign_sent_at', DateTime)
)


t_CampaignIncludes = Table(
    'CampaignIncludes', metadata,
    Column('campaign_id', Unicode(255), nullable=False),
    Column('object', Unicode(255), nullable=False),
    Column('id', Unicode(255), nullable=False),
    Column('name', Unicode(255)),
    Column('list_type', Unicode(255)),
    Column('folder', Unicode(255)),
    Column('person_count', BigInteger),
    Column('campaign_sent_at', DateTime)
)


class CampaignList(Base):
    __tablename__ = 'CampaignList'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_campaign_list_id'),
    )

    id = Column(Unicode(255))
    name = Column(Unicode(255))
    subject = Column(Unicode(255))
    status = Column(Unicode(255))
    status_label = Column(Unicode(255))
    status_id = Column(Integer)
    num_recipients = Column(BigInteger)
    is_segmented = Column(SmallInteger)
    message_type = Column(Unicode(255))
    template_id = Column(Unicode(255))
    sent_at = Column(DateTime)
    send_time = Column(DateTime)


class CampaignMetrics(Base):
    __tablename__ = 'CampaignMetrics'
    __table_args__ = (
        PrimaryKeyConstraint('campaign_id', 'date', 'metric_id', 'measure', name='PK_campaign_metrics'),
        Index('IDX_CampaignMetrics', 'metric_id', 'measure', 'date')
    )

    campaign_id = Column(Unicode(255), nullable=False)
    date = Column(Date, nullable=False)
    metric_id = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    measure = Column(Unicode(50), nullable=False)
    values = Column(Float(53))


t_CampaignRevenue = Table(
    'CampaignRevenue', metadata,
    Column('date', Date, nullable=False),
    Column('Value', Float(53))
)


t_DateDimension = Table(
    'DateDimension', metadata,
    Column('TheDate', Date),
    Column('TheDay', Integer),
    Column('TheDaySuffix', CHAR(2, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TheDayName', Unicode(30)),
    Column('TheDayOfWeek', Integer),
    Column('TheDayOfWeekInMonth', TINYINT),
    Column('TheDayOfYear', Integer),
    Column('IsWeekend', Integer, nullable=False),
    Column('TheWeek', Integer),
    Column('TheISOweek', Integer),
    Column('TheFirstOfWeek', Date),
    Column('TheLastOfWeek', Date),
    Column('TheWeekOfMonth', TINYINT),
    Column('TheMonth', Integer),
    Column('TheMonthName', Unicode(30)),
    Column('TheFirstOfMonth', Date),
    Column('TheLastOfMonth', Date),
    Column('TheFirstOfNextMonth', Date),
    Column('TheLastOfNextMonth', Date),
    Column('TheQuarter', Integer),
    Column('TheFirstOfQuarter', Date),
    Column('TheLastOfQuarter', Date),
    Column('TheYear', Integer),
    Column('TheISOYear', Integer),
    Column('TheFirstOfYear', Date),
    Column('TheLastOfYear', Date),
    Column('IsLeapYear', Boolean),
    Column('Has53Weeks', Integer, nullable=False),
    Column('Has53ISOWeeks', Integer, nullable=False),
    Column('MMYYYY', CHAR(6, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Style101', CHAR(10, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Style103', CHAR(10, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Style112', CHAR(8, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Style120', CHAR(10, 'SQL_Latin1_General_CP1_CI_AS')),
    Index('PK_DateDimension', 'TheDate', unique=True)
)


class FlowList(Base):
    __tablename__ = 'FlowList'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_flow_list_id'),
    )

    id = Column(Unicode(255))
    name = Column(Unicode(255), nullable=False)
    created = Column(DateTime, nullable=False)
    object = Column(Unicode(255))
    status = Column(Unicode(255))
    archived = Column(Boolean)
    updated = Column(DateTime)


class FlowMetrics(Base):
    __tablename__ = 'FlowMetrics'
    __table_args__ = (
        PrimaryKeyConstraint('flow_id', 'date', 'metric_id', 'measure', name='PK_flow_metrics'),
    )

    flow_id = Column(Unicode(255), nullable=False)
    date = Column(Date, nullable=False)
    metric_id = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    values = Column(Float(53), nullable=False)
    measure = Column(Unicode(50), nullable=False)


t_FlowRevenue = Table(
    'FlowRevenue', metadata,
    Column('date', Date, nullable=False),
    Column('Value', Float(53))
)


class Metrics(Base):
    __tablename__ = 'Metrics'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK_metrics_id'),
    )

    id = Column(Unicode(255))
    name = Column(Unicode(255))


class Templates(Base):
    __tablename__ = 'Templates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='PK__Template__3213E83FA2F59BBA'),
    )

    file_id = Column(UNIQUEIDENTIFIER, nullable=False, server_default=text('(newid())'))
    id = Column(Unicode(20))
    updated = Column(DateTime, nullable=False)
    created = Column(DateTime, nullable=False)
    name = Column(Unicode(255), nullable=False)
    html = Column(Unicode, nullable=False)
    image_path = Column(Unicode(255))
    image_blob = Column(LargeBinary)
