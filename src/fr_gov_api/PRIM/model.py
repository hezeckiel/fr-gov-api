from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, field_validator


class ValueWrapper(BaseModel):
    value: str


class StopAssignment(BaseModel):
    ExpectedQuayRef: Optional[ValueWrapper] = None


class EstimatedCall(BaseModel):
    StopPointRef: ValueWrapper
    DestinationDisplay: list[ValueWrapper]
    ExpectedDepartureTime: Optional[str] = None
    ExpectedArrivalTime: Optional[str] = None
    AimedArrivalTime: Optional[str] = None
    AimedDepartureTime: Optional[str] = None
    ArrivalStatus: Optional[str] = None
    DepartureStatus: Optional[str] = None
    ArrivalStopAssignment: Optional[StopAssignment] = None
    DepartureStopAssignment: Optional[StopAssignment] = None
    ArrivalPlatformName: Optional[ValueWrapper] = None
    DeparturePlatformName: Optional[ValueWrapper] = None
    ArrivalProximityText: Optional[ValueWrapper] = None
    CallNote: Optional[list[ValueWrapper]] = None


class EstimatedCalls(BaseModel):
    EstimatedCall: list[EstimatedCall]


class EstimatedVehicleJourney(BaseModel):
    RecordedAtTime: str
    LineRef: ValueWrapper
    DatedVehicleJourneyRef: ValueWrapper
    VehicleMode: list[str]
    VehicleFeatureRef: list[str]
    PublishedLineName: list[ValueWrapper]
    DirectionName: list[ValueWrapper]
    OriginName: list[ValueWrapper]
    DestinationRef: ValueWrapper
    DestinationName: list[ValueWrapper]
    JourneyNote: list[ValueWrapper]
    EstimatedCalls: EstimatedCalls
    VehicleJourneyName: list[ValueWrapper]
    DirectionRef: Optional[ValueWrapper] = None
    RouteRef: Optional[ValueWrapper] = None
    OriginRef: Optional[ValueWrapper] = None
    OperatorRef: Optional[ValueWrapper] = None
    ProductCategoryRef: Optional[ValueWrapper] = None
    DestinationShortName: Optional[list[ValueWrapper]] = None
    FirstOrLastJourney: Optional[ValueWrapper] = None

    @field_validator(
        "RouteRef",
        "OriginRef",
        "OperatorRef",
        "ProductCategoryRef",
        mode="before",
    )
    @classmethod
    def _empty_dict_to_none(cls, v: object) -> object:
        if isinstance(v, dict) and not v:
            return None
        return v


class EstimatedJourneyVersionFrame(BaseModel):
    EstimatedVehicleJourney: list[EstimatedVehicleJourney]


class EstimatedTimetableDelivery(BaseModel):
    ResponseTimestamp: str
    Version: str
    Status: str
    EstimatedJourneyVersionFrame: list[EstimatedJourneyVersionFrame]


class ServiceDelivery(BaseModel):
    ResponseTimestamp: str
    ProducerRef: str
    ResponseMessageIdentifier: str


class Siri(BaseModel):
    ServiceDelivery: ServiceDelivery


class PRIMResponse(BaseModel):
    Siri: Siri
