
from datetime import datetime, timedelta, timezone
import pytz

# Devuelve el tiempo actual en segundos, con zona horaria (por defecto UTC)
def get_current_epoch_seconds(tz_name: str = "UTC") -> int:
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    return int(now.timestamp())

# Suma un timedelta a la fecha actual y devuelve el tiempo resultante en segundos
def add_timedelta_and_get_epoch_seconds(delta: timedelta, tz_name: str = "UTC") -> int:
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    future_time = now + delta
    return int(future_time.timestamp())
