from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Temperatures:
    pk: str
    name: str
    price: float
    quantity: int

    def __init__(self, pk: str, name: str, price: float, quantity: int) -> None:
        self.pk = pk
        self.name = name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def from_dict(obj: Any) -> 'Temperatures':
        assert isinstance(obj, dict)
        pk = from_str(obj.get("pk"))
        name = from_str(obj.get("name"))
        price = from_float(obj.get("price"))
        quantity = from_int(obj.get("quantity"))
        return Temperatures(pk, name, price, quantity)

    def to_dict(self) -> dict:
        result: dict = {}
        result["pk"] = from_str(self.pk)
        result["name"] = from_str(self.name)
        result["price"] = to_float(self.price)
        result["quantity"] = from_int(self.quantity)
        return result


def temperatures_from_dict(s: Any) -> Temperatures:
    return Temperatures.from_dict(s)


def temperatures_to_dict(x: Temperatures) -> Any:
    return to_class(Temperatures, x)
