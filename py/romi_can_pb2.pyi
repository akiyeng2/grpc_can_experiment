from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TalonSRXControlMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    PercentOutput: _ClassVar[TalonSRXControlMode]
    Position: _ClassVar[TalonSRXControlMode]
    Disabled: _ClassVar[TalonSRXControlMode]
PercentOutput: TalonSRXControlMode
Position: TalonSRXControlMode
Disabled: TalonSRXControlMode

class CreateRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class SetRequest(_message.Message):
    __slots__ = ["id", "value", "mode"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    id: int
    value: float
    mode: TalonSRXControlMode
    def __init__(self, id: _Optional[int] = ..., value: _Optional[float] = ..., mode: _Optional[_Union[TalonSRXControlMode, str]] = ...) -> None: ...

class StatusReply(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
