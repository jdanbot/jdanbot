from pydantic import BaseModel


def unpack_needen(obj: dict | BaseModel, fields: tuple) -> dict:
    def my_filter(el) -> bool:
        key, value = el

        return key in fields

    try:
        obj = obj.model_dump()
    except AttributeError:
        pass

    items = obj.items()

    return dict(filter(my_filter, items))
