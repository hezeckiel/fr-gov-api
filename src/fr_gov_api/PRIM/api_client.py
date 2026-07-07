import os
from typing import Literal, Optional

import polars as pl
import requests as rq

from .model import PRIMResponse

API_URL = "https://prim.iledefrance-mobilites.fr"


class PrimClient:
    """"""

    def __init__(self):
        """"""
        self.prim_token = os.getenv("PRIM_TOKEN", "MISSING")
        self.base_url = f"{API_URL}/marketplace"

        self.session = rq.Session()

        self.upadate_headers()

    def upadate_headers(self):
        """"""
        headers = {
            "apiKey": self.prim_token,
            "accept": "application/json",
            "accept-encoding": "gzip, deflate"
        }

        self.session.headers.update(headers)

    def query(
        self,
        endpoint: str,
        method: Literal["get", "post"],
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """"""
        url = f"{self.base_url}/{endpoint}"

        res = self.session.request(
            method,
            url,
            params=params,
            json=json,
        )

        res.raise_for_status()

        data = res.json()

        _obj = PRIMResponse.model_validate(data)

        out = data["Siri"]["ServiceDelivery"]

        return out

    def stop_monitoring(self, stop_point_ref: str) -> dict | None:
        """"""
        payload = {"MonitoringRef": stop_point_ref}

        res = self.query("stop-monitoring", method="get", params=payload)

        data = res.get("StopMonitoringDelivery")

        return data

    def requete_ligne(self, ligne_ref: str) -> dict | None:
        """"""
        payload = {"LineRef": ligne_ref}

        res = self.query("requete-ligne", method="get", params=payload)

        data = res.get("LineDescriptionDelivery")

        return data
    
    def estimated_timetable(self, ligne_ref: str = "ALL", to_df: bool = False) -> dict | pl.DataFrame:
        """"""
        payload = {"LineRef": ligne_ref}

        res = self.query("estimated-timetable", method="get", params=payload)

        data = res["EstimatedTimetableDelivery"][0]["EstimatedJourneyVersionFrame"][0]["EstimatedVehicleJourney"]

        return data
