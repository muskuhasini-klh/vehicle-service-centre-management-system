// =========================================================
// Vehicle Service Centre Management System - Frontend App Engine
// =========================================================

const API_BASE = window.location.origin.includes("5500") || window.location.protocol === "file:"
  ? "http://127.0.0.1:8000"
  : window.location.origin;

let state = {
  customers: [],
  vehicles: [],
  mechanics: [],
  appointments: [],
  services: [],
  spareParts: [],
  bills: [],
  stats: null
};

// Initialize app on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  initApp();
  // Set default appointment date to tomorrow
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const dateInput = document.getElementById("appt-date");
  if (dateInput) {
    dateInput.value = tomorrow.toISOString().split("T")[0];
  }
});

async function initApp() {
  await checkSystemStatus();
  await loadAllData();
}

async function checkSystemStatus() {
  try {
    const res = await fetch(`${API_BASE}/system/status`);
    if (res.ok) {
      const data = await res.json();
      const badge = document.getElementById("active-db-text");
      if (badge) {
        badge.textContent = `DB: ${data.active_database.toUpperCase()} (Online)`;
      }
    }
  } catch (err) {
    console.warn("API check failed:", err);
    const badge = document.getElementById("active-db-text");
    if (badge) badge.textContent = "API Disconnected";
  }
}

async function loadAllData() {
  await Promise.all([
    loadDashboard(),
    loadAppointments(),
    loadServices(),
    loadCustomers(),
    loadVehicles(),
    loadInventory(),
    loadMechanics(),
    loadBills()
  ]);
  populateDropdowns();
}

// ---------------------------------------------------------
// Navigation & Tab Switching
// ---------------------------------------------------------
function switchTab(tabId) {
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tabId);
  });
  document.querySelectorAll(".tab-pane").forEach(pane => {
    pane.classList.toggle("active", pane.id === tabId);
  });
}

function switchSubtab(subtabId) {
  document.querySelectorAll(".subtab-btn").forEach(btn => {
    btn.classList.toggle("active", btn.getAttribute("onclick").includes(subtabId));
  });
  document.querySelectorAll(".subtab-pane").forEach(pane => {
    pane.classList.toggle("active", pane.id === subtabId);
  });
}

// ---------------------------------------------------------
// Modal Helpers
// ---------------------------------------------------------
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    populateDropdowns();
    modal.classList.add("open");
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("open");
}

window.onclick = function(event) {
  if (event.target.classList.contains("modal-backdrop")) {
    event.target.classList.remove("open");
  }
};

// ---------------------------------------------------------
// 1. Dashboard & KPI Loading
// ---------------------------------------------------------
async function loadDashboard() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (res.ok) {
      const stats = await res.json();
      state.stats = stats;
      document.getElementById("stat-customers").textContent = stats.total_customers;
      document.getElementById("stat-appointments").textContent = stats.total_appointments;
      document.getElementById("stat-repairs").textContent = stats.active_repairs;
      document.getElementById("stat-revenue").textContent = `₹${stats.total_revenue.toLocaleString('en-IN')}`;
    }
  } catch (e) {
    console.error("Dashboard stats error:", e);
  }
}

// ---------------------------------------------------------
// 2. Appointments
// ---------------------------------------------------------
async function loadAppointments() {
  try {
    const res = await fetch(`${API_BASE}/appointments`);
    if (res.ok) {
      state.appointments = await res.json();
      renderAppointments();
      renderDashboardRecentAppointments();
    }
  } catch (e) {
    console.error("Failed to load appointments:", e);
  }
}

function renderAppointments() {
  const tbody = document.getElementById("appointments-tbody");
  if (!tbody) return;

  if (state.appointments.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center" style="padding: 24px;">No appointments found.</td></tr>`;
    return;
  }

  tbody.innerHTML = state.appointments.map(a => {
    const badgeClass = `badge-${(a.status || 'pending').toLowerCase().replace('-', '')}`;
    return `
      <tr>
        <td><strong>#APT-${a.appointment_id}</strong></td>
        <td>${escapeHtml(a.customer_name || 'Customer #' + a.customer_id)}</td>
        <td><code>${escapeHtml(a.vehicle_reg || 'N/A')}</code></td>
        <td>${a.appointment_date} <small style="color:#64748b;">${a.appointment_time || ''}</small></td>
        <td>${escapeHtml(a.service_type)}</td>
        <td>${escapeHtml(a.mechanic_name || 'Unassigned')}</td>
        <td><span class="badge ${badgeClass}">${escapeHtml(a.status)}</span></td>
        <td>
          <select class="select-filter" style="padding: 4px 8px; font-size: 0.75rem;" onchange="updateAppointmentStatus(${a.appointment_id}, this.value)">
            <option value="Pending" ${a.status === 'Pending' ? 'selected' : ''}>Pending</option>
            <option value="Confirmed" ${a.status === 'Confirmed' ? 'selected' : ''}>Confirmed</option>
            <option value="In-Progress" ${a.status === 'In-Progress' ? 'selected' : ''}>In-Progress</option>
            <option value="Completed" ${a.status === 'Completed' ? 'selected' : ''}>Completed</option>
          </select>
        </td>
      </tr>
    `;
  }).join("");
}

function renderDashboardRecentAppointments() {
  const tbody = document.getElementById("dash-appointments-body");
  if (!tbody) return;

  const recents = state.appointments.slice(0, 5);
  if (recents.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-center">No recent appointments.</td></tr>`;
    return;
  }

  tbody.innerHTML = recents.map(a => {
    const badgeClass = `badge-${(a.status || 'pending').toLowerCase().replace('-', '')}`;
    return `
      <tr>
        <td><strong>#APT-${a.appointment_id}</strong></td>
        <td>${escapeHtml(a.customer_name || 'Customer')}</td>
        <td><code>${escapeHtml(a.vehicle_reg || '')}</code></td>
        <td>${escapeHtml(a.service_type)}</td>
        <td><span class="badge ${badgeClass}">${escapeHtml(a.status)}</span></td>
      </tr>
    `;
  }).join("");
}

async function updateAppointmentStatus(apptId, newStatus) {
  try {
    const res = await fetch(`${API_BASE}/appointments/${apptId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      await loadAppointments();
      await loadDashboard();
      await loadServices();
    }
  } catch (e) {
    alert("Failed to update appointment status.");
  }
}

async function handleAppointmentSubmit(e) {
  e.preventDefault();
  const customer_id = parseInt(document.getElementById("appt-customer-select").value);
  const vehicle_id = parseInt(document.getElementById("appt-vehicle-select").value);
  const appointment_date = document.getElementById("appt-date").value;
  const appointment_time = document.getElementById("appt-time").value;
  const service_type = document.getElementById("appt-service-type").value;
  const mechanic_val = document.getElementById("appt-mechanic-select").value;
  const mechanic_id = mechanic_val ? parseInt(mechanic_val) : null;

  try {
    const res = await fetch(`${API_BASE}/appointments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customer_id,
        vehicle_id,
        mechanic_id,
        appointment_date,
        appointment_time,
        service_type,
        status: "Pending"
      })
    });
    if (res.ok) {
      closeModal("modal-appointment");
      document.getElementById("form-appointment").reset();
      await loadAppointments();
      await loadDashboard();
      await loadServices();
      alert("Service appointment booked successfully!");
    } else {
      const err = await res.json();
      alert("Error: " + (err.detail || "Booking failed"));
    }
  } catch (err) {
    alert("Connection error when booking appointment.");
  }
}

function filterAppointmentsTable() {
  const query = document.getElementById("filter-appt-search").value.toLowerCase();
  const statusFilter = document.getElementById("filter-appt-status").value;
  const rows = document.querySelectorAll("#appointments-tbody tr");

  rows.forEach(r => {
    const text = r.innerText.toLowerCase();
    const matchesSearch = !query || text.includes(query);
    const matchesStatus = !statusFilter || text.includes(statusFilter.toLowerCase());
    r.style.display = matchesSearch && matchesStatus ? "" : "none";
  });
}

// ---------------------------------------------------------
// 3. Service Tracking
// ---------------------------------------------------------
async function loadServices() {
  try {
    const res = await fetch(`${API_BASE}/service-records`);
    if (res.ok) {
      state.services = await res.json();
      renderServices();
    }
  } catch (e) {
    console.error("Failed to load service records:", e);
  }
}

function renderServices() {
  const tbody = document.getElementById("services-tbody");
  if (!tbody) return;

  if (state.services.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center" style="padding: 24px;">No active service records.</td></tr>`;
    return;
  }

  tbody.innerHTML = state.services.map(s => {
    const badgeClass = `badge-${(s.service_status || 'inspection').toLowerCase().replace('-', '')}`;
    return `
      <tr>
        <td><strong>#SRV-${s.service_id}</strong></td>
        <td>#APT-${s.appointment_id}</td>
        <td><span class="badge ${badgeClass}">${escapeHtml(s.service_status)}</span></td>
        <td>${escapeHtml(s.inspection_notes || 'Pending check')}</td>
        <td>${escapeHtml(s.repair_details || 'Pending actions')}</td>
        <td>
          <small>Start: ${s.start_date || 'N/A'}</small><br>
          <small>End: ${s.completion_date || 'In Progress'}</small>
        </td>
        <td>
          <select class="select-filter" style="padding: 4px 8px; font-size: 0.75rem;" onchange="updateServiceRecordStatus(${s.service_id}, this.value)">
            <option value="Inspection" ${s.service_status === 'Inspection' ? 'selected' : ''}>Inspection</option>
            <option value="In-Progress" ${s.service_status === 'In-Progress' ? 'selected' : ''}>In-Progress</option>
            <option value="Pending Parts" ${s.service_status === 'Pending Parts' ? 'selected' : ''}>Pending Parts</option>
            <option value="Completed" ${s.service_status === 'Completed' ? 'selected' : ''}>Completed</option>
          </select>
        </td>
      </tr>
    `;
  }).join("");
}

async function updateServiceRecordStatus(serviceId, newStatus) {
  try {
    const res = await fetch(`${API_BASE}/service-records/${serviceId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ service_status: newStatus })
    });
    if (res.ok) {
      await loadServices();
      await loadDashboard();
    }
  } catch (e) {
    alert("Failed to update service record.");
  }
}

// ---------------------------------------------------------
// 4. Customers & Vehicles
// ---------------------------------------------------------
async function loadCustomers() {
  try {
    const res = await fetch(`${API_BASE}/customers`);
    if (res.ok) {
      state.customers = await res.json();
      document.getElementById("count-customers").textContent = state.customers.length;
      renderCustomers();
    }
  } catch (e) {
    console.error("Failed to load customers:", e);
  }
}

function renderCustomers() {
  const tbody = document.getElementById("customers-tbody");
  if (!tbody) return;

  tbody.innerHTML = state.customers.map(c => `
    <tr>
      <td>#CUST-${c.customer_id}</td>
      <td><strong>${escapeHtml(c.name)}</strong></td>
      <td>${escapeHtml(c.email)}</td>
      <td>${escapeHtml(c.phone || '-')}</td>
      <td>${escapeHtml(c.address || '-')}</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="promptAddVehicleForCustomer(${c.customer_id})">+ Add Car</button>
      </td>
    </tr>
  `).join("");
}

async function handleCustomerSubmit(e) {
  e.preventDefault();
  const name = document.getElementById("cust-name").value;
  const email = document.getElementById("cust-email").value;
  const phone = document.getElementById("cust-phone").value;
  const address = document.getElementById("cust-address").value;

  try {
    const res = await fetch(`${API_BASE}/customers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, phone, address })
    });
    if (res.ok) {
      closeModal("modal-customer");
      document.getElementById("form-customer").reset();
      await loadCustomers();
      await loadDashboard();
      populateDropdowns();
      alert("Customer registered successfully!");
    } else {
      const err = await res.json();
      alert("Error: " + (err.detail || "Registration failed"));
    }
  } catch (e) {
    alert("Network error.");
  }
}

async function loadVehicles() {
  try {
    const res = await fetch(`${API_BASE}/vehicles`);
    if (res.ok) {
      state.vehicles = await res.json();
      document.getElementById("count-vehicles").textContent = state.vehicles.length;
      renderVehicles();
    }
  } catch (e) {
    console.error("Failed to load vehicles:", e);
  }
}

function renderVehicles() {
  const tbody = document.getElementById("vehicles-tbody");
  if (!tbody) return;

  tbody.innerHTML = state.vehicles.map(v => `
    <tr>
      <td>#VEH-${v.vehicle_id}</td>
      <td><code><strong>${escapeHtml(v.registration_no)}</strong></code></td>
      <td>${escapeHtml(v.make)} ${escapeHtml(v.model)}</td>
      <td>${v.year || '-'}</td>
      <td><span class="badge badge-confirmed">${escapeHtml(v.vehicle_type || 'Car')}</span></td>
      <td>Customer #${v.customer_id}</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="bookForVehicle(${v.customer_id}, ${v.vehicle_id})">Book Service</button>
      </td>
    </tr>
  `).join("");
}

function promptAddVehicleForCustomer(customerId) {
  openModal('modal-vehicle');
  const sel = document.getElementById("veh-customer-select");
  if (sel) sel.value = customerId;
}

function bookForVehicle(customerId, vehicleId) {
  openModal('modal-appointment');
  const custSel = document.getElementById("appt-customer-select");
  const vehSel = document.getElementById("appt-vehicle-select");
  if (custSel) custSel.value = customerId;
  if (vehSel) vehSel.value = vehicleId;
}

async function handleVehicleSubmit(e) {
  e.preventDefault();
  const customer_id = parseInt(document.getElementById("veh-customer-select").value);
  const registration_no = document.getElementById("veh-reg").value;
  const make = document.getElementById("veh-make").value;
  const model = document.getElementById("veh-model").value;
  const year = parseInt(document.getElementById("veh-year").value) || null;
  const vehicle_type = document.getElementById("veh-type").value;

  try {
    const res = await fetch(`${API_BASE}/vehicles`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id, registration_no, make, model, year, vehicle_type })
    });
    if (res.ok) {
      closeModal("modal-vehicle");
      document.getElementById("form-vehicle").reset();
      await loadVehicles();
      await loadDashboard();
      populateDropdowns();
      alert("Vehicle registered successfully!");
    } else {
      const err = await res.json();
      alert("Error: " + (err.detail || "Vehicle registration failed"));
    }
  } catch (e) {
    alert("Network error.");
  }
}

// ---------------------------------------------------------
// 5. Spare Parts & Inventory
// ---------------------------------------------------------
async function loadInventory() {
  try {
    const res = await fetch(`${API_BASE}/spare-parts`);
    if (res.ok) {
      state.spareParts = await res.json();
      renderInventory();
      renderDashboardInventoryAlerts();
    }
  } catch (e) {
    console.error("Failed to load inventory:", e);
  }
}

function renderInventory() {
  const tbody = document.getElementById("inventory-tbody");
  if (!tbody) return;

  tbody.innerHTML = state.spareParts.map(p => {
    const isLow = p.quantity <= p.reorder_level;
    const statusBadge = isLow
      ? `<span class="badge badge-danger">Low Stock (≤ ${p.reorder_level})</span>`
      : `<span class="badge badge-available">In Stock</span>`;

    return `
      <tr>
        <td>#PART-${p.part_id}</td>
        <td><strong>${escapeHtml(p.part_name)}</strong></td>
        <td>${escapeHtml(p.category || 'General')}</td>
        <td><strong>${p.quantity} units</strong></td>
        <td>₹${parseFloat(p.unit_price).toFixed(2)}</td>
        <td>${statusBadge}</td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="quickRestockPart(${p.part_id}, ${p.quantity})">+ Restock</button>
        </td>
      </tr>
    `;
  }).join("");
}

function renderDashboardInventoryAlerts() {
  const container = document.getElementById("dash-inventory-list");
  if (!container) return;

  const lowParts = state.spareParts.filter(p => p.quantity <= p.reorder_level);
  if (lowParts.length === 0) {
    container.innerHTML = `
      <div class="alert-item">
        <span>All parts are adequately stocked above reorder thresholds.</span>
        <span class="badge badge-available">Healthy</span>
      </div>
    `;
    return;
  }

  container.innerHTML = lowParts.map(p => `
    <div class="alert-item critical">
      <div>
        <strong>${escapeHtml(p.part_name)}</strong>
        <p style="font-size: 0.8rem; color: #991b1b; margin-top: 2px;">
          Current Stock: ${p.quantity} (Reorder threshold: ${p.reorder_level})
        </p>
      </div>
      <button class="btn btn-secondary btn-sm" onclick="quickRestockPart(${p.part_id}, ${p.quantity})">Reorder</button>
    </div>
  `).join("");
}

async function quickRestockPart(partId, currentQty) {
  const add = prompt("Enter quantity to add to stock:", "10");
  if (!add || isNaN(add)) return;
  const newQty = currentQty + parseInt(add);

  try {
    const res = await fetch(`${API_BASE}/spare-parts/${partId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quantity: newQty })
    });
    if (res.ok) {
      await loadInventory();
      await loadDashboard();
    }
  } catch (e) {
    alert("Failed to restock item.");
  }
}

async function handleSparePartSubmit(e) {
  e.preventDefault();
  const part_name = document.getElementById("part-name").value;
  const category = document.getElementById("part-category").value;
  const quantity = parseInt(document.getElementById("part-qty").value);
  const unit_price = parseFloat(document.getElementById("part-price").value);
  const reorder_level = parseInt(document.getElementById("part-reorder").value);

  try {
    const res = await fetch(`${API_BASE}/spare-parts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ part_name, category, quantity, unit_price, reorder_level })
    });
    if (res.ok) {
      closeModal("modal-spare-part");
      document.getElementById("form-spare-part").reset();
      await loadInventory();
      await loadDashboard();
      alert("Spare part added to inventory!");
    } else {
      alert("Failed to add spare part.");
    }
  } catch (e) {
    alert("Network error.");
  }
}

// ---------------------------------------------------------
// 6. Mechanics
// ---------------------------------------------------------
async function loadMechanics() {
  try {
    const res = await fetch(`${API_BASE}/mechanics`);
    if (res.ok) {
      state.mechanics = await res.json();
      renderMechanics();
    }
  } catch (e) {
    console.error("Failed to load mechanics:", e);
  }
}

function renderMechanics() {
  const container = document.getElementById("mechanics-grid");
  if (!container) return;

  container.innerHTML = state.mechanics.map(m => {
    const badgeClass = m.status === 'Available' ? 'badge-available' : 'badge-busy';
    return `
      <div class="mechanic-card">
        <div class="mech-header">
          <div class="mech-avatar">${m.name.charAt(0)}</div>
          <span class="badge ${badgeClass}">${m.status}</span>
        </div>
        <div>
          <h4>${escapeHtml(m.name)}</h4>
          <p style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">${escapeHtml(m.specialization || 'General Technician')}</p>
        </div>
        <div style="font-size: 0.82rem; color: #475569; border-top: 1px solid #f1f5f9; padding-top: 8px;">
          📞 ${escapeHtml(m.phone || 'No phone recorded')}
        </div>
        <button class="btn btn-secondary btn-sm" onclick="toggleMechanicStatus(${m.mechanic_id}, '${m.status}')">
          Toggle Status
        </button>
      </div>
    `;
  }).join("");
}

async function toggleMechanicStatus(mechId, currentStatus) {
  const newStatus = currentStatus === 'Available' ? 'Busy' : 'Available';
  try {
    const res = await fetch(`${API_BASE}/mechanics/${mechId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      await loadMechanics();
      await loadDashboard();
    }
  } catch (e) {
    alert("Error updating mechanic status.");
  }
}

async function handleMechanicSubmit(e) {
  e.preventDefault();
  const name = document.getElementById("mech-name").value;
  const phone = document.getElementById("mech-phone").value;
  const specialization = document.getElementById("mech-spec").value;

  try {
    const res = await fetch(`${API_BASE}/mechanics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, phone, specialization, status: "Available" })
    });
    if (res.ok) {
      closeModal("modal-mechanic");
      document.getElementById("form-mechanic").reset();
      await loadMechanics();
      populateDropdowns();
      alert("Mechanic registered successfully!");
    }
  } catch (e) {
    alert("Failed to save mechanic.");
  }
}

// ---------------------------------------------------------
// 7. Billing, Invoices & Payments
// ---------------------------------------------------------
async function loadBills() {
  try {
    const res = await fetch(`${API_BASE}/bills`);
    if (res.ok) {
      state.bills = await res.json();
      renderBills();
    }
  } catch (e) {
    console.error("Failed to load bills:", e);
  }
}

function renderBills() {
  const tbody = document.getElementById("bills-tbody");
  if (!tbody) return;

  tbody.innerHTML = state.bills.map(b => `
    <tr>
      <td><strong>#INV-${String(b.bill_id).padStart(5, '0')}</strong></td>
      <td>Job #SRV-${b.service_id}</td>
      <td>Customer #${b.customer_id}</td>
      <td>${b.bill_date || '-'}</td>
      <td>₹${b.parts_charge.toFixed(2)}</td>
      <td>₹${b.labour_charge.toFixed(2)}</td>
      <td>₹${b.tax.toFixed(2)}</td>
      <td><strong>₹${b.total_amount.toFixed(2)}</strong></td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="viewDetailedInvoice(${b.bill_id})">View Invoice</button>
      </td>
    </tr>
  `).join("");
}

function calculateBillTotal() {
  const parts = parseFloat(document.getElementById("bill-parts").value) || 0;
  const labour = parseFloat(document.getElementById("bill-labour").value) || 0;
  const tax = Math.round((parts + labour) * 0.12 * 100) / 100;
  const total = Math.round((parts + labour + tax) * 100) / 100;

  document.getElementById("bill-tax").value = tax.toFixed(2);
  document.getElementById("bill-total").value = total.toFixed(2);
}

function onServiceJobSelectedForBill() {
  calculateBillTotal();
}

async function handleBillSubmit(e) {
  e.preventDefault();
  const service_id = parseInt(document.getElementById("bill-service-select").value);
  const labour_charge = parseFloat(document.getElementById("bill-labour").value) || 0;
  const parts_charge = parseFloat(document.getElementById("bill-parts").value) || 0;
  const tax = parseFloat(document.getElementById("bill-tax").value) || 0;
  const total_amount = parseFloat(document.getElementById("bill-total").value) || 0;

  // Retrieve customer_id from service -> appointment
  const svc = state.services.find(s => s.service_id === service_id);
  let customer_id = 1;
  if (svc) {
    const appt = state.appointments.find(a => a.appointment_id === svc.appointment_id);
    if (appt) customer_id = appt.customer_id;
  }

  try {
    const res = await fetch(`${API_BASE}/bills`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service_id,
        customer_id,
        labour_charge,
        parts_charge,
        tax,
        total_amount,
        bill_date: new Date().toISOString().split("T")[0]
      })
    });
    if (res.ok) {
      closeModal("modal-bill");
      await loadBills();
      await loadDashboard();
      alert("Invoice generated successfully!");
    }
  } catch (err) {
    alert("Failed to create bill.");
  }
}

async function viewDetailedInvoice(billId) {
  try {
    const res = await fetch(`${API_BASE}/bills/${billId}/invoice`);
    if (!res.ok) throw new Error("Invoice fetch failed");
    const inv = await res.json();
    renderPrintableInvoice(inv);
    openModal("modal-invoice-viewer");
  } catch (e) {
    alert("Could not load invoice details.");
  }
}

function renderPrintableInvoice(inv) {
  const container = document.getElementById("invoice-render-content");
  if (!container) return;

  const partsRows = inv.parts_used.length > 0
    ? inv.parts_used.map(p => `
        <tr>
          <td>${escapeHtml(p.part_name)}</td>
          <td>${p.quantity}</td>
          <td>₹${p.unit_price.toFixed(2)}</td>
          <td style="text-align: right;">₹${p.subtotal.toFixed(2)}</td>
        </tr>
      `).join("")
    : `<tr><td colspan="4" style="color: #64748b;">Standard servicing lubricants & shop supplies included in package.</td></tr>`;

  const isPaid = inv.payment_status === "Paid";
  const payBadge = isPaid
    ? `<span class="badge badge-success" style="font-size: 0.9rem; padding: 6px 14px;">PAID IN FULL</span>`
    : `<button class="btn btn-primary btn-sm" onclick="processQuickPayment(${inv.bill_id}, ${inv.charges.total_amount})">Mark as Paid (UPI / Card)</button>`;

  container.innerHTML = `
    <div class="inv-header">
      <div>
        <h2 class="inv-title">Autocare Pro Service Centre</h2>
        <p style="font-size: 0.85rem; color: #475569;">104 Tech Valley, Jubilee Hills, Hyderabad - 500033</p>
        <p style="font-size: 0.85rem; color: #475569;">GSTIN: 36ABCDE1234F1Z5 | Phone: +91 98765 00000</p>
      </div>
      <div style="text-align: right;">
        <h3 style="color: #0d3830; font-size: 1.3rem;">${inv.invoice_number}</h3>
        <p style="font-size: 0.85rem; color: #64748b;">Date: ${inv.date}</p>
        <div style="margin-top: 10px;">${payBadge}</div>
      </div>
    </div>

    <div class="inv-meta-grid">
      <div class="inv-block">
        <h4>Billed To (Customer):</h4>
        <p><strong>${escapeHtml(inv.customer.name)}</strong></p>
        <p style="font-size: 0.85rem; color: #475569;">${escapeHtml(inv.customer.phone || '')}</p>
        <p style="font-size: 0.85rem; color: #475569;">${escapeHtml(inv.customer.email || '')}</p>
        <p style="font-size: 0.85rem; color: #475569;">${escapeHtml(inv.customer.address || '')}</p>
      </div>
      <div class="inv-block">
        <h4>Vehicle & Job Details:</h4>
        <p><strong>Reg No:</strong> <code>${escapeHtml(inv.vehicle.registration_no)}</code></p>
        <p style="font-size: 0.85rem; color: #475569;"><strong>Model:</strong> ${escapeHtml(inv.vehicle.make)} ${escapeHtml(inv.vehicle.model)} (${inv.vehicle.year})</p>
        <p style="font-size: 0.85rem; color: #475569;"><strong>Package:</strong> ${escapeHtml(inv.service.service_type)}</p>
        <p style="font-size: 0.85rem; color: #475569;"><strong>Mechanic:</strong> ${escapeHtml(inv.service.mechanic_name)}</p>
      </div>
    </div>

    <table class="data-table" style="margin-bottom: 20px;">
      <thead>
        <tr>
          <th>Spare Part / Material Description</th>
          <th>Qty</th>
          <th>Unit Price</th>
          <th style="text-align: right;">Subtotal</th>
        </tr>
      </thead>
      <tbody>
        ${partsRows}
      </tbody>
    </table>

    <div class="inv-totals">
      <div>Parts Total: <strong>₹${inv.charges.parts_charge.toFixed(2)}</strong></div>
      <div>Labour Charges: <strong>₹${inv.charges.labour_charge.toFixed(2)}</strong></div>
      <div>CGST + SGST (12%): <strong>₹${inv.charges.tax.toFixed(2)}</strong></div>
      <div class="grand-total">Total Billed: ₹${inv.charges.total_amount.toFixed(2)}</div>
    </div>
  `;
}

async function processQuickPayment(billId, amount) {
  const method = prompt("Select Payment Method (UPI, Cash, Credit Card):", "UPI");
  if (!method) return;

  try {
    const res = await fetch(`${API_BASE}/payments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        bill_id: billId,
        amount: amount,
        payment_method: method,
        payment_status: "Completed",
        payment_date: new Date().toISOString().split("T")[0]
      })
    });
    if (res.ok) {
      alert("Payment recorded successfully!");
      await loadDashboard();
      await loadBills();
      viewDetailedInvoice(billId);
    }
  } catch (e) {
    alert("Payment recording failed.");
  }
}

// ---------------------------------------------------------
// Dropdown Population
// ---------------------------------------------------------
function populateDropdowns() {
  // 1. Appointment Customer Select
  const apptCustSel = document.getElementById("appt-customer-select");
  if (apptCustSel && state.customers.length > 0) {
    apptCustSel.innerHTML = state.customers.map(c => `
      <option value="${c.customer_id}">${escapeHtml(c.name)} (${c.email})</option>
    `).join("");
  }

  // 2. Appointment Vehicle Select
  const apptVehSel = document.getElementById("appt-vehicle-select");
  if (apptVehSel && state.vehicles.length > 0) {
    apptVehSel.innerHTML = state.vehicles.map(v => `
      <option value="${v.vehicle_id}">${escapeHtml(v.registration_no)} - ${escapeHtml(v.make)} ${escapeHtml(v.model)}</option>
    `).join("");
  }

  // 3. Appointment Mechanic Select
  const apptMechSel = document.getElementById("appt-mechanic-select");
  if (apptMechSel) {
    apptMechSel.innerHTML = `<option value="">-- Auto-Assign Available Mechanic --</option>` +
      state.mechanics.map(m => `
        <option value="${m.mechanic_id}">${escapeHtml(m.name)} (${m.specialization || 'Tech'} - ${m.status})</option>
      `).join("");
  }

  // 4. Vehicle Customer Select
  const vehCustSel = document.getElementById("veh-customer-select");
  if (vehCustSel && state.customers.length > 0) {
    vehCustSel.innerHTML = state.customers.map(c => `
      <option value="${c.customer_id}">${escapeHtml(c.name)}</option>
    `).join("");
  }

  // 5. Bill Service Select
  const billSvcSel = document.getElementById("bill-service-select");
  if (billSvcSel && state.services.length > 0) {
    billSvcSel.innerHTML = state.services.map(s => `
      <option value="${s.service_id}">Job #SRV-${s.service_id} (Appt #${s.appointment_id} - ${s.service_status})</option>
    `).join("");
  }
}

function handleLogout() {
  if (confirm("Sign out of current session?")) {
    window.location.reload();
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
