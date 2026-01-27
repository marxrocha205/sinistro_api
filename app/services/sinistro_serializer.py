from app.core.config import settings


def serialize_sinistro(s):

    return {
        "id": s.id,
        "tipo_principal": s.tipo_principal,
        "tipo_secundario": s.tipo_secundario,
        "descricao_outro": s.descricao_outro,
        "endereco": s.endereco,
        "latitude": s.latitude,
        "longitude": s.longitude,
        "ponto_referencia": s.ponto_referencia,
        "houve_vitima_fatal": s.houve_vitima_fatal,
        "data_hora": s.data_hora,
        "usuario_id": s.usuario_id,
        "fotos": [
            {
                "id": f.id,
                "url": f"{settings.r2_public_url}/{f.caminho_arquivo}",
            }
            for f in s.fotos
        ],
        "veiculos": [
            {
                "id": v.id,
                "tipo": v.tipo,
                "placa": v.placa,
                "chassi": v.chassi,
                "descricao_outro": v.descricao_outro,
                "condutor": (
                    {
                        "id": v.condutor.id,
                        "nome": v.condutor.nome,
                        "cpf": v.condutor.cpf,
                    }
                    if v.condutor else None
                )
            }
            for v in s.veiculos
        ],
        "pedestres": [
            {
                "id": p.id,
                "nome": p.nome,
                "cpf": p.cpf,
            }
            for p in s.pedestres
        ]
    }
