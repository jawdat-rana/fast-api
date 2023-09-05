import json
import datetime
import uuid

from typing import Union, List, Dict
from fastapi import APIRouter, HTTPException, status
from fastapi.exceptions import RequestValidationError, RequestErrorModel
from pydantic import BaseModel, root_model
import requests
import pandas as pd

router = APIRouter()


# Data Access Object
class NorgesBankInvestmentManagement:

    def __init__(self):

        self.data_file_name = 'EQ_2022_Country.xlsx'
        self.dataframe = pd.read_excel('./data/' + self.data_file_name, sheet_name="Holdings Report")

    def __data__(self) -> json:
        return json.dumps(self.dataframe.to_json())

    def get_market_value(self, by_column: str, currency: str):

        market_values = self.dataframe.groupby([by_column])[f'market_value_{currency}'].sum()

        response_payload = []
        for key, value in json.loads(market_values.to_json()).items():
            response_payload.append({by_column: key, "market_value": value})

        return response_payload


# Initializing Data Access Object
DB = NorgesBankInvestmentManagement()


# Data Models
class NBIMDatabaseSnapshotResponseModel(BaseModel):
    timestamp: str
    uuid: str
    data: str


class NBIMMarketValue(BaseModel):
    country: Union[str, None] = None
    industry: Union[str, None] = None
    market_value: int


@router.get("/v1/api/data/", tags=["data"], response_model=NBIMDatabaseSnapshotResponseModel)
async def get_data():
    payload = {'uuid': str(uuid.uuid4()),
               'timestamp': str(datetime.datetime.now()),
               'data': DB.__data__()}

    return payload


@router.get("/v1/api/market_value/", tags=["data"],
            response_model=List[NBIMMarketValue])
async def get_market_overview(by: str = "country", currency: str = "nok"):

    if by not in ["industry", "country"]:
        raise HTTPException(status_code=418, detail="Invalid column, contact support team")

    if currency not in ["nok", "usd"]:
        raise HTTPException(status_code=418, detail="Invalid currency type, contact support team to add currency")

    payload = DB.get_market_value(by, currency)

    return payload


@router.get("/v1/api/market_value/country/{country}", tags=["data"],
            response_model=NBIMMarketValue)
def get_market_overview_by_area(area: str):
    payload = dict()
    payload['uuid'] = str(uuid.uuid4())
    payload['timestamp'] = str(datetime.datetime.now())
    payload['data'] = DB.get_data_by_area(area)

    return payload
