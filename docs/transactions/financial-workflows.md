# Financial Workflows: Fund and Fuel Management

The VSD Fleet Management System includes sophisticated financial management workflows for handling trip expenses and fuel procurement. These processes ensure proper authorization, tracking, and accounting for all transportation-related costs.

---

## Overview of Financial Processes

### Two Primary Financial Workflows
1. **Trip Fund Management**: Handling fixed expenses, driver allowances, and operational costs
2. **Fuel Request Management**: Managing fuel procurement, approval, and stock management

### Integration with ERPNext
- **Journal Entries**: Automatic creation for approved funds
- **Purchase Orders**: Generated for approved fuel requests
- **Stock Entries**: Fuel stock management and consumption
- **Accounting Dimensions**: Automatic dimension setting for financial tracking

---

## Trip Fund Management Workflow

### 1. Automatic Fund Request Generation

When a trip is created, the system automatically generates fund requests based on the route's fixed expenses:

```python
def set_expenses(self):
    reference_route = frappe.get_doc("Trip Routes", self.route)
    for row in reference_route.fixed_expenses:
        fixed_expense_doc = frappe.get_doc("Fixed Expenses", row.expense)
        new_row = self.append("requested_fund_accounts_table", {
            "requested_date": nowdate(),
            "request_amount": row.amount,
            "request_currency": row.currency,
            "request_status": "Requested",
            "expense_type": row.expense,
            "expense_account": fixed_expense_doc.expense_account,
            "payable_account": fixed_expense_doc.cash_bank_account,
            "party_type": row.party_type,
        })
```

### 2. Requested Payment Document

The system creates a **Requested Payment** document that aggregates all fund requests for approval:

#### Document Structure
- **Header Information**: Company, truck, driver, manifest details
- **Requested Funds**: All pending fund requests
- **Approval Section**: Approved/rejected requests
- **Status Tracking**: Overall approval and payment status

#### Key Features
- **Approve/Reject Buttons**: Individual request management
- **Real-time Totals**: USD and TZS summaries
- **Status Updates**: Automatic status progression
- **Payment Tracking**: Journal entry linking

### 3. Fund Approval Process

#### Approval Interface
```javascript
// Approve/Reject buttons with status tracking
cur_frm.cscript.approve_request = function(frm) {
    // Move from requested to approved status
    // Update totals and payment status
};

cur_frm.cscript.reject_request = function(frm) {
    // Move to rejected status with reason
    // Update approval tracking
};
```

#### Business Logic
1. **Individual Review**: Each expense item reviewed separately
2. **Status Progression**: Requested → Approved/Rejected
3. **Automatic Totaling**: Real-time calculation of approved amounts
4. **Payment Status**: Waiting Approval → Waiting Payment → Paid

### 4. Journal Entry Creation

For approved fund requests, the system creates Journal Entries:

```python
@frappe.whitelist()
def create_fund_jl(doc, row):
    # Multi-currency handling
    if company_currency != row.request_currency:
        multi_currency = 1
        exchange_rate = get_exchange_rate(row.request_currency, company_currency)
    
    # Create Journal Entry with proper accounts
    jv_doc = frappe.get_doc(dict(
        doctype="Journal Entry",
        posting_date=row.requested_date,
        accounts=accounts,
        company=doc.company,
        multi_currency=multi_currency,
    ))
    
    # Set accounting dimensions
    set_dimension(doc, jv_doc)
    jv_doc.save()
```

---

## Fuel Request Management Workflow

### 1. Fuel Request Creation

Fuel requests are created within the Trip doctype's Fuel tab:

#### Required Information
- **Item Code**: Fuel item from Transport Settings
- **Quantity**: Liters required
- **Cost per Liter**: Current fuel price
- **Supplier**: Fuel supplier
- **Disbursement Type**: Cash or Credit
- **Currency**: USD or TZS

### 2. Fuel Requests Document

The **Fuel Requests** doctype aggregates all fuel requirements:

#### Document Features
- **Trip Reference**: Links to originating trip
- **Vehicle Information**: Truck and driver details
- **Route Context**: Main and return route information
- **Request Management**: Pending, approved, and rejected requests

#### Custom Load Function
```python
def load_from_db(self):
    # Custom loading for approved/rejected requests
    children_main_approved = frappe.db.get_values(
        "Fuel Requests Table",
        {
            "parent": self.get("reference_docname"),
            "status": "Approved",
        },
        "*", as_dict=True
    )
    # Set approved requests in document
```

### 3. Fuel Approval Process

#### Approval Interface
- **Requested Fuel Section**: Pending requests
- **Approve Buttons**: Individual request approval
- **Approved/Rejected Section**: Processed requests
- **Status Tracking**: Overall request status

#### Validation Rules
```python
def validate_request_status(self):
    for row in self.fuel_request_history:
        if row.status not in ["Rejected", "Approved"]:
            frappe.throw("All fuel requests must be approved or rejected")
        if row.status == "Approved" and not row.purchase_order:
            frappe.throw("Approved requests need Purchase Orders")
```

### 4. Purchase Order Generation

For approved fuel requests, Purchase Orders are created:

```python
@frappe.whitelist()
def create_purchase_order(request_doc, item):
    doc = frappe.new_doc("Purchase Order")
    doc.company = request_doc.company
    doc.supplier = item.supplier
    doc.currency = item.currency
    doc.set_warehouse = set_warehouse
    
    new_item = doc.append("items", {})
    new_item.item_code = item.item_code
    new_item.qty = item.quantity
    new_item.rate = item.cost_per_litre
    
    set_dimension(request_doc, doc)
    doc.insert(ignore_permissions=True)
```

### 5. Stock Entry Management

For fuel consumption tracking:

```python
@frappe.whitelist()
def create_stock_out_entry(doc, fuel_stock_out):
    fuel_item = frappe.get_value("Transport Settings", None, "fuel_item")
    warehouse = frappe.get_value("Truck", doc.truck_number, "trans_ms_fuel_warehouse")
    
    stock_entry_doc = frappe.get_doc(dict(
        doctype="Stock Entry",
        stock_entry_type="Material Issue",
        from_warehouse=warehouse,
        items=[{"item_code": fuel_item, "qty": float(fuel_stock_out)}],
    ))
    
    set_dimension(doc, stock_entry_doc)
    stock_entry_doc.insert(ignore_permissions=True)
```

---

## Real-time Financial Tracking

### Dashboard Summaries

#### Trip Funds Display
```javascript
function approved_total() {
    var total_request_tsh = 0;
    var total_request_usd = 0;
    
    cur_frm.doc.requested_fund_accounts_table.forEach(function (row) {
        if (row.request_currency == 'TZS' && row.request_status == "Approved") {
            total_request_tsh += row.request_amount;
        }
    });
    
    // Update HTML display with totals
    cur_frm.get_field("html2").wrapper.innerHTML = 
        '<p>Total Amount Approved</p><b>USD ' + total_request_usd.toLocaleString() + 
        ' <br> TZS ' + total_request_tsh.toLocaleString() + '</b>';
}
```

#### Fuel Tracking
```javascript
function fuel_amount() {
    var approved_fuel = 0;
    var requested_fuel = 0;
    var rejected_fuel = 0;
    
    cur_frm.doc.fuel_request_history.forEach(function (row) {
        if (row.status == "Approved") {
            approved_fuel += row.quantity;
        }
    });
    
    // Display fuel summaries
}
```

---

## Accounting Dimension Integration

### Automatic Dimension Setting

The system automatically applies accounting dimensions to financial transactions:

```python
def set_dimension(src_doc, tr_doc, src_child=None, tr_child=None):
    set = frappe.get_cached_doc("Transport Settings", "Transport Settings")
    for dim in set.accounting_dimension:
        if dim.source_doctype == src_doc.doctype and dim.target_doctype == tr_doc.doctype:
            if dim.source_type == "Field":
                value = src_doc.get(dim.source_field_name)
            elif dim.source_type == "Value":
                value = dim.value
            
            if dim.target_type == "Main":
                setattr(tr_doc, dim.target_field_name, value)
```

### Supported Dimensions
- **Truck**: Vehicle-based cost tracking
- **Route**: Route-based profitability analysis
- **Driver**: Driver performance metrics
- **Customer**: Customer profitability tracking

---

## Multi-Currency Support

### Currency Handling
- **Base Currency**: TZS (Tanzanian Shilling)
- **Foreign Currency**: USD (US Dollar)
- **Exchange Rates**: Automatic rate fetching
- **Conversion Logic**: Proper multi-currency accounting

### Exchange Rate Management
```python
if company_currency != row.request_currency:
    multi_currency = 1
    exchange_rate = get_exchange_rate(row.request_currency, company_currency)
    debit_amount = row.request_amount * exchange_rate
else:
    multi_currency = 0
    exchange_rate = 1
    debit_amount = row.request_amount
```

---

## Status Management and Validation

### Fund Request Statuses
- **Requested**: Initial state, awaiting approval
- **Approved**: Management approved, ready for payment
- **Rejected**: Request denied with reason
- **Paid**: Payment completed (Journal Entry created)

### Fuel Request Statuses
- **Requested**: Initial state, awaiting approval
- **Approved**: Approved for procurement
- **Rejected**: Request denied
- **Ordered**: Purchase Order created

### Validation Gates
1. **Trip Submission**: All requests must be approved/rejected
2. **Fund Disbursement**: Approved funds need Journal Entries
3. **Fuel Procurement**: Approved fuel needs Purchase Orders
4. **Stock Management**: Fuel consumption requires Stock Entries

---

## Best Practices

### Fund Management
1. **Timely Approval**: Process requests promptly for smooth operations
2. **Proper Documentation**: Maintain clear approval reasons
3. **Budget Control**: Monitor expense patterns and limits
4. **Regular Reconciliation**: Match actual vs. planned expenses

### Fuel Management
1. **Market Pricing**: Regular fuel price updates
2. **Supplier Management**: Maintain approved supplier list
3. **Consumption Tracking**: Monitor fuel efficiency patterns
4. **Stock Control**: Maintain adequate fuel inventory

### Financial Controls
1. **Segregation of Duties**: Separate request and approval roles
2. **Approval Limits**: Define authorization levels
3. **Audit Trail**: Maintain complete transaction history
4. **Regular Reports**: Monitor financial performance

---

## Reporting and Analytics

### Standard Reports
- **Trip Report and Expenses**: Complete financial analysis per trip
- **Fuel Expense By Trip**: Detailed fuel cost tracking
- **General Ledger**: Accounting impact analysis

### Key Metrics
- **Cost per Trip**: Total expenses per transportation job
- **Fuel Efficiency**: Consumption vs. planned ratios
- **Approval Rates**: Request approval/rejection patterns
- **Payment Timing**: Average payment processing time

---

The financial workflow systems ensure complete control and visibility over transportation costs while maintaining integration with ERPNext's accounting framework for comprehensive financial management.