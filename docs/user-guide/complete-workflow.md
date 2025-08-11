# Complete Fleet Management Workflow Guide

This comprehensive guide walks you through the complete end-to-end process of using the VSD Fleet Management System, from initial setup to trip completion and invoicing.


## Prerequisites: Master Data Setup

Before handling any customer transactions, ensure all master data is properly configured:

### Required Master Data
- **Trucks**: Vehicle details, license plates, fuel warehouses
- **Trailers**: Trailer specifications and types  
- **Truck Drivers**: Driver profiles with documents and employee links
- **Fuel UOM**: Fuel measurement units (Liters, Gallons)
- **Trip Locations**: All pickup and delivery locations
- **Trip Location Types**: Loading Point, Offloading Point, Border Point, etc.
- **Cargo Types**: Categories of cargo your fleet handles
- **Trip Routes**: Predefined routes with steps, distances, and fuel consumption
- **Trip Fixed Expenses**: Standard costs per route (tolls, permits, driver allowances)
- **Transport Settings**: System-wide configurations and accounting dimensions

### Critical Configuration: Transport Settings
The Transport Settings doctype is essential for system operation:
- **Fuel Item**: Default fuel item for stock management
- **Vehicle Fuel Parent Warehouse**: Main fuel storage location
- **Accounting Dimensions**: Map transactions to cost centers and dimensions
- **Account Groups**: Define expense and cash account categories

---

## Customer Service Workflow

### Phase 1: Cargo Registration

When a customer requests transportation services:

#### 1.1 Create Cargo Registration
1. Navigate to **Transactions → Cargo Registration**
2. Click **New**
3. Enter:
   - **Customer**: Select from Customer master
   - **Transport Type**: Cross Border or Internal
   - **Posting Date**: Auto-filled, read-only

#### 1.2 Add Cargo Details
In the **Cargo Details** child table, add each cargo item:

**Critical Planning Note**: Each row should represent one vehicle's capacity. If you have cargo requiring multiple vehicles, create separate rows for each vehicle.

For each cargo row, specify:
- **Container Size**: Loose, 20 FT, or 40 FT
- **Container Number**: Required for containerized cargo
- **BL Number**: Bill of Lading reference
- **Seal Number**: For sealed containers
- **Net Weight (kg)**: Automatically converts to tonnes
- **Number of Packages**: Count of items
- **Cargo Route**: Link to predefined Trip Routes
- **Loading/Offloading Dates**: Expected dates
- **Location Details**: 
  - Cargo Location Country/City (pickup)
  - Cargo Destination Country/City (delivery)
- **Service Charges**:
  - Service Item: Transportation service item
  - Currency: Billing currency
  - Rate: Price per unit

#### 1.3 Create Customer Invoice
Before proceeding to manifest creation:
1. Select specific cargo rows using checkboxes
2. Click **Create Invoice** button
3. System generates Sales Invoice with:
   - Vehicle details (when assigned)
   - Route information
   - Service charges
   - Automatic weight-based billing (if enabled)

**Important**: Create invoice before submitting Cargo Registration.

---

### Phase 2: Vehicle Assignment via Manifest

#### 2.1 Assign Cargo to Manifest
From any cargo detail row:
1. Click **Assign Manifest** button
2. System opens dialog showing:
   - Existing manifests for the same route
   - Available manifests with truck and driver details
3. Choose between:
   - **Assign to Existing Manifest**: Add to current manifest
   - **Create New Manifest**: Start fresh manifest

#### 2.2 Configure Manifest Details
In the Manifest form:
- **Transporter Type**: In House or Sub-Contractor
- **Trip Route**: Inherited from cargo
- **Posting Date**: Auto-filled

**For In House Operations**:
- **Truck**: Select available idle truck
- **Assigned Driver**: Choose active, available driver
- **Has Trailers**: Check if trailers needed
- **Trailer Selection**: Up to 3 trailers supported

**For Sub-Contractor Operations**:
- **Sub-Contractor Name**: Name of contractor
- **Truck License Plate**: External truck details
- **Driver Name**: Sub-contractor's driver
- **License Number**: External driver's license

#### 2.3 Cargo Allocation
In the **Manifest Cargo Details** section:
- **Cargo Allocation**: Choose Truck or Trailers
- **Specific Allocation**: Select exact truck/trailer
- System calculates **Manifest Total Weight**

#### 2.4 Submit Manifest
After configuration, submit the manifest to lock vehicle assignment.

---

### Phase 3: Trip Creation and Management

#### 3.1 Create Vehicle Trip
After manifest submission:
1. Click **Create Vehicle Trip** button
2. System automatically creates trip with:
   - Route steps from Trip Routes master
   - Fixed expenses from route configuration
   - Automatic fuel allocation based on route
   - Truck assignment and status update

#### 3.2 Trip Tabs Overview

##### Tab 1: Trip Details
- **Basic Information**: Manifest, route, dates
- **Vehicle Details**: Truck/trailer assignments
- **Driver Information**: In-house or sub-contractor details
- **Summary**: Total distance and fuel consumption

##### Tab 2: Route Steps
Pre-populated from Trip Routes master:
- **Location**: Each stop along the route
- **Distance**: Kilometers between stops
- **Fuel Consumption**: Liters per segment
- **Location Type**: Loading, offloading, border points
- **Dates**: Fill actual loading/offloading dates

##### Tab 3: Side Trips
For deviations from main route:
- **Additional stops** not in main route
- **Extra fuel consumption**
- **Additional distance**
- System recalculates totals automatically

##### Tab 4: Location Updates
Real-time tracking:
- **Manual Updates**: Driver location input
- **GPS Integration**: Automatic location tracking
- **View on Map**: Google Maps integration

##### Tab 5: Trip Funds
**Automatic Generation**: Based on Trip Routes fixed expenses
- **Expense Type**: Tolls, permits, allowances
- **Amount**: Predefined amounts per route
- **Currency**: USD or TZS
- **Status**: Requested → Approved → Paid
- **Accounts**: Expense and payable accounts

**Fund Approval Process**:
1. System creates **Requested Payment** document
2. Accountant reviews and approves/rejects
3. Approved funds show "Approved" status
4. **Disburse Funds** button creates Journal Entry

##### Tab 6: Fuel Management
**Fuel Request Process**:
1. Fill fuel requirements:
   - **Item Code**: Fuel item from settings
   - **Quantity**: Liters needed
   - **Disbursement Type**: Cash/Credit
   - **Supplier**: Fuel supplier
   - **Cost per Liter**: Current fuel price
2. Status: Requested → Approved → Ordered

**Fuel Approval Workflow**:
- Requests appear in **Fuel Requests** doctype
- Supervisor approves/rejects requests
- **Create Purchase Order**: Generate PO for approved fuel
- **Reduce Stock**: Create stock entry for fuel consumption

##### Tab 7: Trip Status
- **Trip Status**: Pending → Completed → Breakdown
- **Approval Status**: Fund and fuel approval summary
- **Trip Completion**: Mark as completed when finished

---

### Phase 4: Approval Workflows

#### 4.1 Fund Approval Process
1. **Requested Payment** document created automatically
2. Accountant receives notification
3. Review each fund request:
   - **Approve**: Funds available for disbursement
   - **Reject**: Request denied with reason
4. Approved funds enable Journal Entry creation
5. Payment tracking through Journal Entries

#### 4.2 Fuel Approval Process
1. **Fuel Requests** document tracks all requests
2. Fuel supervisor reviews:
   - Verify quantities against route requirements
   - Check supplier rates
   - Approve/reject individual requests
3. Approved requests enable:
   - Purchase Order creation
   - Stock entry processing
   - Supplier payment processing

---

### Phase 5: Trip Execution

#### 5.1 Pre-Trip Requirements
Before trip submission, ensure:
- All fund requests approved/rejected
- All fuel requests approved/rejected
- Approved fuel requests have Purchase Orders
- Approved fund requests have Journal Entries
- Stock out entry created for fuel

#### 5.2 Trip Submission
Submit trip to start journey:
- Truck status changes to "On Trip"
- Driver marked as "In Trip"
- Trip becomes read-only for modifications

#### 5.3 Trip Operations
Available actions during trip:
- **Complete Trip**: Mark as finished
- **Create Breakdown**: Handle vehicle breakdowns
- **Location Updates**: Track progress
- **Return Trip**: For round trips

#### 5.4 Breakdown Management
If breakdown occurs:
1. Click **Create Breakdown Entry**
2. Fill breakdown details:
   - Date and time
   - Location
   - Description of issue
3. System creates **Allocate New Vehicle Trip** option
4. New trip inherits cargo and route details
5. Original trip marked as "Re-Assigned"

---

### Phase 6: Trip Completion

#### 6.1 Complete Trip Process
1. Update final locations and dates
2. Complete all fuel transactions
3. Click **Complete Trip** button
4. System updates:
   - Truck status to "Idle"
   - Driver availability
   - Trip completion date

#### 6.2 Financial Reconciliation
- Review all Journal Entries
- Confirm Purchase Orders received
- Update stock entries
- Generate expense reports

---

## Reporting and Analytics

### Standard Reports
1. **Trip Report and Expenses**: Complete trip overview with costs
2. **Fuel Expense By Trip**: Detailed fuel consumption analysis

### Key Metrics
- Trip profitability per route
- Fuel efficiency tracking
- Vehicle utilization rates
- Driver performance metrics
- Customer service levels

---

## Best Practices

### Data Management
- Register cargo by vehicle capacity for accurate manifests
- Maintain updated master data for smooth operations
- Regular reconciliation of fuel and expense accounts

### Workflow Efficiency
- Pre-approve standard route expenses
- Maintain fuel supplier agreements
- Regular vehicle inspections
- Driver training on system usage

### Compliance
- Ensure all required documents attached
- Regular backup of transaction data
- Audit trail maintenance
- Regulatory reporting preparation

---

This workflow ensures complete traceability from customer cargo registration through trip completion and financial settlement, providing comprehensive fleet management capabilities for both internal and sub-contractor operations.