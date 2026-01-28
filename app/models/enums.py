from enum import Enum

class PerfilUsuario(str, Enum):
    ADMIN = "ADMIN"
    AGENTE = "AGENTE"


class TipoPrincipalSinistro(str, Enum):
    CARRO = "CARRO"
    MOTO = "MOTO"
    OUTRO = "OUTRO"


class TipoSecundarioSinistro(str, Enum):
    CARRO_CARRO = "CARRO_CARRO"
    CARRO_MOTO = "CARRO_MOTO"
    CARRO_PEDESTRE = "CARRO_PEDESTRE"
    CARRO_OUTRO = "CARRO_OUTRO"
    MOTO_CARRO = "MOTO_CARRO"
    MOTO_MOTO = "MOTO_MOTO"
    MOTO_PEDESTRE = "MOTO_PEDESTRE"
    MOTO_OUTRO = "MOTO_OUTRO"
    OUTRO_OUTRO = "OUTRO_OUTRO"


class TipoVeiculo(str, Enum):
    CARRO = "CARRO"
    MOTO = "MOTO"
    OUTRO = "OUTRO"


class TipoFoto(str, Enum):
    SINISTRO = "SINISTRO"
    VITIMA = "VITIMA"
    VEICULO = "VEICULO"
    CNH = "CNH"
