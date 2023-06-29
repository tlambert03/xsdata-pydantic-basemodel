from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "foo"


class Items(BaseModel):
    item: List["Items.Item"] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "foo",
        },
    )

    class Item(BaseModel):
        product_name: str = Field(
            metadata={
                "name": "productName",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        quantity: int = Field(
            metadata={
                "type": "Element",
                "namespace": "foo",
                "required": True,
                "max_exclusive": 100,
            }
        )
        usprice: Decimal = Field(
            metadata={
                "name": "USPrice",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        comment: Optional[str] = Field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "foo",
            },
        )
        ship_date: Optional[XmlDate] = Field(
            default=None,
            metadata={
                "name": "shipDate",
                "type": "Element",
                "namespace": "foo",
            },
        )
        part_num: str = Field(
            metadata={
                "name": "partNum",
                "type": "Attribute",
                "required": True,
                "pattern": r"\d{3}-[A-Z]{2}",
            }
        )


class Usaddress(BaseModel):
    class Meta:
        name = "USAddress"

    name: str = Field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    street: str = Field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    city: str = Field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    state: str = Field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    zip: Decimal = Field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    country: str = Field(
        init=False,
        default="US",
        metadata={
            "type": "Attribute",
        },
    )


class Comment(BaseModel):
    class Meta:
        name = "comment"
        namespace = "foo"

    value: str = Field(
        default="",
        metadata={
            "required": True,
        },
    )


class PurchaseOrderType(BaseModel):
    ship_to: Usaddress = Field(
        metadata={
            "name": "shipTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    bill_to: Usaddress = Field(
        metadata={
            "name": "billTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    comment: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "foo",
        },
    )
    items: Items = Field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    order_date: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "name": "orderDate",
            "type": "Attribute",
        },
    )


class PurchaseOrder(PurchaseOrderType, BaseModel):
    class Meta:
        name = "purchaseOrder"
        namespace = "foo"
