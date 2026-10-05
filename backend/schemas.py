from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import date, time

# --- Base & Create Schemas ---
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: Optional[str] = "password123"

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerResponse(CustomerBase):
    customer_id: int
    model_config = ConfigDict(from_attributes=True)


class VehicleBase(BaseModel):
    customer_id: int
    registration_no: str
    make: str
    model: str
    year: Optional[int] = None
    vehicle_type: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    registration_no: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    vehicle_type: Optional[str] = None

class VehicleResponse(VehicleBase):
    vehicle_id: int
    model_config = ConfigDict(from_attributes=True)


class MechanicBase(BaseModel):
    name: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    status: str = "Available"

class MechanicCreate(MechanicBase):
    pass

class MechanicUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    status: Optional[str] = None

class MechanicResponse(MechanicBase):
    mechanic_id: int
    model_config = ConfigDict(from_attributes=True)


class AppointmentBase(BaseModel):
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int] = None
    appointment_date: str
    appointment_time: str
    service_type: str
    status: str = "Pending"

class AppointmentCreate(BaseModel):
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int] = None
    appointment_date: str
    appointment_time: str
    service_type: str
    status: Optional[str] = "Pending"

class AppointmentUpdate(BaseModel):
    mechanic_id: Optional[int] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    service_type: Optional[str] = None
    status: Optional[str] = None

class AppointmentResponse(BaseModel):
    appointment_id: int
    customer_id: int
    vehicle_id: int
    mechanic_id: Optional[int] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    service_type: str
    status: str
    customer_name: Optional[str] = None
    vehicle_reg: Optional[str] = None
    mechanic_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ServiceRecordCreate(BaseModel):
    appointment_id: int
    mechanic_id: int
    inspection_notes: Optional[str] = None
    repair_details: Optional[str] = None
    service_status: str = "Inspection"
    start_date: Optional[str] = None
    completion_date: Optional[str] = None

class ServiceRecordUpdate(BaseModel):
    mechanic_id: Optional[int] = None
    inspection_notes: Optional[str] = None
    repair_details: Optional[str] = None
    service_status: Optional[str] = None
    start_date: Optional[str] = None
    completion_date: Optional[str] = None

class ServiceRecordResponse(BaseModel):
    service_id: int
    appointment_id: int
    mechanic_id: int
    inspection_notes: Optional[str] = None
    repair_details: Optional[str] = None
    service_status: str
    start_date: Optional[str] = None
    completion_date: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class SparePartBase(BaseModel):
    part_name: str
    category: Optional[str] = None
    quantity: int = 0
    unit_price: float
    reorder_level: int = 5

class SparePartCreate(SparePartBase):
    pass

class SparePartUpdate(BaseModel):
    part_name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    reorder_level: Optional[int] = None

class SparePartResponse(SparePartBase):
    part_id: int
    model_config = ConfigDict(from_attributes=True)


class ServicePartCreate(BaseModel):
    service_id: int
    part_id: int
    quantity_used: int

class ServicePartResponse(BaseModel):
    service_id: int
    part_id: int
    quantity_used: int
    model_config = ConfigDict(from_attributes=True)


class BillCreate(BaseModel):
    service_id: int
    customer_id: int
    labour_charge: float = 0.0
    parts_charge: float = 0.0
    tax: float = 0.0
    total_amount: float
    bill_date: Optional[str] = None

class BillResponse(BaseModel):
    bill_id: int
    service_id: int
    customer_id: int
    bill_date: Optional[str] = None
    labour_charge: float
    parts_charge: float
    tax: float
    total_amount: float
    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(BaseModel):
    bill_id: int
    amount: float
    payment_method: str
    payment_status: str = "Completed"
    payment_date: Optional[str] = None

class PaymentResponse(BaseModel):
    payment_id: int
    bill_id: int
    payment_date: Optional[str] = None
    amount: float
    payment_method: str
    payment_status: str
    model_config = ConfigDict(from_attributes=True)


# --- Auth & Dashboard Schemas ---
class LoginRequest(BaseModel):
    email: str
    password: str
    role: Optional[str] = "admin"  # "admin", "mechanic", or "customer"

class LoginResponse(BaseModel):
    token: str
    user_id: int
    name: str
    email: str
    role: str

class DashboardStats(BaseModel):
    total_customers: int
    total_vehicles: int
    total_appointments: int
    active_repairs: int
    available_mechanics: int
    total_parts_stock: int
    low_stock_parts: int
    total_revenue: float
    active_database: str