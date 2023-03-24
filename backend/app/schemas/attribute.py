from typing import Any, Optional

from pydantic import BaseModel, Field, root_validator


class AttributeBase(BaseModel):
    attribute_name: str = Field(..., alias="attributeName")
    attribute_data_type: str = Field(..., alias="attributeType")
    validation_data: Any = Field(None, alias="validation")

    class Config:
        allow_population_by_field_name = True


class AttributeInDB(AttributeBase):
    attribute_id: Any = Field(None, alias="attributeID")

    class Config:
        allow_population_by_field_name = True


class Attribute(AttributeInDB):
    attribute_value: Optional[Any] = Field(None, alias="attributeValue")
    # cast string to correct type based on attribute type

    @root_validator
    def check_metadata(cls, values):
        t = values.get("attribute_data_type")
        v = values.get("attribute_value")
        # check if string is actually and array and convert
        if (
            (t == "list" or t == "options")
            and isinstance(v, str)
            and v.startswith("{")
            and v.startswith("{")
        ):
            values["attribute_value"] = v[1:-1].split(",")
        # convert if a number
        if (t == "num_lmt" or t == "number") and isinstance(v, str) and v.isnumeric():
            values["attribute_value"] = int(v)
        if t == "checkbox":
            values["attribute_value"] = str(v).lower() == "true"
        return values

    class Config:
        allow_population_by_field_name = True
