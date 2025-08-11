# Manifest Management: Vehicle Assignment and Trip Planning

The **Manifest** doctype serves as the critical bridge between cargo registration and trip execution, handling vehicle assignment, trailer allocation, and cargo organization for efficient transportation operations.

---

## Purpose and Scope

Manifest management encompasses:
- **Vehicle Assignment**: Linking cargo to specific trucks and drivers
- **Trailer Management**: Allocating appropriate trailers for cargo types
- **Cargo Organization**: Optimizing load distribution across vehicles
- **Trip Preparation**: Setting up complete vehicle-cargo combinations
- **Transporter Coordination**: Managing both in-house and sub-contractor operations

---

## Document Structure

### Header Information
| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Trip Route** | Link | Transportation route | Yes |
| **Transporter** | Select | In House / Sub-Contractor | Yes |
| **Vehicle Trip** | Link | Generated trip reference | Auto-filled |
| **Date** | Date | Manifest creation date | Yes |

### In-House Operations
| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Truck Number** | Link | Selected vehicle | Yes |
| **Truck License Plate** | Data | Vehicle registration | Auto-filled |
| **Assigned Driver** | Link | Selected driver | Yes |
| **Driver Name** | Data | Driver full name | Auto-filled |

### Sub-Contractor Operations  
| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Sub-Contractor Name** | Data | Contractor company | Yes |
| **Truck License Plate** | Data | External vehicle plate | Yes |
| **Driver Name** | Data | External driver name | Yes |
| **Driver License Number** | Data | External license | Optional |

### Trailer Configuration
| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| **Has Trailers** | Check | Enable trailer selection | No |
| **Trailer 1/2/3** | Link | Up to 3 trailers | Conditional |
| **Trailer Types** | Data | Auto-filled trailer specs | Auto |

---

## Key Features and Functionality

### 1. Dynamic Vehicle Assignment

#### Truck Selection Logic
```javascript
// Filter for idle, enabled trucks
frm.set_query("truck", function () {
    return {
        filters: {
            status: "Idle",
            disabled: 0
        }
    };
});
```

#### Driver Assignment
```javascript
// Filter for active, available drivers
frm.set_query("assigned_driver", function () {
    return {
        filters: {
            in_trip: 0,
            status: "Active"
        }
    };
});
```

### 2. Intelligent Trailer Management

#### Cascade Selection
- **Trailer 1**: Must be selected before Trailer 2
- **Trailer 2**: Must be selected before Trailer 3
- **Dependency Validation**: Removing parent trailer clears child trailers

#### Duplicate Prevention
```javascript
function filters_for_trailers(trailer_names) {
    // Prevent same trailer selection multiple times
    cur_frm.set_query("trailer_1", function () {
        return {
            filters: {
                disabled: 0,
                name: ["not in", trailer_names]
            }
        };
    });
}
```

### 3. Cargo Allocation System

#### Allocation Options
- **Truck**: Assign cargo directly to truck
- **Trailers**: Distribute cargo across trailers

#### Smart Allocation Logic
```javascript
cargo_allocation: function(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    if (row.cargo_allocation == "Truck") {
        if (!frm.doc.truck) {
            frappe.msgprint("Please select truck before Allocating cargo to Truck");
            return;
        }
        row.specific_cargo_allocated = frm.doc.truck;
    }
}
```

### 4. Weight Management
- **Automatic Calculation**: Total manifest weight from all cargo
- **Real-time Updates**: Weight recalculation on cargo changes
- **Load Validation**: Ensure weight limits not exceeded

---

## Business Process Flow

### Phase 1: Manifest Creation
1. **From Cargo Registration**: Click "Assign Manifest" on cargo row
2. **Dialog Selection**: Choose existing manifest or create new
3. **Route Validation**: System filters manifests by route

### Phase 2: Vehicle Configuration
1. **Transporter Type**: Select In House or Sub-Contractor
2. **Vehicle Selection**: Choose truck (filters for available vehicles)
3. **Driver Assignment**: Select driver (filters for available drivers)
4. **Trailer Setup**: Configure trailers if needed

### Phase 3: Cargo Organization
1. **Cargo Details**: Review assigned cargo
2. **Allocation Strategy**: Assign cargo to truck or specific trailers
3. **Weight Distribution**: Ensure balanced loading
4. **Final Review**: Verify all assignments correct

### Phase 4: Manifest Submission
1. **Validation**: System checks all required fields
2. **Vehicle Lock**: Truck status changes to "On Trip"
3. **Trip Creation**: "Create Vehicle Trip" button becomes available

---

## JavaScript Functionality

### 1. Dynamic Form Behavior

#### Transporter Type Switching
```javascript
transporter_type: (frm) => {
    var transporter_type = frm.doc.transporter_type;
    if (transporter_type === 'Sub-Contractor') {
        // Hide in-house fields, show sub-contractor fields
        frm.doc.manifest_cargo_details.forEach(function(row) {
            row.transporter_type = 'Sub-Contractor';
            row.sub_contractor_cargo_allocation = '';
        });
    }
}
```

#### Trailer Dependency Management
```javascript
trailer_1: function(frm) {
    if (!frm.doc.trailer_1) {
        // Clear dependent trailers
        frm.doc.trailer_2 = "";
        frm.doc.trailer_3 = "";
    }
    // Update filters for remaining trailers
    filters_for_trailers(trailer_names);
}
```

### 2. Cargo Dialog Integration

#### Add Cargo to Manifest
```javascript
function showCargoDialog(data) {
    var dialog = new frappe.ui.Dialog({
        title: __("Cargo Details"),
        fields: [
            {
                fieldname: 'cargo_list',
                fieldtype: 'Table',
                data: data,
            }
        ],
        primary_action: function() {
            // Process selected cargo
        }
    });
}
```

---

## Validation Rules

### Business Logic Validations
1. **Vehicle Availability**: Only idle trucks can be assigned
2. **Driver Availability**: Only available drivers can be assigned
3. **Trailer Sequence**: Must select trailers in order (1, 2, 3)
4. **Weight Limits**: Manifest weight cannot exceed vehicle capacity
5. **Route Consistency**: All cargo must be on same route

### System Enforced Rules
1. **Unique Assignments**: Same vehicle cannot be on multiple active manifests
2. **Status Validation**: Submitted manifests cannot be modified
3. **Dependency Checks**: Driver must belong to assigned truck (for defaults)

---

## Integration Points

### Upstream Dependencies
- **Cargo Registration**: Source of cargo to be manifested
- **Truck Master**: Available vehicles and specifications
- **Truck Driver**: Available drivers and qualifications
- **Trailer Master**: Available trailers and types
- **Trip Routes**: Route definitions and requirements

### Downstream Processes
- **Trips**: Vehicle trip creation from manifest
- **Fuel Requests**: Automatic fuel planning
- **Requested Payment**: Trip expense planning
- **Vehicle Status**: Truck availability updates

---

## Advanced Features

### 1. Cargo Addition Workflow
```javascript
// Add cargo to existing manifest
frm.add_custom_button(__('Add Cargo to Manifest'), function () {
    frappe.call({
        method: "vsd_fleet_ms.custom.custom_functions.add_to_manifest",
        args: { route_starting_point: frm.doc.route_starting_point },
        callback: function (r) {
            if (r.message) {
                showCargoDialog(r.message);
            }
        }
    });
});
```

### 2. Vehicle Trip Creation
```javascript
// Create trip from manifest
frm.add_custom_button(__('Vehicle Trip'), function () {
    frappe.call({
        method: "vsd_fleet_ms.vsd_fleet_ms.doctype.trips.trips.create_vehicle_trip_from_manifest",
        args: { args_array: trip_data },
        callback: function (r) {
            if (r.message) {
                frappe.set_route("Form", "Trips", r.message.name);
            }
        }
    });
}, __("Create"));
```

---

## Best Practices

### Efficient Manifest Planning
1. **Route Consolidation**: Group cargo by route for efficient manifests
2. **Vehicle Matching**: Match vehicle capacity to cargo requirements
3. **Driver Scheduling**: Consider driver availability and qualifications
4. **Trailer Optimization**: Use appropriate trailer types for cargo

### Quality Control
1. **Weight Verification**: Confirm manifest weight against vehicle capacity
2. **Documentation Review**: Ensure all required documents attached
3. **Route Validation**: Verify route matches cargo pickup/delivery points
4. **Resource Availability**: Double-check vehicle and driver availability

### Performance Optimization
1. **Batch Processing**: Process multiple cargo items in single manifest
2. **Advance Planning**: Create manifests ahead of scheduled trips
3. **Resource Allocation**: Balance workload across available fleet
4. **Contingency Planning**: Have backup vehicles/drivers identified

---

## Reporting and Analytics

### Key Metrics
- Manifest utilization rates
- Vehicle capacity optimization
- Driver assignment efficiency
- Trailer usage patterns
- Route consolidation opportunities

### Standard Reports
- Manifest summary by period
- Vehicle utilization analysis
- Driver assignment patterns
- Cargo consolidation metrics

---

The Manifest doctype ensures optimal vehicle-cargo matching while maintaining flexibility for both in-house and sub-contractor operations, forming the critical link between cargo registration and trip execution.