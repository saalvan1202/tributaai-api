from sqlalchemy import text
from sqlalchemy.orm import Session

class ConsultasRepo():
    @staticmethod
    def tipo_deudas(db:Session,cod_administrado:str):
        tipo_deudas=''
        query = text("""
        SELECT DISTINCT 
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
        for item in result:
            tipo_deudas=tipo_deudas + ',' + str(item)
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