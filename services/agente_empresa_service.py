from sqlalchemy.orm import Session
from schemas.agente_empresa_schema import AgenteEmpresaSchema,AgenteEmpresaCreate,AgenteEmpresaEstado,AgenteEmpresaComunicate
from models.agente_empresa import AgenteEmpresa
from models.empresa import Empresa
from models.agentes import Agente
from fastapi.responses import JSONResponse
from models.derivaciones import Derivaciones
from models.contactos import Contactos
from schemas.agente_empresa_schema import AgenteValidate

def get_agente_empresa(db:Session):
    result={}
    agentes_empresas=db.query(Empresa.id.label("id_empresa"),
                              Empresa.nombre.label("empresa"),
                              AgenteEmpresa.empresa_id,
                              AgenteEmpresa.agente_id
                                     ).outerjoin(AgenteEmpresa,Empresa.id==AgenteEmpresa.empresa_id
                                            ).filter(Empresa.estado=='A'
                                                     ).all()
    if not agentes_empresas:
        return JSONResponse(content={"message":"No se encontraron "})
    for agentes in agentes_empresas:
        print("jej")
        if not agentes.id_empresa in result:
            result[agentes.id_empresa]={
                "id":agentes.id_empresa,
                "empresa":agentes.empresa,
                "permisos":[]
            }
        if not agentes.agente_id:
            continue
        result[agentes.empresa_id]["permisos"].append(agentes.agente_id)
    return list(result.values())

def create_agente_empresa(db:Session,data:AgenteEmpresaCreate):
    result={}
    agentes_empresas=db.query(Empresa.id.label("id_empresa"),
                              Empresa.nombre.label("empresa"),
                              AgenteEmpresa.empresa_id,
                              AgenteEmpresa.agente_id
                                     ).outerjoin(AgenteEmpresa,Empresa.id==AgenteEmpresa.empresa_id
                                            ).filter(Empresa.estado=='A'
                                                     ,Empresa.id==data.id_empresa
                                                     ).all()
    if not agentes_empresas:
        for agente in data.agentes:
            agente_empresa=AgenteEmpresa(
                empresa_id=agente.id_empresa,
                agente_id=agente,
                estado_agente='A',
                estado='A'
            )
            db.add(agente_empresa)
            db.commit()
            db.refresh(agente_empresa)
            return JSONResponse(content={"message":"Asignación de agentes correctamente ejecutado"})
    agentes_asignados={p.agente_id for p in agentes_empresas}
    agentes_enviados=set(data.agentes)
    agentes_elimiandos=agentes_asignados-agentes_enviados
    for agente in data.agentes:
        if agente in agentes_asignados:
            continue
        obj=db.query(AgenteEmpresa
                     ).filter(AgenteEmpresa.estado=='I'
                              ,AgenteEmpresa.empresa_id==data.id_empresa
                              ,AgenteEmpresa.agente_id==agente).first()
        if obj:
            obj.estado='A'
            db.commit()
            db.refresh(obj)
            continue
        agente_empresa_asignado=AgenteEmpresa(
            empresa_id=data.id_empresa,
            agente_id=agente,
            estado_agente='A',
            estado='A'
        )
        db.add(agente_empresa_asignado)
        db.commit()
        db.refresh(agente_empresa_asignado)
    if agentes_elimiandos:
        db.query(AgenteEmpresa
                 ).filter(AgenteEmpresa.empresa_id==data.id_empresa
                          ,AgenteEmpresa.agente_id.in_(agentes_elimiandos)).update({AgenteEmpresa.estado:'I'},synchronize_session=False)
    return JSONResponse(content={"message":"Asignación de agentes correctamente ejecutado"})

def get_agentes_asignados_empresa(db:Session,id_empresa:int):
    agentes_asignados=db.query(Agente.id,
                               Agente.nombre,
                               Agente.descripcion,
                               AgenteEmpresa.estado_agente,
                               AgenteEmpresa.telefono,
                               AgenteEmpresa.instancia,
                               Agente.logo,
                               Agente.path,
                               AgenteEmpresa.empresa_id,
                               AgenteEmpresa.id.label("id_agente_empresa")
                               ).join(AgenteEmpresa,AgenteEmpresa.agente_id==Agente.id
                                      ).filter(AgenteEmpresa.empresa_id==id_empresa,
                                               Agente.estado=='A',
                                               AgenteEmpresa.estado=='A').all()
    if not agentes_asignados:
        return JSONResponse(content={"message":"No se encontraron agentes asignados"})
    agentes_list = [
        {
            "id": a.id,
            "id_agente_empresa":a.id_agente_empresa,
            "nombre": a.nombre,
            "descripcion": a.descripcion,
            "logo": a.logo,
            "empresa_id": a.empresa_id,
            "path":a.path,
            "instancia":a.instancia,
            "telefono":a.telefono,
            "estado_agente":a.estado_agente
        }
        for a in agentes_asignados
    ]
    return agentes_list

def get_agentes_asignados_empresa_path(db:Session,data:AgenteValidate):
    agentes_asignados=db.query(Agente.id,
                               Agente.nombre,
                               Agente.descripcion,
                               AgenteEmpresa.estado_agente,
                               AgenteEmpresa.telefono,
                               AgenteEmpresa.instancia,
                               Agente.logo,
                               Agente.path,
                               AgenteEmpresa.empresa_id,
                               AgenteEmpresa.id.label("id_agente_empresa")
                               ).join(AgenteEmpresa,AgenteEmpresa.agente_id==Agente.id
                                      ).filter(AgenteEmpresa.empresa_id==data.id_empresa,
                                               Agente.estado=='A',
                                               AgenteEmpresa.estado=='A',
                                               Agente.path==data.path).first()
    if not agentes_asignados:
        return JSONResponse(content={"message":"No se encontraron agentes asignados"})
    estado_derivacion=db.query(Derivaciones,Contactos
                               ).join(Contactos,Contactos.id==Derivaciones.id_contacto
                                      ).filter(Contactos.wa_id==data.telefono,Derivaciones.estado_derivacion=='ATENDIENDO').first()
    data=dict(agentes_asignados._mapping)
    data["estado_derivacion"] = False if estado_derivacion else True
    return data

def edit_agentes_asignados_empresa(db:Session,data:AgenteEmpresaComunicate):
    agentes_asignados=db.query(AgenteEmpresa).filter(AgenteEmpresa.id==data.id_agente_empresa).first()
    if not agentes_asignados:
        return JSONResponse(content={"message":"No se encontraron agentes asignados"})
    agentes_asignados.telefono=data.telefono
    agentes_asignados.instancia=data.instancia
    db.commit()
    db.refresh(agentes_asignados)
    return agentes_asignados

def estado_agentes_asignados_empresa(db:Session,data:AgenteEmpresaEstado):
    agente_empresa=db.query(AgenteEmpresa).filter(AgenteEmpresa.id==data.id_agente_empresa).first()
    if not agente_empresa:
        return JSONResponse(content={"message":"No se encontraron agentes asignados"})
    agente_empresa.estado_agente=data.estado
    db.commit()
    db.refresh(agente_empresa)
    return agente_empresa
    