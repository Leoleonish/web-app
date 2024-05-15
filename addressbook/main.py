from fastapi import FastAPI, Depends, HTTPException
from .database import get_db, engine
from sqlalchemy.orm import Session
from . import models
from .schemas import Address

app = FastAPI()


models.Base.metadata.create_all(engine)


@app.post('/addresses')
async def create_address(address: Address, db: Session = Depends(get_db)):
        try:
                new_add = models.Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
                db.add(new_add)
                db.commit()
                db.refresh(new_add)
                return new_add
        except ValueError as e:
                raise HTTPException(status_code=400, detail=f'{e}')


@app.get('/address')
async def all(db: Session = Depends(get_db)):
        return db.query(models.Address).all()


@app.get('/address/{id}/', status_code=200)
async def one(id, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@app.put('/address/{id}/')
async def update(id, a1: Address, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id==id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    address.name = a1.name
    address.latitude = a1.latitude
    address.longitude = a1.longitude
    db.commit()
    return db.query(models.Address).filter(models.Address.id==id).first()


@app.delete('/address/{id}')
async def destroy(id, db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id==id)
    if not address.first():
        raise HTTPException(status_code=404, detail="Address not found")
    address.delete()
    db.commit()
    return {"data": 'empty'}


def calculate_distance(lat1,lon1,lat2,lon2):
    from math import radians, sin, cos, acos, sqrt

    R = 6371      #radius of the world in km

    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)

    distance_lat = lat2 - lat1
    distance_lon = lon1 - lon2

    a = sin(distance_lat / 2) * sin(distance_lon / 2) + cos(lat1) * cos(lat2) * sin(distance_lon / 2) * sin(distance_lon / 2)
    c = 2 * acos(sqrt(a))

    return R * c


@app.get('/address/near', response_model=List[Address])
async def get_address_near(latitude: float, longitude: float, radius: float, db: Session = Depends(get_db)):
    addresses = db.query(models.Address).all()
    return [
        address for address in addresses if calculate_distance(latitude, longitude, address.longitude, address.longitude) <= radius
    ]

