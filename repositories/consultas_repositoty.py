from sqlalchemy import text
from sqlalchemy.orm import Session
from collections import defaultdict

class ConsultasRepo():
    @staticmethod
    def tipo_deudas(db:Session,cod_administrado:str):
        tipo_deudas=''
        query = text("""
        SELECT DISTINCT
            deudas_administrado.id_tipo_deudas_administrado AS id_deuda, 
            deudas_administrado.descripcion_tipo AS tipo_deuda
        FROM cuotas_deudas_administrado
        INNER JOIN deudas_administrado 
            ON deudas_administrado.id_deudas_administrado = cuotas_deudas_administrado.id_deudas_administrado
        LEFT JOIN predio_urbano 
            ON cuotas_deudas_administrado.cod_predio_urbano = predio_urbano.cod_predio_urbano
        WHERE cuotas_deudas_administrado.codigo_administrado = :codigo
          AND cuotas_deudas_administrado.estado_deuda <> 'I'
          AND cuotas_deudas_administrado.estado_deuda = 'P'
          AND cuotas_deudas_administrado.estado = 'A'
        """)
        result = db.execute(query, {"codigo": cod_administrado}).fetchall()
        if not result:
            return False
        tipo_deudas = ",".join([f"{row[0]}:{row[1]}" for row in result])
        return tipo_deudas
    @staticmethod
    def consulta_deudas(db:Session,tipos:int,codigo:str):
        query=text("""select "cuotas_deudas_administrado".id_deudas_administrado as id_deu,"cuotas_deudas_administrado".*, 
                coalesce(trim(predio_urbano.cod_predio_urbano||' '||predio_urbano.direccion),cuotas_deudas_administrado.cod_predio_urbano) as direccion_predio 
                ,"deudas_administrado"."nro_anexo", 
                cuotas_deudas_administrado.cod_predio_urbano as predio 
                from "cuotas_deudas_administrado" 
                inner join "deudas_administrado" on "deudas_administrado"."id_deudas_administrado" = "cuotas_deudas_administrado"."id_deudas_administrado" 
                left join "predio_urbano" on "cuotas_deudas_administrado"."cod_predio_urbano" = "predio_urbano"."cod_predio_urbano"
                where "cuotas_deudas_administrado"."codigo_administrado" = :codigo
                and "cuotas_deudas_administrado"."estado_deuda" <> 'I' 
                and "cuotas_deudas_administrado"."estado_deuda" = 'P' 
                and "cuotas_deudas_administrado"."estado" = 'A' 
                and "deudas_administrado"."id_tipo_deudas_administrado" = :tipos
                order by "cuotas_deudas_administrado"."anio" asc, "cuotas_deudas_administrado"."tipo" asc, "cuotas_deudas_administrado"."cuota" asc
                """)
        result = db.execute(query, {"codigo": codigo,"tipos":tipos}).fetchall()
        if not result:
            return False
        return result
    import json

    @staticmethod
    def generar_mensaje_whatsapp(data):
        deudas = data["deudas"]

        # Eliminar duplicados por año, mes y predio
        unicas = {(d["anio"], d["mes"], d["predio"]): d for d in deudas}.values()

        # Agrupar por año
        deudas_por_anio = defaultdict(list)
        for d in unicas:
            deudas_por_anio[d["anio"]].append(d)

        predio = list(unicas)[0]["direccion_predio"]
        codigo = list(unicas)[0]["predio"]

        mensaje = (
            "📢 *Municipalidad de Tarapoto*\n"
            "Estimado contribuyente, hemos verificado sus *deudas pendientes de Impuesto Predial*.\n\n"
            f"🏠 Predio: *{predio}*\n"
            f"💳 Código: *{codigo}*\n\n"
            "📅 *Detalle de cuotas pendientes:*\n"
        )

        total_general = 0

        # Recorrer los años
        for anio, lista in sorted(deudas_por_anio.items()):
            lista_ordenada = sorted(lista, key=lambda x: x["mes"])
            total_anio = sum(d["monto"] for d in lista_ordenada)
            total_general += total_anio

            mensaje += f"\n📆 *Año {anio}*\n\n"
            for d in lista_ordenada:
                mensaje += f"  🗓 {ConsultasRepo.mes_nombre(d['mes'])} → S/ {d['monto']:.2f}\n"
            mensaje += f"  💵 *Subtotal {anio}: S/ {total_anio:.2f}*\n"

        mensaje += (
            f"\n💰 *Total pendiente:* *S/ {total_general:.2f}*\n\n"
            "Para regularizar su deuda, puede acercarse a la caja municipal o escribirnos para más información.\n\n"
            "🤝 Gracias por su compromiso con el desarrollo de nuestra ciudad."
        )

        return mensaje

    @staticmethod
    def mes_nombre(num):
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return meses[num - 1]
