import json
from pydantic import BaseModel, Field
from typing import Optional


class ETAJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj is None:
            # don't serialize None
            return None
        elif isinstance(obj, BaseModel):
            # only return the non-None values, including non-None values in nested models
            filtered_dict = {}
            for k, v in obj.dict().items():
                if v is None:
                    continue
                elif isinstance(v, BaseModel):
                    filtered_dict[k] = self.default(v)
                else:
                    filtered_dict[k] = v
            return filtered_dict
        # Let the base class default method raise the TypeError
        return super().default(obj)


class C(BaseModel):
    cfoo: Optional[str] = Field(default=None)
    cbar: Optional[str] = Field(default=None)


class B(BaseModel):
    bfoo: Optional[str] = Field(default=None)
    bbar: Optional[str] = Field(default=None)
    c: Optional[C] = Field(default=None)


class A(BaseModel):
    afoo: Optional[str] = Field(default=None)
    abar: Optional[str] = Field(default=None)
    b: Optional[B] = Field(default=None)

    def json(self, **kwargs) -> str:
        return json.dumps(self.dict(exclude_unset=True, exclude_none=True), **kwargs)


a = A(afoo="afoo", b=B(bfoo="bfoo", c=C(cfoo="cfoo")))

# print(a.dict(exclude_unset=True, exclude_none=True, exclude_defaults=True))

print(a.json(indent=4))
