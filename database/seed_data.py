import sys
from pathlib import Path
from datetime import date, time

# Add backend directory to sys.path so we can import models and database
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from database import SessionLocal, engine, Base
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

def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Customer).count() > 0:
            print("Database already contains data. Skipping re-seeding.")
            return

        print("Seeding initial data for Vehicle Service Centre...")

        # 1. Customers
        customers = [
            Customer(
                name="Vedasri Reddy",
                email="vedasri@gmail.com",
                phone="9876543210",
                password="password123",
                address="Plot 45, Jubilee Hills, Hyderabad"
            ),
            Customer(
                name="Hasini Murthy",
                email="hasini@gmail.com",
                phone="9876543211",
                password="password123",
                address="B-12, Madhapur, Hyderabad"
            ),
            Customer(
                name="Rishitha Goud",
                email="rishitha@gmail.com",
                phone="9876543212",
                password="password123",
                address="Flat 304, Gachibowli, Hyderabad"
            ),
            Customer(
                name="Niharika Reddy",
                email="niharika@gmail.com",
                phone="9876543213",
                password="password123",
                address="Sector 2, Hitec City, Hyderabad"
            ),
        ]
        db.add_all(customers)
        db.commit()
        for c in customers:
            db.refresh(c)
        print(f"Created {len(customers)} customers.")

        # 2. Vehicles
        vehicles = [
            Vehicle(
                customer_id=customers[0].customer_id,
                registration_no="TS09AB1234",
                make="Honda",
                model="City ZX",
                year=2021,
                vehicle_type="Sedan"
            ),
            Vehicle(
                customer_id=customers[1].customer_id,
                registration_no="TS07XY5678",
                make="Hyundai",
                model="Creta SX",
                year=2022,
                vehicle_type="SUV"
            ),
            Vehicle(
                customer_id=customers[2].customer_id,
                registration_no="TS08CD9012",
                make="Maruti Suzuki",
                model="Swift Dzire",
                year=2020,
                vehicle_type="Sedan"
            ),
            Vehicle(
                customer_id=customers[3].customer_id,
                registration_no="TS10EF3456",
                make="Toyota",
                model="Innova Crysta",
                year=2023,
                vehicle_type="MUV"
            ),
        ]
        db.add_all(vehicles)
        db.commit()
        for v in vehicles:
            db.refresh(v)
        print(f"Created {len(vehicles)} vehicles.")

        # 3. Mechanics
        mechanics = [
            Mechanic(
                name="Rajesh Kumar",
                phone="9123456780",
                specialization="Engine Diagnostics & Transmission",
                status="Available"
            ),
            Mechanic(
                name="Anil Sharma",
                phone="9123456781",
                specialization="Brake Systems & Suspension",
                status="Available"
            ),
            Mechanic(
                name="Suresh Nair",
                phone="9123456782",
                specialization="Electrical & AC Systems",
                status="Busy"
            ),
            Mechanic(
                name="Vikram Singh",
                phone="9123456783",
                specialization="General Maintenance & Bodywork",
                status="Available"
            ),
        ]
        db.add_all(mechanics)
        db.commit()
        for m in mechanics:
            db.refresh(m)
        print(f"Created {len(mechanics)} mechanics.")

        # 4. Spare Parts
        spare_parts = [
            SparePart(part_name="Synthetic Engine Oil 5W30 (3.5L)", category="Fluids & Lubricants", quantity=25, unit_price=1850.00, reorder_level=5),
            SparePart(part_name="Ceramic Front Brake Pads", category="Braking", quantity=14, unit_price=1200.00, reorder_level=4),
            SparePart(part_name="Premium Oil Filter", category="Filters", quantity=30, unit_price=350.00, reorder_level=6),
            SparePart(part_name="High-Flow Air Filter", category="Filters", quantity=18, unit_price=450.00, reorder_level=5),
            SparePart(part_name="Iridium Spark Plugs (Set of 4)", category="Ignition", quantity=12, unit_price=1600.00, reorder_level=3),
            SparePart(part_name="All-Season Wiper Blades Pair", category="Accessories", quantity=8, unit_price=650.00, reorder_level=4),
            SparePart(part_name="Engine Coolant Pre-Mix (1L)", category="Fluids & Lubricants", quantity=3, unit_price=280.00, reorder_level=5), # Low stock
            SparePart(part_name="Maintenance-Free 12V Battery", category="Electrical", quantity=6, unit_price=4500.00, reorder_level=2),
        ]
        db.add_all(spare_parts)
        db.commit()
        for p in spare_parts:
            db.refresh(p)
        print(f"Created {len(spare_parts)} spare parts.")

        # 5. Appointments
        appointments = [
            Appointment(
                customer_id=customers[0].customer_id,
                vehicle_id=vehicles[0].vehicle_id,
                mechanic_id=mechanics[0].mechanic_id,
                appointment_date=date(2026, 9, 28),
                appointment_time=time(10, 0),
                service_type="Periodic Maintenance & Oil Service",
                status="Completed"
            ),
            Appointment(
                customer_id=customers[1].customer_id,
                vehicle_id=vehicles[1].vehicle_id,
                mechanic_id=mechanics[1].mechanic_id,
                appointment_date=date(2026, 9, 29),
                appointment_time=time(11, 30),
                service_type="Brake Pad Replacement & Inspection",
                status="In-Progress"
            ),
            Appointment(
                customer_id=customers[2].customer_id,
                vehicle_id=vehicles[2].vehicle_id,
                mechanic_id=mechanics[2].mechanic_id,
                appointment_date=date(2026, 9, 30),
                appointment_time=time(14, 0),
                service_type="AC Cooling Check & Electrical Diagnostic",
                status="Pending"
            ),
            Appointment(
                customer_id=customers[3].customer_id,
                vehicle_id=vehicles[3].vehicle_id,
                mechanic_id=mechanics[3].mechanic_id,
                appointment_date=date(2026, 9, 30),
                appointment_time=time(16, 0),
                service_type="Full Body Wash & Wheel Alignment",
                status="Confirmed"
            ),
        ]
        db.add_all(appointments)
        db.commit()
        for a in appointments:
            db.refresh(a)
        print(f"Created {len(appointments)} appointments.")

        # 6. Service Records
        service_records = [
            ServiceRecord(
                appointment_id=appointments[0].appointment_id,
                mechanic_id=mechanics[0].mechanic_id,
                inspection_notes="Completed 30-point safety check. Replaced engine oil and oil filter.",
                repair_details="Engine oil flushed and replaced. Replaced oil filter. Tested idle rpm.",
                service_status="Completed",
                start_date=date(2026, 9, 28),
                completion_date=date(2026, 9, 28)
            ),
            ServiceRecord(
                appointment_id=appointments[1].appointment_id,
                mechanic_id=mechanics[1].mechanic_id,
                inspection_notes="Front brake pads worn down to 2mm. Disc rotor in good health.",
                repair_details="Replacing front brake pads with ceramic pads and bleeding brake lines.",
                service_status="In-Progress",
                start_date=date(2026, 9, 29),
                completion_date=None
            ),
            ServiceRecord(
                appointment_id=appointments[2].appointment_id,
                mechanic_id=mechanics[2].mechanic_id,
                inspection_notes="Scheduled for AC compressor pressure test.",
                repair_details="Inspection pending arrival.",
                service_status="Inspection",
                start_date=date(2026, 9, 30),
                completion_date=None
            ),
        ]
        db.add_all(service_records)
        db.commit()
        for s in service_records:
            db.refresh(s)
        print(f"Created {len(service_records)} service records.")

        # 7. Service Parts
        service_parts = [
            ServicePart(service_id=service_records[0].service_id, part_id=spare_parts[0].part_id, quantity_used=1),
            ServicePart(service_id=service_records[0].service_id, part_id=spare_parts[2].part_id, quantity_used=1),
            ServicePart(service_id=service_records[1].service_id, part_id=spare_parts[1].part_id, quantity_used=1),
        ]
        db.add_all(service_parts)
        db.commit()
        print(f"Mapped {len(service_parts)} service parts.")

        # 8. Bills
        bill1 = Bill(
            service_id=service_records[0].service_id,
            customer_id=customers[0].customer_id,
            bill_date=date(2026, 9, 28),
            labour_charge=800.00,
            parts_charge=2200.00,  # 1850 + 350
            tax=360.00,            # 12% GST
            total_amount=3360.00
        )
        bill2 = Bill(
            service_id=service_records[1].service_id,
            customer_id=customers[1].customer_id,
            bill_date=date(2026, 9, 29),
            labour_charge=500.00,
            parts_charge=1200.00,
            tax=204.00,
            total_amount=1904.00
        )
        db.add_all([bill1, bill2])
        db.commit()
        db.refresh(bill1)
        db.refresh(bill2)
        print("Created 2 billing invoices.")

        # 9. Payment
        payment1 = Payment(
            bill_id=bill1.bill_id,
            payment_date=date(2026, 9, 28),
            amount=3360.00,
            payment_method="UPI / Online",
            payment_status="Completed"
        )
        payment2 = Payment(
            bill_id=bill2.bill_id,
            payment_date=date(2026, 9, 29),
            amount=1904.00,
            payment_method="Credit Card",
            payment_status="Pending"
        )
        db.add_all([payment1, payment2])
        db.commit()
        print("Created initial payments.")

        print("--> Database successfully seeded with 9 tables of interconnected records!")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
