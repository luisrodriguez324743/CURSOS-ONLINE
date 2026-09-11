from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.database.connection import SessionLocal
from src.entities.certificado import Certificado
from src.entities.factura import Factura
from src.entities.pago import Pago


def _seed_factura(session) -> None:
    id_usuario = UUID("11111111-1111-1111-1111-111111111111")
    id_curso = UUID("22222222-2222-2222-2222-222222222222")
    id_factura = UUID("33333333-3333-3333-3333-333333333333")

    existente = session.query(Factura).filter_by(id_factura=id_factura).first()
    if existente is not None:
        print("La factura ya existe.")
        return

    factura = Factura(
        id_factura=id_factura,
        numero_factura="FAC-001",
        total=199.99,
        id_usuario=id_usuario,
        id_curso=id_curso,
        metodo_pago="tarjeta",
        estado="pagada",
    )

    session.add(factura)
    print("Factura semilla cargada correctamente.")


def _seed_pago(session) -> None:
    id_usuario = UUID("11111111-1111-1111-1111-111111111111")
    id_curso = UUID("22222222-2222-2222-2222-222222222222")
    id_factura = UUID("33333333-3333-3333-3333-333333333333")
    id_pago = UUID("44444444-4444-4444-4444-444444444444")

    existente = session.query(Pago).filter_by(id_pago=id_pago).first()
    if existente is not None:
        print("El pago ya existe.")
        return

    pago = Pago(
        id_pago=id_pago,
        monto=199.99,
        metodo_pago="tarjeta",
        estado="pagado",
        id_usuario=id_usuario,
        id_curso=id_curso,
        id_factura=id_factura,
    )

    session.add(pago)
    print("Pago semilla cargado correctamente.")


def _seed_certificado(session) -> None:
    id_usuario = UUID("11111111-1111-1111-1111-111111111111")
    id_curso = UUID("22222222-2222-2222-2222-222222222222")
    id_certificado = UUID("55555555-5555-5555-5555-555555555555")

    existente = (
        session.query(Certificado).filter_by(id_certificado=id_certificado).first()
    )
    if existente is not None:
        print("El certificado ya existe.")
        return

    certificado = Certificado(
        id_certificado=id_certificado,
        codigo="CERT-001",
        id_usuario=id_usuario,
        id_curso=id_curso,
    )

    session.add(certificado)
    print("Certificado semilla cargado correctamente.")


def seed() -> None:
    session = SessionLocal()
    try:
        _seed_factura(session)
        _seed_pago(session)
        _seed_certificado(session)
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Error al insertar los datos semilla.")
    finally:
        session.close()
