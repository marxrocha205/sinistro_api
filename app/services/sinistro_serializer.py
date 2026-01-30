from app.core.config import settings


def serialize_sinistro(s):

    envolvidos = []

    for v in s.veiculos:
        envolvidos.append({
            "tipo": v.tipo,  # carro ou moto
            "veiculo": {
                "id": v.id,
                "placa": v.placa,
                "chassi": v.chassi,
                "descricao_outro": v.descricao_outro,
                "condutor": {
                    "nome": v.condutor.nome,
                    "cpf": v.condutor.cpf,
                    "possui_cnh": v.condutor.possui_cnh,
                    "numero_cnh": v.condutor.numero_cnh,
                } if v.condutor else None
            }
        })

    for p in s.pedestres:
        envolvidos.append({
            "tipo": "pedestre",
            "pedestre": {
                "nome": p.nome,
                "cpf": p.cpf,
            }
        })

    return {
        "id": s.id,
        "tipo_principal": s.tipo_principal,
        "tipo_secundario": s.tipo_secundario,
        "descricao_outro": s.descricao_outro,
        "endereco": s.endereco,
        "ponto_referencia": s.ponto_referencia,
        "latitude": s.latitude,
        "longitude": s.longitude,
        "houve_vitima_fatal": s.houve_vitima_fatal,
        "data_hora": s.data_hora,
        "usuario": {
            "id": s.usuario.id,
            "username": s.usuario.username,
            "perfil": s.usuario.perfil,
        } if s.usuario else None,
        "fotos": [
            {
                "id": f.id,
                "url": f"{settings.r2_public_url}/{f.caminho_arquivo}",
            }
            for f in s.fotos
        ],
        "envolvidos": envolvidos
    }
