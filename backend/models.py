from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Text, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15))
    password = Column(String(255))
    address = Column(String(255))

    vehicles = relationship("Vehicle", back_populates="customer", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="customer", cascade="all, delete-orphan")
    bills = relationship("Bill", back_populates="customer")

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }

class Vehicle(Base):
    __tablename__ = "vehicle"

    vehicle_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    registration_no = Column(String(20), unique=True, nullable=False, index=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer)
    vehicle_type = Column(String(30))

    customer = relationship("Customer", back_populates="vehicles")
    appointments = relationship("Appointment", back_populates="vehicle", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "customer_id": self.customer_id,
            "registration_no": self.registration_no,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "vehicle_type": self.vehicle_type
        }

class Mechanic(Base):
    __tablename__ = "mechanic"

    mechanic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(15))
    specialization = Column(String(100))
    status = Column(String(20), default="Available")

    appointments = relationship("Appointment", back_populates="mechanic")
    service_records = relationship("ServiceRecord", back_populates="mechanic")

    def to_dict(self):
        return {
            "mechanic_id": self.mechanic_id,
            "name": self.name,
            "phone": self.phone,
            "specialization": self.specialization,
            "status": self.status
        }

class Appointment(Base):
    __tablename__ = "appointment"

    appointment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicle.vehicle_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanic.mechanic_id"), nullable=True)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(Time, nullable=False)
    service_type = Column(String(100), nullable=False)
    status = Column(String(30), default="Pending")

    customer = relationship("Customer", back_populates="appointments")
    vehicle = relationship("Vehicle", back_populates="appointments")
    mechanic = relationship("Mechanic", back_populates="appointments")
    service_records = relationship("ServiceRecord", back_populates="appointment", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "customer_id": self.customer_id,
            "vehicle_id": self.vehicle_id,
            "mechanic_id": self.mechanic_id,
            "appointment_date": str(self.appointment_date) if self.appointment_date else None,
            "appointment_time": str(self.appointment_time) if self.appointment_time else None,
            "service_type": self.service_type,
            "status": self.status
        }

class ServiceRecord(Base):
    __tablename__ = "service_record"

    service_id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointment.appointment_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanic.mechanic_id"), nullable=False)
    inspection_notes = Column(Text)
    repair_details = Column(Text)
    service_status = Column(String(30), default="Inspection")
    start_date = Column(Date)
    completion_date = Column(Date)

    appointment = relationship("Appointment", back_populates="service_records")
    mechanic = relationship("Mechanic", back_populates="service_records")
    service_parts = relationship("ServicePart", back_populates="service_record", cascade="all, delete-orphan")
    bills = relationship("Bill", back_populates="service_record", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "appointment_id": self.appointment_id,
            "mechanic_id": self.mechanic_id,
            "inspection_notes": self.inspection_notes,
            "repair_details": self.repair_details,
            "service_status": self.service_status,
            "start_date": str(self.start_date) if self.start_date else None,
            "completion_date": str(self.completion_date) if self.completion_date else None
        }

class SparePart(Base):
    __tablename__ = "spare_part"

    part_id = Column(Integer, primary_key=True, index=True)
    part_name = Column(String(100), nullable=False)
    category = Column(String(50))
    quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Numeric(10, 2), nullable=False)
    reorder_level = Column(Integer, nullable=False, default=5)

    service_parts = relationship("ServicePart", back_populates="spare_part")

    def to_dict(self):
        return {
            "part_id": self.part_id,
            "part_name": self.part_name,
            "category": self.category,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price) if self.unit_price is not None else 0.0,
            "reorder_level": self.reorder_level
        }

class ServicePart(Base):
    __tablename__ = "service_part"

    service_id = Column(Integer, ForeignKey("service_record.service_id"), primary_key=True)
    part_id = Column(Integer, ForeignKey("spare_part.part_id"), primary_key=True)
    quantity_used = Column(Integer, nullable=False)

    service_record = relationship("ServiceRecord", back_populates="service_parts")
    spare_part = relationship("SparePart", back_populates="service_parts")

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "part_id": self.part_id,
            "quantity_used": self.quantity_used
        }

class Bill(Base):
    __tablename__ = "bill"

    bill_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("service_record.service_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"), nullable=False)
    bill_date = Column(Date)
    labour_charge = Column(Numeric(10, 2), default=0)
    parts_charge = Column(Numeric(10, 2), default=0)
    tax = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)

    service_record = relationship("ServiceRecord", back_populates="bills")
    customer = relationship("Customer", back_populates="bills")
    payments = relationship("Payment", back_populates="bill", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "bill_id": self.bill_id,
            "service_id": self.service_id,
            "customer_id": self.customer_id,
            "bill_date": str(self.bill_date) if self.bill_date else None,
            "labour_charge": float(self.labour_charge) if self.labour_charge is not None else 0.0,
            "parts_charge": float(self.parts_charge) if self.parts_charge is not None else 0.0,
            "tax": float(self.tax) if self.tax is not None else 0.0,
            "total_amount": float(self.total_amount) if self.total_amount is not None else 0.0
        }

class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bill.bill_id"), nullable=False)
    payment_date = Column(Date)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(30), nullable=False)
    payment_status = Column(String(30), default="Pending")

    bill = relationship("Bill", back_populates="payments")

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "bill_id": self.bill_id,
            "payment_date": str(self.payment_date) if self.payment_date else None,
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status
        }