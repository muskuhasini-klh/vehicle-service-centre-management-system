-- =========================================================
-- Vehicle Service Centre Management System
-- Database Schema (PostgreSQL)
-- Database Engineering PBL - 9 Tables
-- =========================================================

-- 1. Customer Table
CREATE TABLE IF NOT EXISTS customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    password VARCHAR(255),
    address VARCHAR(255)
);

-- 2. Vehicle Table
CREATE TABLE IF NOT EXISTS vehicle (
    vehicle_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    registration_no VARCHAR(20) UNIQUE NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT,
    vehicle_type VARCHAR(30),
    CONSTRAINT fk_vehicle_customer FOREIGN KEY (customer_id) 
        REFERENCES customer(customer_id) ON DELETE CASCADE
);

-- 3. Mechanic Table
CREATE TABLE IF NOT EXISTS mechanic (
    mechanic_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    specialization VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Available'
);

-- 4. Appointment Table
CREATE TABLE IF NOT EXISTS appointment (
    appointment_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    mechanic_id INT,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending',
    CONSTRAINT fk_appointment_customer FOREIGN KEY (customer_id) 
        REFERENCES customer(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_appointment_vehicle FOREIGN KEY (vehicle_id) 
        REFERENCES vehicle(vehicle_id) ON DELETE CASCADE,
    CONSTRAINT fk_appointment_mechanic FOREIGN KEY (mechanic_id) 
        REFERENCES mechanic(mechanic_id) ON DELETE SET NULL
);

-- 5. Service Record Table
CREATE TABLE IF NOT EXISTS service_record (
    service_id SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL,
    mechanic_id INT NOT NULL,
    inspection_notes TEXT,
    repair_details TEXT,
    service_status VARCHAR(30) DEFAULT 'Inspection',
    start_date DATE,
    completion_date DATE,
    CONSTRAINT fk_service_appointment FOREIGN KEY (appointment_id) 
        REFERENCES appointment(appointment_id) ON DELETE CASCADE,
    CONSTRAINT fk_service_mechanic FOREIGN KEY (mechanic_id) 
        REFERENCES mechanic(mechanic_id) ON DELETE RESTRICT
);

-- 6. Spare Part Table
CREATE TABLE IF NOT EXISTS spare_part (
    part_id SERIAL PRIMARY KEY,
    part_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    quantity INT NOT NULL DEFAULT 0,
    unit_price NUMERIC(10, 2) NOT NULL,
    reorder_level INT NOT NULL DEFAULT 5
);

-- 7. Service Part Table (Associative Entity)
CREATE TABLE IF NOT EXISTS service_part (
    service_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity_used INT NOT NULL,
    PRIMARY KEY (service_id, part_id),
    CONSTRAINT fk_servicepart_service FOREIGN KEY (service_id) 
        REFERENCES service_record(service_id) ON DELETE CASCADE,
    CONSTRAINT fk_servicepart_part FOREIGN KEY (part_id) 
        REFERENCES spare_part(part_id) ON DELETE RESTRICT
);

-- 8. Bill Table
CREATE TABLE IF NOT EXISTS bill (
    bill_id SERIAL PRIMARY KEY,
    service_id INT NOT NULL,
    customer_id INT NOT NULL,
    bill_date DATE,
    labour_charge NUMERIC(10, 2) DEFAULT 0.00,
    parts_charge NUMERIC(10, 2) DEFAULT 0.00,
    tax NUMERIC(10, 2) DEFAULT 0.00,
    total_amount NUMERIC(10, 2) NOT NULL,
    CONSTRAINT fk_bill_service FOREIGN KEY (service_id) 
        REFERENCES service_record(service_id) ON DELETE CASCADE,
    CONSTRAINT fk_bill_customer FOREIGN KEY (customer_id) 
        REFERENCES customer(customer_id) ON DELETE RESTRICT
);

-- 9. Payment Table
CREATE TABLE IF NOT EXISTS payment (
    payment_id SERIAL PRIMARY KEY,
    bill_id INT NOT NULL,
    payment_date DATE,
    amount NUMERIC(10, 2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    payment_status VARCHAR(30) DEFAULT 'Pending',
    CONSTRAINT fk_payment_bill FOREIGN KEY (bill_id) 
        REFERENCES bill(bill_id) ON DELETE CASCADE
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_customer_email ON customer(email);
CREATE INDEX IF NOT EXISTS idx_vehicle_reg ON vehicle(registration_no);
CREATE INDEX IF NOT EXISTS idx_appointment_date ON appointment(appointment_date);
CREATE INDEX IF NOT EXISTS idx_service_status ON service_record(service_status);
