from typing import Any, Dict, Mapping, MutableMapping, Optional, Type, TypeVar

from compenv.infrastructure.types import Connection as ConnectionProtocol
from compenv.infrastructure.types import Table as TableProtocol

Context = MutableMapping[str, Any]
_V = TypeVar("_V", bound=TableProtocol)

class Schema:
    context: Dict[str, object]
    connection: ConnectionProtocol
    database: str
    def __init__(
        self, schema_name: str, context: Optional[Context] = ..., *, connection: Optional[ConnectionProtocol] = None
    ) -> None: ...
    def spawn_missing_classes(self, context: Optional[Context] = ...) -> None: ...
    def __call__(self, cls: Type[_V], *, context: Optional[Mapping[str, object]] = ...) -> Type[_V]: ...
