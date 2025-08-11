# DocType API Reference

This comprehensive reference documents all major doctypes in the VSD Fleet Management System, including their fields, relationships, and key methods.

---

## Core Transaction Doctypes

### Cargo Registration

**Purpose**: Customer cargo registration and service request management

#### Key Fields
```json
{
  "customer": "Link to Customer",
  "transport_type": "Select: Cross Border/Internal", 
  "posting_date": "Date",
  "cargo_details": "Table: Cargo Detail child table",
  "requested_fund": "Table: Requested Fund Details"
}
```

#### Child Table: Cargo Detail
```json
{
  "container_size": "Select: Loose/20 FT/40 FT",
  "net_weight": "Float: Weight in kg",
  "cargo_route": "Link: Trip Routes",
  "service_item": "Link: Item for billing",
  "rate": "Float: Service rate",
  "manifest_number": "Link: Assigned manifest",
  "created_trip": "Data: Generated trip reference"
}
```

#### Key Methods
- `create_sales_invoice()`: Generate customer invoice from selected cargo
- JavaScript: `assign_manifest()`: Assign cargo to vehicle manifest

#### Business Rules
- Each cargo row represents one vehicle's capacity
- Invoice creation required before manifest assignment
- Location validation (city must match country)

---

### Manifest

**Purpose**: Vehicle assignment and cargo organization for trips

#### Key Fields
```json
{
  "route": "Link: Trip Routes",
  "transporter_type": "Select: In House/Sub-Contractor",
  "truck": "Link: Truck (for In House)",
  "assigned_driver": "Link: Truck Driver",
  "has_trailers": "Check: Enable trailer selection",
  "trailer_1/2/3": "Link: Up to 3 trailers",
  "manifest_cargo_details": "Table: Cargo assignments",
  "vehicle_trip": "Link: Generated trip"
}
```

#### Child Table: Manifest Cargo Details
```json
{
  "cargo_id": "Data: Reference to cargo detail",
  "cargo_allocation": "Select: Truck/Trailers", 
  "specific_cargo_allocated": "Data: Specific vehicle/trailer",
  "weight": "Float: Cargo weight"
}
```

#### Key Methods
- `get_manifests()`: Fetch available manifests by route
- `add_to_existing_manifest()`: Add cargo to existing manifest
- `create_new_manifest()`: Create manifest with cargo
- `validate()`: Update truck status on submission

#### Business Rules
- Only idle trucks can be assigned
- Trailer selection must be sequential (1, 2, 3)
- Cargo allocation must match available vehicles

---

### Trips

**Purpose**: Complete trip execution and management

#### Key Fields
```json
{
  "manifest": "Link: Source manifest",
  "route": "Link: Trip route",
  "transporter_type": "Data: In House/Sub-Contractor",
  "main_route_steps": "Table: Route execution steps",
  "side_trips": "Table: Additional route deviations",
  "location_update": "Table: GPS/manual tracking",
  "requested_fund_accounts_table": "Table: Trip expenses",
  "fuel_request_history": "Table: Fuel requirements",
  "trip_status": "Select: Pending/Completed/Breakdown",
  "trip_completed": "Check: Completion flag"
}
```

#### Child Tables

##### Route Steps
```json
{
  "location": "Data: Stop name",
  "distance": "Int: Kilometers",
  "fuel_consumption_qty": "Float: Liters",
  "location_type": "Select: Loading/Offloading/Border/Town",
  "loading_date": "Date: Actual pickup",
  "offloading_date": "Date: Actual delivery"
}
```

##### Requested Fund Details
```json
{
  "expense_type": "Link: Fixed Expenses",
  "request_amount": "Currency: Amount requested",
  "request_currency": "Link: USD/TZS",
  "request_status": "Select: Requested/Approved/Rejected",
  "expense_account": "Link: GL expense account",
  "payable_account": "Link: Cash/bank account",
  "journal_entry": "Link: Payment voucher"
}
```

##### Fuel Requests Table
```json
{
  "item_code": "Link: Fuel item",
  "quantity": "Float: Liters required",
  "cost_per_litre": "Currency: Fuel price",
  "total_cost": "Currency: Calculated total",
  "supplier": "Link: Fuel supplier",
  "status": "Select: Requested/Approved/Rejected",
  "purchase_order": "Link: Generated PO"
}
```

#### Key Methods
- `create_vehicle_trip_from_manifest()`: Generate trip from manifest
- `create_fund_jl()`: Create Journal Entry for approved funds
- `create_purchase_order()`: Generate PO for fuel
- `create_stock_out_entry()`: Process fuel stock consumption
- `create_breakdown()`: Handle vehicle breakdown
- `create_resumption_trip()`: Generate replacement trip

#### Business Rules
- All fund/fuel requests must be approved before submission
- Approved requests must have corresponding PO/Journal Entry
- Stock out entry required for In House trips

---

## Support Doctypes

### Fuel Requests

**Purpose**: Centralized fuel approval management

#### Key Fields
```json
{
  "reference_doctype": "Link: Source document type",
  "reference_docname": "Dynamic: Source document",
  "truck": "Link: Vehicle",
  "truck_driver": "Link: Driver",
  "main_route": "Link: Trip route",
  "requested_fuel": "Table: Pending requests",
  "approved_requests": "Table: Processed requests",
  "status": "Select: Waiting/Partially/Fully Processed"
}
```

#### Custom Methods
- Custom `load_from_db()`: Loads approved/rejected requests
- `update_children()`: Prevents standard child table updates

---

### Requested Payment

**Purpose**: Trip fund approval management

#### Key Fields
```json
{
  "company": "Link: Operating company",
  "truck_driver": "Link: Driver",
  "manifest": "Link: Source manifest",
  "requested_funds": "Table: Pending fund requests",
  "accounts_approval": "Table: Processed requests",
  "approval_status": "Select: Waiting/Processed",
  "payment_status": "Select: Waiting/Paid"
}
```

#### JavaScript Features
- Real-time total calculations
- Approve/reject button handling
- Payment status tracking
- Journal Entry integration

---

## Master Data Doctypes

### Truck

**Purpose**: Vehicle master data and status tracking

#### Key Fields
```json
{
  "truck_number": "Data: Unique identifier",
  "license_plate": "Data: Registration number",
  "make": "Data: Manufacturer",
  "model": "Data: Vehicle model",
  "fuel_type": "Select: Petrol/Diesel",
  "status": "Select: Idle/On Trip/Under Maintenance/Disabled",
  "trans_ms_current_trip": "Link: Active trip",
  "trans_ms_fuel_warehouse": "Link: Fuel storage location"
}
```

#### Status Management
- **Idle**: Available for assignment
- **On Trip**: Currently assigned to active trip
- **Under Maintenance**: Temporarily unavailable
- **Disabled**: Permanently unavailable

---

### Truck Driver

**Purpose**: Driver master data and availability tracking

#### Key Fields
```json
{
  "full_name": "Data: Driver name",
  "status": "Select: Active/Suspended/Left",
  "cell_number": "Data: Contact number",
  "employee": "Link: HR Employee record",
  "in_trip": "Check: Current trip status",
  "drivers_document": "Table: License and certifications"
}
```

---

### Trip Routes

**Purpose**: Route definition with steps and expenses

#### Key Fields
```json
{
  "route_name": "Data: Unique route identifier",
  "starting_point": "Data: Origin location",
  "ending_point": "Data: Destination location", 
  "trip_steps": "Table: Route waypoints",
  "fixed_expenses": "Table: Standard route costs",
  "total_distance": "Int: Calculated distance",
  "total_fuel_consumption_qty": "Float: Calculated fuel"
}
```

#### Child Tables

##### Trip Steps
```json
{
  "location": "Data: Waypoint name",
  "distance": "Int: Kilometers from previous",
  "fuel_consumption_qty": "Float: Liters for segment",
  "location_type": "Select: Loading/Offloading/Border/Town"
}
```

##### Fixed Expenses Table
```json
{
  "expense": "Link: Fixed Expenses master",
  "amount": "Currency: Standard amount",
  "currency": "Link: USD/TZS",
  "party_type": "Select: Employee/Supplier"
}
```

---

### Transport Settings

**Purpose**: System-wide configuration (SingleDocType)

#### Key Fields
```json
{
  "fuel_item": "Link: Default fuel item",
  "vehicle_fuel_parent_warehouse": "Link: Main fuel warehouse",
  "sales_item_group": "Link: Service item group",
  "expense_account_group": "Table: Expense account categories",
  "cash_or_bank_account_group": "Table: Payment account categories",
  "accounting_dimension": "Table: Dimension mapping rules"
}
```

#### Accounting Dimension Table
```json
{
  "dimension_name": "Data: Dimension identifier",
  "source_doctype": "Link: Source document",
  "source_field_name": "Data: Source field",
  "target_doctype": "Link: Target document", 
  "target_field_name": "Data: Target field",
  "source_type": "Select: Field/Value/Child",
  "target_type": "Select: Main/Child"
}
```

---

## Utility Functions

### Dimension Setting
```python
def set_dimension(src_doc, tr_doc, src_child=None, tr_child=None):
    """Apply accounting dimensions from source to target document"""
    # Fetch Transport Settings dimension configuration
    # Apply field mappings based on doctype combinations
    # Handle main document and child table dimensions
```

### Custom Functions
```python
def update_child_table(self, fieldname, df=None):
    """Prevent modification of approved/rejected fund requests"""
    # Custom child table update logic
    # Protect approved/rejected financial records
```

```python
def add_to_manifest(route_starting_point):
    """Fetch available cargo for manifest assignment"""
    # Query cargo details by route
    # Filter unassigned, submitted cargo
    # Return data for manifest dialog
```

---

## API Integration Points

### ERPNext Integration
- **Stock Entry**: Fuel consumption tracking
- **Purchase Order**: Fuel procurement
- **Journal Entry**: Financial transactions
- **Sales Invoice**: Customer billing

### Custom Workflows
- **Manifest Assignment**: Cargo to vehicle assignment
- **Trip Creation**: Automated trip generation
- **Approval Workflows**: Fund and fuel approval
- **Status Updates**: Vehicle and driver availability

---

## JavaScript Event Handlers

### Form Events
```javascript
// Cargo Registration
frappe.ui.form.on('Cargo Registration', {
    create_invoice: function(frm) {
        // Generate customer invoice from selected cargo
    }
});

// Manifest  
frappe.ui.form.on('Manifest', {
    refresh: function(frm) {
        // Add custom buttons for cargo management
        // Filter vehicle/driver selection
    }
});

// Trips
frappe.ui.form.on('Trips', {
    refresh: function(frm) {
        // Add action buttons (complete, breakdown)
        // Calculate financial summaries
    }
});
```

### Child Table Events
```javascript
frappe.ui.form.on('Cargo Detail', {
    assign_manifest: function(frm, cdt, cdn) {
        // Open manifest assignment dialog
    }
});

frappe.ui.form.on('Fuel Requests Table', {
    create_purchase_order: function(frm, cdt, cdn) {
        // Generate PO for approved fuel
    }
});
```

---

This reference provides the technical foundation for understanding the VSD Fleet Management System's data structure and API capabilities for customization and integration purposes.