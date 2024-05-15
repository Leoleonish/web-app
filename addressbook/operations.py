from .models import Address
from .schemas import AddressModel


def add_address(db, address: Address):
    db.add(AddressModel(**address.dict()))
    db.commit()
    db.refresh(AddressModel)
    return Address(**AddressModel.to_dict(db.query(AddressModel).filter_by(id=db.new.id).first()))


def get_all_addresses(db):
    return [Address(**address.to_dict()) for address in db.query(AddressModel)]


def get_addresses_by_location(db):
    return [Address(**address.to_dict()) for address in db.query(AddressModel)]


def update_address(db, address_id: int, new_data: Address):
    address = db.query(AddressModel).filter_by(id=address_id).first()
    if not address:
        raise ValueError(f"Address with id {address_id} not found")
    for field, value in new_data.dict().items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return Address(**AddressModel.to_dict(address))


def delete_address(db, address_id: int):
    address = db.query(AddressModel).filter_by(id=address_id).delete()
    db.commit()
    return {"deleted": address > 0}
