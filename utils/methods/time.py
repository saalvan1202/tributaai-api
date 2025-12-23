from datetime import datetime as dt
import pytz
def timeActual():
    zona_peru = pytz.timezone("America/Lima")
    fecha_actual = dt.now(zona_peru)
    fecha_registro = fecha_actual.strftime("%Y/%m/%d,%H:%M:%S")
    fecha_validacion=fecha_actual.strftime("%Y-%m-%d")
    hora=fecha_actual.strftime("%H:%M:%S")
    timestamp = int(fecha_actual.timestamp())
    return {"fecha_registro":fecha_registro,"fecha_validacion":fecha_validacion,"hora":hora,"timestamp":timestamp}