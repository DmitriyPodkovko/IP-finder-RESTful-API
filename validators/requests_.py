from pydantic import BaseModel, IPvAnyAddress, Field, field_validator
from datetime import datetime
# from helpers.matchers import ip_checker, port_checker
# from helpers.mobile_operators_ import checker


class IpsDataRequest(BaseModel):
    IP_DST: IPvAnyAddress
    Port_DST: int = Field(gt=0, lt=65536, description='Distinction port (0-65535)')
    Date: str = Field(description='Date in format DD.MM.YYYY')
    # Date: str = Field(pattern=r"\d{2}\.\d{2}\.\d{4}", description='Date in format DD.MM.YYYY')
    Time: str = Field(description='Time in format HH:MM:SS')
    # Time: str = Field(pattern=r"\d{2}:\d{2}:\d{2}", description='Time in format HH:MM:SS')
    Provider: str

    @field_validator('Date')
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError(f"Invalid date: {value}. Expected format DD.MM.YYYY.")
        return value

    @field_validator('Time')
    def validate_time(cls, value):
        try:
            datetime.strptime(value, "%H:%M:%S")
        except ValueError:
            raise ValueError(f"Invalid time: {value}. Expected format HH:MM:SS.")
        return value

# class IpsDataRequest(BaseModel):
#     id: int
#     empty: None = None
#     source_ip: str = "10.0.0.1"
#     source_port: int = 8001
#     dest_ip: str = "192.168.0.1"
#     dest_port: int = 8002
#     datetime_: datetime = datetime.utcnow()
#     operator_: str = "Kyivstar"
#     country: str = "Ukraine"
#     result: str = None
#
#     @field_validator('operator_')
#     def operator_isvalid(cls, v):
#         if not checker(operator=v):
#             raise ValueError('Operator is not valid!')
#         return v
#
#     @field_validator('source_ip')
#     def source_ip_isvalid(cls, v):
#         if not ip_checker(ip=v):
#             raise ValueError('Source ip is not valid!')
#         return v
#
#     @field_validator('source_port')
#     def source_port_isvalid(cls, v):
#         if not port_checker(port=v):
#             raise ValueError('Source port is not valid!')
#         return v
#
#     @field_validator('dest_ip')
#     def dest_ip_isvalid(cls, v):
#         if not ip_checker(ip=v):
#             raise ValueError('Dest ip is not valid!')
#         return v
#
#     @field_validator('dest_port')
#     def dest_port_isvalid(cls, v):
#         if not port_checker(port=v):
#             raise ValueError('Dest port is not valid!')
#         return v
#
#     @field_validator('country')
#     def country_isvalid(cls, v):
#         if not isinstance(v, str):
#             raise ValueError('Country is not valid!')
#         return v
#
#     @field_validator('id')
#     def id_isvalid(cls, v):
#         if not isinstance(v, int):
#             raise ValueError('Id is not valid!')
#         return v
