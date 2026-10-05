import os
from pathlib import Path
from datetime import date, datetime, time
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from database import SessionLocal, engine, Base, ACTIVE_DB_TYPE, get_db
from models import (
    Customer,
    Vehicle,
    Mechanic,
    Appointment,
    ServiceRecord,
    SparePart,
    ServicePart,
    Bill,
    Payment
)
from schemas import (
    CustomerCreate, CustomerUpdate, CustomerResponse,
    VehicleCreate, VehicleUpdate, VehicleResponse,
    MechanicCreate, MechanicUpdate, MechanicResponse,
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
    ServiceRecordCreate, ServiceRecordUpdate, ServiceRecordResponse,
    SparePartCreate, SparePartUpdate, SparePartResponse,
    ServicePartCreate, ServicePartResponse,
    BillCreate, BillResponse,
    PaymentCreate, PaymentResponse,
    LoginRequest, LoginResponse,
    DashboardStats
)
from auth import verify_password, generate_token

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vehicle Service Centre Management System API",
    version="2.0.0",
    description="Backend API for Database Engineering PBL Review 3 & Review 4"
)

# CORS middleware for seamless browser frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

def parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str).strip(), "%Y-%m-%d").date()
    except Exception:
        return date.today()

def parse_time(time_str: Optional[str]) -> Optional[time]:
    if not time_str:
        return None
    try:
        ts = str(time_str).strip()
        if len(ts) == 5:
            return datetime.strptime(ts, "%H:%M").time()
        return datetime.strptime(ts, "%H:%M:%S").time()
    except Exception:
        return time(10, 0)

# ==========================================
# SYSTEM & AUTH ENDPOINTS
# ==========================================

@app.get("/system/status")
def system_status():
    return {
        "status": "online",
        "system": "Vehicle Service Centre Management System",
        "active_database": ACTIVE_DB_TYPE or "sqlite",
        "version": "2.0.0",
        "review": "Review 3 & Review 4 Ready"
    }

@app.post("/login", response_model=LoginResponse)
def login(creds: LoginRequest, db: Session = Depends(get_db)):
    # Support admin login
    if creds.email == "admin@servicecentre.com" and creds.password in ("admin123", "VEDA@2007", "admin"):
        return LoginResponse(
            token=generate_token(1, "admin"),
            user_id=1,
            name="System Administrator",
            email=creds.email,
            role="admin"
        )

    # Check customer
    customer = db.query(Customer).filter(Customer.email == creds.email).first()
    if customer:
        if not customer.password or verify_password(creds.password, customer.password):
            return LoginResponse(
                token=generate_token(customer.customer_id, "customer"),
                user_id=customer.customer_id,
                name=customer.name,
                email=customer.email,
                role="customer"
            )

    # Check mechanic
    mechanic = db.query(Mechanic).filter(Mechanic.name.ilike(creds.email.split("@")[0])).first()
    if mechanic and creds.password in ("mechanic123", "password123", "admin123"):
        return LoginResponse(
            token=generate_token(mechanic.mechanic_id, "mechanic"),
            user_id=mechanic.mechanic_id,
            name=mechanic.name,
            email=creds.email,
            role="mechanic"
        )

    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_cust = db.query(func.count(Customer.customer_id)).scalar() or 0
    total_veh = db.query(func.count(Vehicle.vehicle_id)).scalar() or 0
    total_appt = db.query(func.count(Appointment.appointment_id)).scalar() or 0
    active_repairs = db.query(func.count(ServiceRecord.service_id)).filter(
        ServiceRecord.service_status.in_(["Inspection", "In-Progress", "Pending Parts"])
    ).scalar() or 0
    avail_mech = db.query(func.count(Mechanic.mechanic_id)).filter(
        Mechanic.status == "Available"
    ).scalar() or 0
    total_parts = db.query(func.sum(SparePart.quantity)).scalar() or 0
    low_stock = db.query(func.count(SparePart.part_id)).filter(
        SparePart.quantity <= SparePart.reorder_level
    ).scalar() or 0
    revenue = db.query(func.sum(Payment.amount)).filter(
        Payment.payment_status == "Completed"
    ).scalar() or 0.0

    return DashboardStats(
        total_customers=total_cust,
        total_vehicles=total_veh,
        total_appointments=total_appt,
        active_repairs=active_repairs,
        available_mechanics=avail_mech,
        total_parts_stock=int(total_parts),
        low_stock_parts=low_stock,
        total_revenue=float(revenue),
        active_database=ACTIVE_DB_TYPE or "sqlite"
    )

# ==========================================
# 1. CUSTOMERS
# ==========================================

@app.get("/customers", response_model=List[CustomerResponse])
def get_customers(q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Customer)
    if q:
        query = query.filter(or_(Customer.name.ilike(f"%{q}%"), Customer.email.ilike(f"%{q}%"), Customer.phone.ilike(f"%{q}%")))
    return query.all()

@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    customer = Customer(
        name=data.name,
        email=data.email,
        phone=data.phone,
        password=data.password or "password123",
        address=data.address
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    if data.name is not None: customer.name = data.name
    if data.email is not None: customer.email = data.email
    if data.phone is not None: customer.phone = data.phone
    if data.address is not None: customer.address = data.address
    db.commit()
    db.refresh(customer)
    return customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully", "customer_id": customer_id}

# ==========================================
# 2. VEHICLES
# ==========================================

@app.get("/vehicles", response_model=List[VehicleResponse])
def get_vehicles(customer_id: Optional[int] = None, q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Vehicle)
    if customer_id:
        query = query.filter(Vehicle.customer_id == customer_id)
    if q:
        query = query.filter(or_(Vehicle.registration_no.ilike(f"%{q}%"), Vehicle.make.ilike(f"%{q}%"), Vehicle.model.ilike(f"%{q}%")))
    return query.all()

@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

@app.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    existing = db.query(Vehicle).filter(Vehicle.registration_no == data.registration_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vehicle registration number already exists")
    cust = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Associated customer not found")
    vehicle = Vehicle(
        customer_id=data.customer_id,
        registration_no=data.registration_no.upper().strip(),
        make=data.make,
        model=data.model,
        year=data.year,
        vehicle_type=data.vehicle_type
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle

@app.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(vehicle_id: int, data: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if data.registration_no is not None: vehicle.registration_no = data.registration_no.upper().strip()
    if data.make is not None: vehicle.make = data.make
    if data.model is not None: vehicle.model = data.model
    if data.year is not None: vehicle.year = data.year
    if data.vehicle_type is not None: vehicle.vehicle_type = data.vehicle_type
    db.commit()
    db.refresh(vehicle)
    return vehicle

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(vehicle)
    db.commit()
    return {"message": "Vehicle deleted successfully", "vehicle_id": vehicle_id}

# ==========================================
# 3. MECHANICS
# ==========================================

@app.get("/mechanics", response_model=List[MechanicResponse])
def get_mechanics(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Mechanic)
    if status:
        query = query.filter(Mechanic.status == status)
    return query.all()

@app.get("/mechanics/{mechanic_id}", response_model=MechanicResponse)
def get_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return mechanic

@app.post("/mechanics", response_model=MechanicResponse, status_code=status.HTTP_201_CREATED)
def create_mechanic(data: MechanicCreate, db: Session = Depends(get_db)):
    mechanic = Mechanic(
        name=data.name,
        phone=data.phone,
        specialization=data.specialization,
        status=data.status
    )
    db.add(mechanic)
    db.commit()
    db.refresh(mechanic)
    return mechanic

@app.put("/mechanics/{mechanic_id}", response_model=MechanicResponse)
def update_mechanic(mechanic_id: int, data: MechanicUpdate, db: Session = Depends(get_db)):
    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    if data.name is not None: mechanic.name = data.name
    if data.phone is not None: mechanic.phone = data.phone
    if data.specialization is not None: mechanic.specialization = data.specialization
    if data.status is not None: mechanic.status = data.status
    db.commit()
    db.refresh(mechanic)
    return mechanic

@app.delete("/mechanics/{mechanic_id}")
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(Mechanic).filter(Mechanic.mechanic_id == mechanic_id).first()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    db.delete(mechanic)
    db.commit()
    return {"message": "Mechanic deleted successfully", "mechanic_id": mechanic_id}

# ==========================================
# 4. APPOINTMENTS
# ==========================================

@app.get("/appointments", response_model=List[AppointmentResponse])
def get_appointments(status: Optional[str] = None, customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Appointment)
    if status:
        query = query.filter(Appointment.status == status)
    if customer_id:
        query = query.filter(Appointment.customer_id == customer_id)
    
    appts = query.order_by(Appointment.appointment_date.desc()).all()
    results = []
    for a in appts:
        cust = db.query(Customer).filter(Customer.customer_id == a.customer_id).first()
        veh = db.query(Vehicle).filter(Vehicle.vehicle_id == a.vehicle_id).first()
        mech = db.query(Mechanic).filter(Mechanic.mechanic_id == a.mechanic_id).first() if a.mechanic_id else None
        results.append(AppointmentResponse(
            appointment_id=a.appointment_id,
            customer_id=a.customer_id,
            vehicle_id=a.vehicle_id,
            mechanic_id=a.mechanic_id,
            appointment_date=str(a.appointment_date),
            appointment_time=str(a.appointment_time),
            service_type=a.service_type,
            status=a.status,
            customer_name=cust.name if cust else "Unknown",
            vehicle_reg=veh.registration_no if veh else "Unknown",
            mechanic_name=mech.name if mech else "Not Assigned"
        ))
    return results

@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    a = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Appointment not found")
    cust = db.query(Customer).filter(Customer.customer_id == a.customer_id).first()
    veh = db.query(Vehicle).filter(Vehicle.vehicle_id == a.vehicle_id).first()
    mech = db.query(Mechanic).filter(Mechanic.mechanic_id == a.mechanic_id).first() if a.mechanic_id else None
    return AppointmentResponse(
        appointment_id=a.appointment_id,
        customer_id=a.customer_id,
        vehicle_id=a.vehicle_id,
        mechanic_id=a.mechanic_id,
        appointment_date=str(a.appointment_date),
        appointment_time=str(a.appointment_time),
        service_type=a.service_type,
        status=a.status,
        customer_name=cust.name if cust else "Unknown",
        vehicle_reg=veh.registration_no if veh else "Unknown",
        mechanic_name=mech.name if mech else "Not Assigned"
    )

@app.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    cust = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    veh = db.query(Vehicle).filter(Vehicle.vehicle_id == data.vehicle_id).first()
    if not veh:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    appt = Appointment(
        customer_id=data.customer_id,
        vehicle_id=data.vehicle_id,
        mechanic_id=data.mechanic_id,
        appointment_date=parse_date(data.appointment_date),
        appointment_time=parse_time(data.appointment_time),
        service_type=data.service_type,
        status=data.status or "Pending"
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)

    # Automatically create an initial ServiceRecord when appointment is booked
    mech_id = data.mechanic_id
    if not mech_id:
        first_mech = db.query(Mechanic).first()
        mech_id = first_mech.mechanic_id if first_mech else 1

    svc = ServiceRecord(
        appointment_id=appt.appointment_id,
        mechanic_id=mech_id,
        inspection_notes=f"Initial booking for {data.service_type}",
        repair_details="Scheduled for service",
        service_status="Inspection",
        start_date=parse_date(data.appointment_date)
    )
    db.add(svc)
    db.commit()

    mech = db.query(Mechanic).filter(Mechanic.mechanic_id == appt.mechanic_id).first() if appt.mechanic_id else None
    return AppointmentResponse(
        appointment_id=appt.appointment_id,
        customer_id=appt.customer_id,
        vehicle_id=appt.vehicle_id,
        mechanic_id=appt.mechanic_id,
        appointment_date=str(appt.appointment_date),
        appointment_time=str(appt.appointment_time),
        service_type=appt.service_type,
        status=appt.status,
        customer_name=cust.name,
        vehicle_reg=veh.registration_no,
        mechanic_name=mech.name if mech else "Not Assigned"
    )

@app.put("/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if data.mechanic_id is not None: appt.mechanic_id = data.mechanic_id
    if data.appointment_date is not None: appt.appointment_date = parse_date(data.appointment_date)
    if data.appointment_time is not None: appt.appointment_time = parse_time(data.appointment_time)
    if data.service_type is not None: appt.service_type = data.service_type
    if data.status is not None: appt.status = data.status
    db.commit()
    db.refresh(appt)

    cust = db.query(Customer).filter(Customer.customer_id == appt.customer_id).first()
    veh = db.query(Vehicle).filter(Vehicle.vehicle_id == appt.vehicle_id).first()
    mech = db.query(Mechanic).filter(Mechanic.mechanic_id == appt.mechanic_id).first() if appt.mechanic_id else None
    return AppointmentResponse(
        appointment_id=appt.appointment_id,
        customer_id=appt.customer_id,
        vehicle_id=appt.vehicle_id,
        mechanic_id=appt.mechanic_id,
        appointment_date=str(appt.appointment_date),
        appointment_time=str(appt.appointment_time),
        service_type=appt.service_type,
        status=appt.status,
        customer_name=cust.name if cust else "Unknown",
        vehicle_reg=veh.registration_no if veh else "Unknown",
        mechanic_name=mech.name if mech else "Not Assigned"
    )

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"message": "Appointment deleted successfully", "appointment_id": appointment_id}

# ==========================================
# 5. SERVICE RECORDS
# ==========================================

@app.get("/service-records", response_model=List[ServiceRecordResponse])
def get_service_records(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ServiceRecord)
    if status:
        query = query.filter(ServiceRecord.service_status == status)
    records = query.order_by(ServiceRecord.service_id.desc()).all()
    return [
        ServiceRecordResponse(
            service_id=r.service_id,
            appointment_id=r.appointment_id,
            mechanic_id=r.mechanic_id,
            inspection_notes=r.inspection_notes,
            repair_details=r.repair_details,
            service_status=r.service_status,
            start_date=str(r.start_date) if r.start_date else None,
            completion_date=str(r.completion_date) if r.completion_date else None
        ) for r in records
    ]

@app.get("/service-records/{service_id}", response_model=ServiceRecordResponse)
def get_service_record(service_id: int, db: Session = Depends(get_db)):
    r = db.query(ServiceRecord).filter(ServiceRecord.service_id == service_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Service record not found")
    return ServiceRecordResponse(
        service_id=r.service_id,
        appointment_id=r.appointment_id,
        mechanic_id=r.mechanic_id,
        inspection_notes=r.inspection_notes,
        repair_details=r.repair_details,
        service_status=r.service_status,
        start_date=str(r.start_date) if r.start_date else None,
        completion_date=str(r.completion_date) if r.completion_date else None
    )

@app.post("/service-records", response_model=ServiceRecordResponse, status_code=status.HTTP_201_CREATED)
def create_service_record(data: ServiceRecordCreate, db: Session = Depends(get_db)):
    record = ServiceRecord(
        appointment_id=data.appointment_id,
        mechanic_id=data.mechanic_id,
        inspection_notes=data.inspection_notes,
        repair_details=data.repair_details,
        service_status=data.service_status,
        start_date=parse_date(data.start_date),
        completion_date=parse_date(data.completion_date)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return ServiceRecordResponse(
        service_id=record.service_id,
        appointment_id=record.appointment_id,
        mechanic_id=record.mechanic_id,
        inspection_notes=record.inspection_notes,
        repair_details=record.repair_details,
        service_status=record.service_status,
        start_date=str(record.start_date) if record.start_date else None,
        completion_date=str(record.completion_date) if record.completion_date else None
    )

@app.put("/service-records/{service_id}", response_model=ServiceRecordResponse)
def update_service_record(service_id: int, data: ServiceRecordUpdate, db: Session = Depends(get_db)):
    r = db.query(ServiceRecord).filter(ServiceRecord.service_id == service_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Service record not found")
    if data.mechanic_id is not None: r.mechanic_id = data.mechanic_id
    if data.inspection_notes is not None: r.inspection_notes = data.inspection_notes
    if data.repair_details is not None: r.repair_details = data.repair_details
    if data.service_status is not None:
        r.service_status = data.service_status
        if data.service_status == "Completed" and not r.completion_date:
            r.completion_date = date.today()
    if data.start_date is not None: r.start_date = parse_date(data.start_date)
    if data.completion_date is not None: r.completion_date = parse_date(data.completion_date)
    db.commit()
    db.refresh(r)
    return ServiceRecordResponse(
        service_id=r.service_id,
        appointment_id=r.appointment_id,
        mechanic_id=r.mechanic_id,
        inspection_notes=r.inspection_notes,
        repair_details=r.repair_details,
        service_status=r.service_status,
        start_date=str(r.start_date) if r.start_date else None,
        completion_date=str(r.completion_date) if r.completion_date else None
    )

@app.delete("/service-records/{service_id}")
def delete_service_record(service_id: int, db: Session = Depends(get_db)):
    r = db.query(ServiceRecord).filter(ServiceRecord.service_id == service_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Service record not found")
    db.delete(r)
    db.commit()
    return {"message": "Service record deleted", "service_id": service_id}

# ==========================================
# 6. SPARE PARTS
# ==========================================

@app.get("/spare-parts", response_model=List[SparePartResponse])
def get_spare_parts(low_stock: bool = False, q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(SparePart)
    if low_stock:
        query = query.filter(SparePart.quantity <= SparePart.reorder_level)
    if q:
        query = query.filter(or_(SparePart.part_name.ilike(f"%{q}%"), SparePart.category.ilike(f"%{q}%")))
    return query.all()

@app.get("/spare-parts/{part_id}", response_model=SparePartResponse)
def get_spare_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(SparePart).filter(SparePart.part_id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Spare part not found")
    return part

@app.post("/spare-parts", response_model=SparePartResponse, status_code=status.HTTP_201_CREATED)
def create_spare_part(data: SparePartCreate, db: Session = Depends(get_db)):
    part = SparePart(
        part_name=data.part_name,
        category=data.category,
        quantity=data.quantity,
        unit_price=data.unit_price,
        reorder_level=data.reorder_level
    )
    db.add(part)
    db.commit()
    db.refresh(part)
    return part

@app.put("/spare-parts/{part_id}", response_model=SparePartResponse)
def update_spare_part(part_id: int, data: SparePartUpdate, db: Session = Depends(get_db)):
    part = db.query(SparePart).filter(SparePart.part_id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Spare part not found")
    if data.part_name is not None: part.part_name = data.part_name
    if data.category is not None: part.category = data.category
    if data.quantity is not None: part.quantity = data.quantity
    if data.unit_price is not None: part.unit_price = data.unit_price
    if data.reorder_level is not None: part.reorder_level = data.reorder_level
    db.commit()
    db.refresh(part)
    return part

@app.delete("/spare-parts/{part_id}")
def delete_spare_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(SparePart).filter(SparePart.part_id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Spare part not found")
    db.delete(part)
    db.commit()
    return {"message": "Spare part deleted", "part_id": part_id}

# ==========================================
# 7. SERVICE PARTS (MAPPING)
# ==========================================

@app.get("/service-parts", response_model=List[ServicePartResponse])
def get_service_parts(service_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(ServicePart)
    if service_id:
        query = query.filter(ServicePart.service_id == service_id)
    return query.all()

@app.post("/service-parts", response_model=ServicePartResponse, status_code=status.HTTP_201_CREATED)
def create_service_part(data: ServicePartCreate, db: Session = Depends(get_db)):
    part = db.query(SparePart).filter(SparePart.part_id == data.part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    if part.quantity < data.quantity_used:
        raise HTTPException(status_code=400, detail=f"Insufficient inventory. Only {part.quantity} available.")

    # Deduct stock
    part.quantity -= data.quantity_used

    service_part = ServicePart(
        service_id=data.service_id,
        part_id=data.part_id,
        quantity_used=data.quantity_used
    )
    db.add(service_part)
    db.commit()
    return service_part

# ==========================================
# 8. BILLING & INVOICING
# ==========================================

@app.get("/bills", response_model=List[BillResponse])
def get_bills(db: Session = Depends(get_db)):
    bills = db.query(Bill).order_by(Bill.bill_id.desc()).all()
    return [
        BillResponse(
            bill_id=b.bill_id,
            service_id=b.service_id,
            customer_id=b.customer_id,
            bill_date=str(b.bill_date) if b.bill_date else None,
            labour_charge=float(b.labour_charge),
            parts_charge=float(b.parts_charge),
            tax=float(b.tax),
            total_amount=float(b.total_amount)
        ) for b in bills
    ]

@app.get("/bills/{bill_id}/invoice")
def get_detailed_invoice(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    cust = db.query(Customer).filter(Customer.customer_id == bill.customer_id).first()
    svc = db.query(ServiceRecord).filter(ServiceRecord.service_id == bill.service_id).first()
    appt = db.query(Appointment).filter(Appointment.appointment_id == svc.appointment_id).first() if svc else None
    veh = db.query(Vehicle).filter(Vehicle.vehicle_id == appt.vehicle_id).first() if appt else None
    mech = db.query(Mechanic).filter(Mechanic.mechanic_id == svc.mechanic_id).first() if svc else None
    
    # Retrieve used parts
    service_parts = db.query(ServicePart).filter(ServicePart.service_id == bill.service_id).all()
    parts_breakdown = []
    for sp in service_parts:
        part = db.query(SparePart).filter(SparePart.part_id == sp.part_id).first()
        if part:
            parts_breakdown.append({
                "part_name": part.part_name,
                "unit_price": float(part.unit_price),
                "quantity": sp.quantity_used,
                "subtotal": float(part.unit_price) * sp.quantity_used
            })

    # Retrieve payments
    payments = db.query(Payment).filter(Payment.bill_id == bill.bill_id).all()
    payment_status = "Paid" if any(p.payment_status == "Completed" for p in payments) else "Pending"

    return {
        "invoice_number": f"INV-{bill.bill_id:05d}",
        "bill_id": bill.bill_id,
        "date": str(bill.bill_date or date.today()),
        "customer": {
            "customer_id": cust.customer_id if cust else None,
            "name": cust.name if cust else "Valued Customer",
            "email": cust.email if cust else "",
            "phone": cust.phone if cust else "",
            "address": cust.address if cust else ""
        },
        "vehicle": {
            "registration_no": veh.registration_no if veh else "N/A",
            "make": veh.make if veh else "N/A",
            "model": veh.model if veh else "N/A",
            "year": veh.year if veh else "N/A"
        },
        "service": {
            "service_id": svc.service_id if svc else None,
            "service_type": appt.service_type if appt else "General Service",
            "mechanic_name": mech.name if mech else "Staff",
            "repair_details": svc.repair_details if svc else ""
        },
        "parts_used": parts_breakdown,
        "charges": {
            "parts_charge": float(bill.parts_charge),
            "labour_charge": float(bill.labour_charge),
            "tax": float(bill.tax),
            "total_amount": float(bill.total_amount)
        },
        "payment_status": payment_status,
        "payments": [p.to_dict() for p in payments]
    }

@app.post("/bills", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
def create_bill(data: BillCreate, db: Session = Depends(get_db)):
    bill = Bill(
        service_id=data.service_id,
        customer_id=data.customer_id,
        labour_charge=data.labour_charge,
        parts_charge=data.parts_charge,
        tax=data.tax,
        total_amount=data.total_amount,
        bill_date=parse_date(data.bill_date) or date.today()
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return BillResponse(
        bill_id=bill.bill_id,
        service_id=bill.service_id,
        customer_id=bill.customer_id,
        bill_date=str(bill.bill_date),
        labour_charge=float(bill.labour_charge),
        parts_charge=float(bill.parts_charge),
        tax=float(bill.tax),
        total_amount=float(bill.total_amount)
    )

@app.delete("/bills/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    db.delete(bill)
    db.commit()
    return {"message": "Bill deleted", "bill_id": bill_id}

# ==========================================
# 9. PAYMENTS
# ==========================================

@app.get("/payments", response_model=List[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).order_by(Payment.payment_id.desc()).all()
    return [
        PaymentResponse(
            payment_id=p.payment_id,
            bill_id=p.bill_id,
            payment_date=str(p.payment_date) if p.payment_date else None,
            amount=float(p.amount),
            payment_method=p.payment_method,
            payment_status=p.payment_status
        ) for p in payments
    ]

@app.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == data.bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    payment = Payment(
        bill_id=data.bill_id,
        amount=data.amount,
        payment_method=data.payment_method,
        payment_status=data.payment_status or "Completed",
        payment_date=parse_date(data.payment_date) or date.today()
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return PaymentResponse(
        payment_id=payment.payment_id,
        bill_id=payment.bill_id,
        payment_date=str(payment.payment_date),
        amount=float(payment.amount),
        payment_method=payment.payment_method,
        payment_status=payment.payment_status
    )

# ==========================================
# FRONTEND STATIC FILES & SPA ROUTE
# ==========================================

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    def serve_frontend():
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Vehicle Service Centre Management System API is running"}

    @app.get("/styles.css")
    def get_styles():
        return FileResponse(FRONTEND_DIR / "styles.css", media_type="text/css")

    @app.get("/app.js")
    def get_app_js():
        return FileResponse(FRONTEND_DIR / "app.js", media_type="application/javascript")
else:
    @app.get("/")
    def home():
        return {"message": "Vehicle Service Centre Management System API is running"}