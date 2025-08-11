# Trip Management: Complete Transportation Execution

The **Trips** doctype is the operational heart of the fleet management system, managing the complete lifecycle of transportation operations from trip creation through completion, including route execution, fund management, fuel administration, and status tracking.

---

## Purpose and Scope

Trip Management encompasses:
- **Route Execution**: Managing predefined route steps and progress tracking
- **Financial Management**: Handling trip funds, expenses, and approvals
- **Fuel Administration**: Managing fuel requests, approvals, and stock
- **Real-time Tracking**: Location updates and progress monitoring
- **Status Management**: Trip progression from start to completion
- **Exception Handling**: Breakdown management and trip reassignment

---

## Document Structure and Tabs

### Tab 1: Trip Details

#### Basic Information
| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Manifest** | Link | Source manifest | Yes |
| **Transporter Type** | Data | In House/Sub-Contractor | Auto |
| **Route** | Link | Trip route | Auto |
| **Date** | Date | Trip start date | Yes |
| **Company** | Link | Operating company | Yes |

#### Vehicle Information (In House)
- **Truck Number**: Assigned vehicle
- **Truck License Plate**: Vehicle registration
- **Assigned Driver**: Selected driver
- **Driver Name**: Driver details
- **Trailers**: Up to 3 trailers if configured

#### Sub-Contractor Information
- **Sub-Contractor Name**: Contractor company
- **Truck License Plate**: External vehicle
- **Driver Name**: External driver
- **License Number**: External license

### Tab 2: Route Steps

Route steps are automatically populated from the Trip Routes master:

| Field | Type | Purpose | Editable |
|-------|------|---------|----------|
| **Location** | Data | Stop/checkpoint name | No |
| **Distance** | Int | Kilometers to this point | No |
| **Fuel Consumption** | Float | Liters for this segment | No |
| **Location Type** | Select | Loading/Offloading/Border/Town | No |
| **Loading Date** | Date | Actual pickup date | Yes |
| **Offloading Date** | Date | Actual delivery date | Yes |

**Validation Rules**:
- Loading date must be before offloading date
- Dates must be filled for Loading and Offloading points

### Tab 3: Side Trips

For deviations from the main route:

| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Location** | Data | Additional stop | Yes |
| **Distance** | Int | Extra kilometers | Yes |
| **Fuel Consumption** | Float | Additional fuel | Yes |
| **Purpose** | Text | Reason for deviation | Optional |

**Impact**: Side trips automatically update total distance and fuel consumption.

### Tab 4: Location Updates

Real-time tracking capability:

| Field | Type | Purpose | Source |
|-------|------|---------|--------|
| **Update Time** | Datetime | Timestamp | Manual/GPS |
| **Location** | Data | Current position | Manual |
| **Latitude/Longitude** | Float | GPS coordinates | GPS |
| **Status** | Select | Current activity | Manual |
| **View on Map** | Button | Google Maps integration | System |

### Tab 5: Trip Funds

Automatically generated from Trip Routes fixed expenses:

| Field | Type | Purpose | Status |
|-------|------|---------|--------|
| **Expense Type** | Link | Fixed expense category | Auto |
| **Request Amount** | Currency | Expense amount | Auto |
| **Request Currency** | Link | USD/TZS | Auto |
| **Request Status** | Select | Requested/Approved/Rejected | Manual |
| **Expense Account** | Link | GL account | Auto |
| **Payable Account** | Link | Cash/Bank account | Auto |
| **Party Type** | Select | Employee/Supplier | Auto |
| **Party** | Dynamic | Payment recipient | Auto |
| **Journal Entry** | Link | Payment voucher | System |

**Fund Management Features**:
- **Approve/Reject**: Status management
- **Disburse Funds**: Create Journal Entry
- **Real-time Totals**: USD/TZS summary displays

### Tab 6: Fuel Management

Comprehensive fuel administration:

| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Item Code** | Link | Fuel item | Yes |
| **Item Name** | Data | Fuel description | Auto |
| **UOM** | Link | Unit of measure | Yes |
| **Quantity** | Float | Liters required | Yes |
| **Cost per Liter** | Currency | Current fuel price | Yes |
| **Total Cost** | Currency | Calculated amount | Auto |
| **Currency** | Link | Pricing currency | Yes |
| **Disbursement Type** | Select | Cash/Credit | Yes |
| **Supplier** | Link | Fuel supplier | Yes |
| **Status** | Select | Requested/Approved/Rejected | System |
| **Purchase Order** | Link | Generated PO | System |

**Fuel Workflow**:
1. **Request**: Fill fuel requirements
2. **Approval**: Supervisor approves/rejects via Fuel Requests
3. **Purchase**: Create Purchase Order for approved fuel
4. **Stock**: Reduce stock via Stock Entry

### Tab 7: Trip Status

Status tracking and completion:

| Field | Type | Purpose | Control |
|-------|------|---------|---------|
| **Trip Status** | Select | Pending/Completed/Breakdown | System |
| **Approve Status** | Data | Fund/fuel approval summary | Auto |
| **Trip Completed** | Check | Completion flag | Manual |
| **Trip Completed Date** | Date | Completion timestamp | Auto |

---

## Key JavaScript Functionality

### 1. Real-time Financial Summaries

```javascript
// Dynamic fund totals calculation
function approved_total() {
    var total_request_tsh = 0;
    var total_request_usd = 0;
    cur_frm.doc.requested_fund_accounts_table.forEach(function (row) {
        if (row.request_currency == 'TZS' && row.request_status == "Approved") {
            total_request_tsh += row.request_amount;
        }
        else if (row.request_currency == 'USD' && row.request_status == "Approved") {
            total_request_usd += row.request_amount;
        }
    });
    // Update HTML display
}
```

### 2. Border Charges Calculation

```javascript
// Automatic border duration calculation
date_of_departure_from_border: (frm) => {
    if (frm.doc.date_of_departure_from_border && frm.doc.arrival_date_at_border) {
        var date1 = frappe.datetime.str_to_obj(cur_frm.doc.date_of_departure_from_border);
        var date2 = frappe.datetime.str_to_obj(cur_frm.doc.arrival_date_at_border);
        var difference_days = Math.floor((date1 - date2) / (1000 * 60 * 60 * 24));
        frm.doc.total_days_at_the_border = difference_days;
    }
}
```

### 3. Action Buttons

```javascript
// Trip completion
frm.add_custom_button(__("Complete Trip"), function () {
    frm.set_value("trip_completed", 1);
    frm.set_value("trip_completed_date", frappe.datetime.nowdate());
    // Update truck status to Idle
}, __('Actions'));

// Breakdown management
frm.add_custom_button(__('Create Breakdown Entry'), function() {
    // Handle vehicle breakdown
}, __('Actions'));
```

---

## Business Process Flow

### Phase 1: Trip Creation
1. **From Manifest**: Click "Create Vehicle Trip"
2. **Auto-Population**: System fills trip details from manifest
3. **Route Steps**: Copied from Trip Routes master
4. **Fixed Expenses**: Auto-generated as fund requests
5. **Fuel Allocation**: Initial fuel requirements set

### Phase 2: Pre-Trip Approval
1. **Fund Approval**: Accountant reviews requested funds
2. **Fuel Approval**: Supervisor approves fuel requests
3. **Purchase Orders**: Generate POs for approved fuel
4. **Stock Preparation**: Create stock entries for fuel

### Phase 3: Trip Execution
1. **Submit Trip**: Lock configuration and start journey
2. **Status Tracking**: Vehicle marked "On Trip"
3. **Location Updates**: Regular position updates
4. **Progress Monitoring**: Route step completion tracking

### Phase 4: Exception Handling
1. **Breakdown Detection**: System creates breakdown entry
2. **New Trip Creation**: Generate replacement trip
3. **Resource Reallocation**: Assign new vehicle/driver
4. **Continuity**: Maintain cargo and route integrity

### Phase 5: Trip Completion
1. **Final Updates**: Complete all route steps
2. **Reconciliation**: Verify all expenses and fuel usage
3. **Completion**: Mark trip as completed
4. **Resource Release**: Free vehicle and driver

---

## Python Backend Functionality

### 1. Automatic Trip Setup

```python
def before_insert(self):
    self.set_route_steps()          # Copy route steps
    if self.transporter_type == "In House":
        self.set_fuel_stock()       # Set fuel allocation
        self.set_expenses()         # Generate expense requests
```

### 2. Validation Rules

```python
def validate_request_status(self):
    # Ensure all requests approved/rejected before submission
    for row in self.fuel_request_history:
        if row.status not in ["Rejected", "Approved"]:
            frappe.throw("All fuel requests must be approved or rejected")
        if row.status == "Approved" and not row.purchase_order:
            frappe.throw("Approved fuel requests need Purchase Orders")
```

### 3. Integration Functions

```python
@frappe.whitelist()
def create_fund_jl(doc, row):
    # Create Journal Entry for approved funds
    # Handle multi-currency transactions
    # Set accounting dimensions
```

---

## Approval Workflows

### Fund Approval Process
1. **Requested Payment**: System creates payment request document
2. **Review**: Accountant evaluates each expense
3. **Decision**: Approve/reject with reasons
4. **Journal Entry**: Create payment voucher for approved funds
5. **Tracking**: Monitor payment status

### Fuel Approval Process
1. **Fuel Requests**: System creates fuel request document
2. **Validation**: Supervisor checks quantities and suppliers
3. **Approval**: Approve/reject individual requests
4. **Procurement**: Generate Purchase Orders
5. **Stock Management**: Process stock entries

---

## Status Management

### Trip Status Progression
- **Pending**: Initial state, configuration in progress
- **In Progress**: Trip submitted and active
- **Breakdown**: Vehicle breakdown occurred
- **Completed**: Trip finished successfully

### Approval Status Tracking
- **Requested**: Initial state for funds/fuel
- **Approved**: Management approval received
- **Rejected**: Request denied
- **Paid**: Payment processed (funds only)

---

## Integration Points

### ERPNext Integration
- **Stock Entry**: Fuel stock management
- **Purchase Order**: Fuel procurement
- **Journal Entry**: Financial transactions
- **Sales Invoice**: Customer billing (via Cargo Registration)

### Fleet Management Integration
- **Truck Status**: Vehicle availability updates
- **Driver Assignment**: Driver availability tracking
- **Route Management**: Route execution tracking
- **Manifest Linking**: Cargo-trip relationship

---

## Reporting and Analytics

### Standard Reports
- **Trip Report and Expenses**: Complete trip financial analysis
- **Fuel Expense By Trip**: Detailed fuel consumption tracking

### Key Performance Indicators
- Trip completion rate
- Fuel efficiency by route
- Average trip duration
- Cost per kilometer
- Driver performance metrics
- Vehicle utilization rates

---

## Best Practices

### Pre-Trip Planning
1. **Complete Setup**: Ensure all approvals before trip start
2. **Resource Verification**: Confirm vehicle and driver availability
3. **Route Review**: Validate route steps and timing
4. **Documentation**: Verify all required documents attached

### During Trip Execution
1. **Regular Updates**: Maintain location tracking
2. **Exception Reporting**: Promptly report issues or delays
3. **Fuel Management**: Monitor consumption vs. plan
4. **Communication**: Keep stakeholders informed

### Post-Trip Activities
1. **Completion Verification**: Confirm all deliveries made
2. **Financial Reconciliation**: Match actual vs. planned costs
3. **Performance Review**: Analyze efficiency metrics
4. **Documentation**: Complete all trip records

---

The Trips doctype provides comprehensive control over transportation operations, ensuring efficient execution while maintaining complete financial and operational visibility throughout the trip lifecycle.