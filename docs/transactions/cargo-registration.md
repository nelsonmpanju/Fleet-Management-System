# Cargo Registration: Customer Service Entry Point
The **Cargo Registration** doctype is the primary entry point for all customer transportation requests. This document captures customer cargo details and initiates the fleet management workflow.

## Purpose and Scope

Cargo Registration serves multiple critical functions:
- **Customer Request Management**: Central repository for all transportation requests
- **Cargo Specification**: Detailed cargo characteristics and requirements  
- **Service Pricing**: Rate definition and invoice generation
- **Workflow Initiation**: Starting point for manifest and trip creation
- **Compliance Documentation**: Required shipping and regulatory information

---

## Document Structure

### Header Information
| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Customer** | Link | Customer requesting service | Yes |
| **Transport Type** | Select | Cross Border / Internal | Yes |
| **Posting Date** | Date | Registration date (auto-filled) | Yes |
| **Company** | Link | Your company entity | Yes |

### Cargo Details (Child Table)
Each row represents cargo requiring one vehicle:

#### Cargo Identification
- **Cargo ID**: Auto-generated unique identifier
- **Container Size**: Loose / 20 FT / 40 FT
- **Container Number**: Required for containerized cargo
- **BL Number**: Bill of Lading reference
- **Seal Number**: Container seal (for sealed containers)

#### Cargo Specifications  
- **Cargo Type**: Link to Cargo Types master
- **Net Weight (kg)**: Cargo weight in kilograms
- **Number of Packages**: Count of individual packages
- **Cargo Route**: Link to predefined Trip Routes

#### Location Information
- **Cargo Location Country/City**: Pickup location
- **Cargo Destination Country/City**: Delivery destination  
- **Expected Loading Date**: Planned pickup date
- **Expected Offloading Date**: Planned delivery date

#### Service Charges
- **Service Item**: Transportation service from Item master
- **Currency**: Billing currency (USD/TZS)
- **Rate**: Price per unit/service

#### Assignment Tracking
- **Manifest Number**: Assigned manifest (auto-filled)
- **Transporter Type**: In House / Sub-Contractor (auto-filled)
- **Assigned Truck/Driver**: Vehicle assignment details
- **Created Trip**: Generated trip reference
- **Sales Invoice**: Generated invoice reference

---

## Key Features and Functionality

### 1. Intelligent Cargo Planning
**Best Practice**: Each cargo detail row should represent one vehicle's capacity.
- For multi-vehicle cargo, create separate rows per vehicle
- System validates location relationships
- Automatic weight conversion (kg to tonnes)
- Date validation (loading before offloading)

### 2. Dynamic Location Filtering
JavaScript implementation automatically filters cities based on selected countries:
```javascript
// Automatic city filtering based on country selection
cargo_location_city_filter(frm, cdt, cdn);
cargo_destination_city_filter(frm, cdt, cdn);
```

### 3. Invoice Generation Workflow
The **Create Invoice** button generates customer invoices:
- Select specific cargo rows using checkboxes
- System creates Sales Invoice with:
  - Vehicle details (when assigned)
  - Route information  
  - Service charges
  - Optional weight-based billing

**Important**: Create invoice before submitting Cargo Registration.

### 4. Manifest Assignment Integration
Each cargo row includes **Assign Manifest** button:
- Opens dialog showing available manifests for the route
- Displays truck and driver details
- Options to assign to existing or create new manifest
- Seamless integration with vehicle assignment

---

## Business Process Flow

### Step 1: Customer Request
1. Customer contacts for transportation service
2. Create new Cargo Registration
3. Enter customer and transport type

### Step 2: Cargo Documentation
1. Add cargo details row for each vehicle needed
2. Specify container/package details
3. Define pickup and delivery locations
4. Set expected dates

### Step 3: Service Pricing
1. Select appropriate service item
2. Define currency and rate
3. Consider weight-based billing options

### Step 4: Invoice Generation
1. Select cargo rows for billing
2. Click Create Invoice
3. Review generated Sales Invoice
4. Send to customer for approval

### Step 5: Vehicle Assignment
1. Click Assign Manifest on cargo rows
2. Choose existing manifest or create new
3. System initiates vehicle assignment workflow

---

## Validation Rules

### Automatic Validations
- **Date Logic**: Loading date must be before offloading date
- **Weight Conversion**: Automatic kg to tonnes calculation
- **Location Relationships**: City must belong to selected country
- **Service Items**: Must be from "Services" item group

### Business Rules
- Cannot modify cargo after manifest assignment
- Invoice creation locks cargo specifications
- Container number mandatory for containerized cargo
- Route selection drives available manifests

---

## Integration Points

### Upstream Dependencies
- **Customer Master**: Valid customer required
- **Item Master**: Service items for billing
- **Trip Routes**: Available transportation routes
- **Cargo Types**: Cargo classification
- **Transport Locations**: Pickup/delivery points

### Downstream Processes
- **Sales Invoice**: Customer billing
- **Manifest**: Vehicle assignment
- **Trips**: Transportation execution
- **Fuel Requests**: Fuel planning
- **Requested Payment**: Expense management

---

## JavaScript Functionality

### Form Behavior
```javascript
// Auto-fill posting date and make read-only
if (!frm.doc.posting_date) {
    frm.set_value('posting_date', frappe.datetime.nowdate());
    frm.set_df_property('posting_date', 'read_only', 1);
}
```

### Invoice Creation
```javascript
create_invoice: function(frm) {
    let selected = frm.get_selected().cargo_details;
    if (selected) {
        let rows = frm.doc.cargo_details.filter(i => 
            selected.includes(i.name) && !i.invoice);
        // Generate invoice for selected rows
    }
}
```

### Manifest Assignment Dialog
- Dynamic table generation showing available manifests
- Single-selection checkbox behavior
- Integration with manifest creation/assignment APIs

---

## Reporting and Analytics

### Key Metrics
- Cargo registration volume by customer
- Average weight per vehicle type
- Route utilization patterns
- Service pricing analysis
- Time from registration to delivery

### Standard Reports
- Cargo registration summary
- Customer service analysis
- Route demand planning
- Vehicle capacity utilization

---

## Best Practices

### Data Entry Guidelines
1. **Accurate Planning**: One row per vehicle ensures proper resource allocation
2. **Complete Information**: Fill all required fields for smooth processing
3. **Realistic Dates**: Set achievable loading/offloading dates
4. **Proper Classification**: Select correct cargo types for compliance

### Workflow Optimization
1. **Batch Processing**: Group similar cargo for efficient manifest creation
2. **Early Invoicing**: Generate invoices promptly for cash flow
3. **Route Consolidation**: Combine compatible cargo on same routes
4. **Regular Review**: Monitor pending assignments and follow up

### Quality Control
1. **Weight Verification**: Confirm actual vs. declared weights
2. **Documentation**: Ensure all required documents attached
3. **Customer Communication**: Keep customers informed of status
4. **Compliance Check**: Verify regulatory requirements met

---

The Cargo Registration doctype forms the foundation of your fleet management operations, ensuring accurate customer service delivery from initial request through final delivery.