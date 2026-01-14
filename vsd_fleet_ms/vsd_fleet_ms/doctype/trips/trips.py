# Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from operator import mul
import frappe
import time
import datetime
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
import json
from frappe.utils import nowdate, cstr, cint, flt, comma_or, now
from frappe import _, msgprint
from frappe.model.document import Document
from vsd_fleet_ms.utils.dimension import set_dimension
from erpnext.setup.utils import get_exchange_rate
from vsd_fleet_ms.vsd_fleet_ms.doctype.requested_payment.requested_payment import request_funds

class Trips(Document):
    def before_submit(self):
        self.set_driver()
        self.validate_request_status()

    def on_submit(self):
        if self.transporter_type == "In House":
            if not self.stock_out_entry:
                frappe.throw(_("Stock Out Entry is not set"))

    def onload(self):

        if not self.company:
            self.company = frappe.defaults.get_user_default(
                "Company"
            ) or frappe.defaults.get_global_default("company")
        if not self.fuel_stock_out:
            self.fuel_stock_out = self.total_fuel

    def before_insert(self):
        self.set_route_steps()
        if self.transporter_type == "In House":
            self.set_fuel_stock()
            self.set_expenses()
        elif self.transporter_type == "Sub-Contractor":
            self.requested_fund_accounts_table = []

    def validate(self):
        if self.transporter_type == "In House":
            self.validate_fuel_requests()

        # self.set_permits()

    def on_update(self):
        """Update Round Trip when trip is modified"""
        if self.round_trip and not self.flags.ignore_round_trip_update:
            self.update_round_trip()

    def update_round_trip(self):
        """Update Round Trip child table with latest trip data"""
        try:
            round_trip = frappe.get_doc("Round Trip", self.round_trip)
            # Find this trip in the round trip's trip_details
            for trip_row in round_trip.trip_details:
                if trip_row.trip_id == self.name:
                    trip_row.trip_driver = self.driver_name
                    trip_row.trip_start_date = self.date
                    trip_row.trip_end_date = self.trip_completed_date
                    break

            # Update Round Trip status based on all trips
            round_trip.update_status()

            # Save without triggering recursive updates
            round_trip.flags.ignore_round_trip_update = True
            round_trip.save()
        except Exception as e:
            frappe.log_error(f"Error updating Round Trip {self.round_trip}: {str(e)}")

    def set_fuel_stock(self):
        self.fuel_stock_out = self.total_fuel

    def set_route_steps(self):
        reference_route = frappe.get_doc("Trip Routes", self.route)
        if len(reference_route.trip_steps) > 0:
            self.main_route_steps = []
            for row in reference_route.trip_steps:
                new_row = self.append("main_route_steps", {})
                new_row.location = row.location
                new_row.distance = row.distance
                new_row.fuel_consumption_qty = row.fuel_consumption_qty
                new_row.location_type = row.location_type


    def set_expenses(self):
        # reference_doc = frappe.get_doc(self.reference_doctype, self.reference_docname)
        # self.route = reference_doc.route
        reference_route = frappe.get_doc("Trip Routes", self.route)
        if len(reference_route.fixed_expenses) > 0:
            self.requested_fund_accounts_table = []
            for row in reference_route.fixed_expenses:
                fixed_expense_doc = frappe.get_doc("Fixed Expenses", row.expense)
                expense_account_doc = frappe.get_doc("Account", fixed_expense_doc.expense_account)
                payable_account_currency_doc = frappe.get_doc("Account", fixed_expense_doc.cash_bank_account)
                aday = nowdate()
                new_row = self.append("requested_fund_accounts_table", {})
                new_row.requested_date = aday
                new_row.request_amount = row.amount
                new_row.request_currency = row.currency
                new_row.request_status = "Requested"
                new_row.expense_type = row.expense
                new_row.expense_account = fixed_expense_doc.expense_account
                new_row.expense_account_currency = expense_account_doc.account_currency
                new_row.payable_account_currency = payable_account_currency_doc.account_currency
                new_row.payable_account = fixed_expense_doc.cash_bank_account
                new_row.party_type = row.party_type
                new_row.requested_by = frappe.session.user
                new_row.requested_on = now()
                if row.party_type == "Employee":
                    new_row.party = frappe.db.get_value(
                        "Truck Driver", self.assigned_driver, "employee"
                    )

    def set_driver(self):
        employee = None
        if self.transporter_type == "In House":
            if not self.assigned_driver:
                frappe.throw("Driver is not set")
            employee = frappe.db.get_value("Truck Driver", self.assigned_driver, "employee")
        elif self.transporter_type == "Sub-Contractor":
            if not self.sub_contactor_driver_name:
                frappe.throw("Driver Name is not set")

        # frappe.throw("EMP" + str(employee))
        for row in self.requested_fund_accounts_table:
            if row.party_type == "Employee":
                if employee:
                    row.party = employee

    # def set_permits(self):
    #     if self.main_cargo_category and not len(self.trip_permits):
    #         self.trip_permits = []
    #         cargo_category = frappe.get_doc(
    #             "Cargo Types", self.main_cargo_category
    #         )
    #         for row in cargo_category.permits:
    #             new_row = self.append("trip_permits", {})
    #             new_row.permit_name = row.permit_name
    #             new_row.mandatory = row.mandatory

    def before_save(self):
        if not self.date:
            self.date = datetime.datetime.now()
        # validate_requested_funds(self)
        self.validate_main_route_inputs()

    def validate_fuel_requests(self):
        make_request = False

        # Check main trip
        for request in self.get("fuel_request_history"):
            if request.status == "Open":
                make_request = True


        if make_request:
            existing_fuel_request = frappe.db.get_value(
                "Fuel Requests",
                {"reference_doctype": "Trips", "reference_docname": self.name},
            )

            # Timestamp
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            if existing_fuel_request:
                doc = frappe.get_doc("Fuel Requests", existing_fuel_request)
                doc.db_set("modified", timestamp)
                if "Fully Processed" == doc.status:
                    doc.db_set("status", "Partially Processed")
            else:
                fuel_request = frappe.new_doc("Fuel Requests")
                fuel_request.update(
                    {
                        "truck_plate_number": self.get("vehicle_plate_number"),
                        "customer": self.get("customer"),
                        "truck": self.get("vehicle_plate_number"),
                        "truck_driver": self.get("driver"),
                        "reference_doctype": "Trips",
                        "reference_docname": self.name,
                        "status": "Waiting Approval",
                    }
                )
                fuel_request.insert(ignore_permissions=True)

            # Mark the requests as open
            for request in self.get("fuel_request_history"):
                if request.status == "Open":
                    request.set("status", "Requested")
                    request.set("transaction_date", nowdate())


    def validate_main_route_inputs(self):
        loading_date = None
        offloading_date = None

        steps = self.get("main_route_steps")
        for step in steps:
            if step.location_type == "Loading Point":
                loading_date = step.loading_date
            if step.location_type == "Offloading Point":
                offloading_date = step.offloading_date
        if offloading_date and not loading_date:
            frappe.throw("Loading Date must be set before Offloading Date")

    def validate_request_status(self):
        for row in self.fuel_request_history:
            if row.status not in  ["Rejected", "Approved"]:
                frappe.throw("<b>All fuel requests must be on either approved or rejected before submitting the trip</b>")
            
            if row.status == "Approved" and not row.purchase_order:
                frappe.throw("<b>All approved fuel requests must have Purchase Order before submitting the trip</b>")
        
        for row in self.requested_fund_accounts_table:
            if row.request_status not in  ["Rejected", "Approved"]:
                frappe.throw("<b>All fund requests must be on either approved or rejected before submitting the trip</b>")
            
            if row.request_status == "Approved" and not row.journal_entry:
                frappe.throw("<b>All approved fund requests must have a Journal Entry before submitting the trip</b>")


@frappe.whitelist()
def create_vehicle_trip_from_manifest(args_array):
    args_dict = json.loads(args_array)
    vehicle_trip = frappe.new_doc("Trips")
    vehicle_trip.manifest = args_dict.get("manifest_name")
    vehicle_trip.transporter_type = args_dict.get("transporter_type")
    if vehicle_trip.save():
        manifest = frappe.get_doc("Manifest", args_dict.get("manifest_name"))
        manifest.vehicle_trip = vehicle_trip.name
        manifest.save()
        cargos = frappe.get_all("Cargo Detail", filters={"manifest_number":manifest.name}, fields="*")
        for cargo in cargos:
            cargo_registration = frappe.get_doc("Cargo Registration", cargo.parent )
            for row in cargo_registration.cargo_details:
                if row.manifest_number == manifest.name:
                    row.created_trip = vehicle_trip.name
                    cargo_registration.save()
                    break
        
        if args_dict.get("transporter_type") == "In House":
            funds_args = {
                "reference_doctype": "Trips",
                "reference_docname": vehicle_trip.name,
                "manifest": args_dict.get("manifest_name"),
                "truck": args_dict.get("truck"),
                "truck_driver": args_dict.get("driver"),
                "trip_route": args_dict.get("trip_route")
            }
            request_funds(**funds_args)
        
    return vehicle_trip.as_dict()

@frappe.whitelist()
def create_fund_jl(doc, row):
    doc = frappe.get_doc(json.loads(doc))
    row = frappe._dict(json.loads(row))
    if row.journal_entry:
        frappe.throw("Journal Entry Already Created")

    if row.request_status != "Approved":
        frappe.throw("Fund Request is not Approved")

    accounts = []
    
    company_currency = frappe.db.get_value(
        "Company",
        doc.company,
        "default_currency",
    )

    if company_currency != row.request_currency:
        multi_currency = 1
        exchange_rate = get_exchange_rate(row.request_currency, company_currency)
    else:
        # if row.request_currency != row.expense_account_currency or row.request_currency != row.payable_account_currency:
        #     multi_currency = 1
        #     exchange_rate = get_exchange_rate(row.request_currency, row.expense_account_currency)
        #     exchange_rate_to_calculate = get_exchange_rate(row.request_currency, company_currency)
        # else:
        multi_currency = 0
        exchange_rate = 1

    if row.request_currency != row.expense_account_currency:
        debit_amount = row.request_amount * exchange_rate
        debit_exchange_rate = exchange_rate
    else:
        debit_amount = row.request_amount
        debit_exchange_rate = 1

    if row.request_currency != row.payable_account_currency:
        credit_amt = row.request_amount * exchange_rate
        credit_exchange_rate = exchange_rate
    else:
        credit_amt = row.request_amount
        credit_exchange_rate = 1

    debit_row = dict(
        account=row.expense_account,
        exchange_rate=debit_exchange_rate,
        debit_in_account_currency=debit_amount,
        cost_center=row.cost_center,
    )
    accounts.append(debit_row)

    credit_row = dict(
        account=row.payable_account,
        exchange_rate=credit_exchange_rate,
        credit_in_account_currency=credit_amt,
        cost_center=row.cost_center,
    )
    accounts.append(credit_row)

    company = doc.company
    user_remark = "ref Document: {0}".format(doc.name)
    if row.requested_date:
        date = row.requested_date
    else:
        date = nowdate()
        
    jv_doc = frappe.get_doc(
        dict(
            doctype="Journal Entry",
            posting_date=date,
            accounts=accounts,
            company=company,
            multi_currency=multi_currency,
            user_remark=user_remark,
        )
    )
    jv_doc.flags.ignore_permissions = True
    frappe.flags.ignore_account_permission = True
    set_dimension(doc, jv_doc)
    for account_row in jv_doc.accounts:
        set_dimension(doc, jv_doc, tr_child=account_row)
    jv_doc.save()
    jv_url = frappe.utils.get_url_to_form(jv_doc.doctype, jv_doc.name)
    si_msgprint = "Journal Entry Created <a href='{0}'>{1}</a>".format(
        jv_url, jv_doc.name
    )
    frappe.msgprint(_(si_msgprint))
    frappe.set_value(row.doctype, row.name, "journal_entry", jv_doc.name)
    return jv_doc

@frappe.whitelist()
def make_vehicle_inspection(source_name, target_doc=None, ignore_permissions=False):

    docs = get_mapped_doc(
        "Trips",
        source_name,
        {
            "Trips": {
                "doctype": "Vehicle Inspection",
                "field_map": {
                    "driver_name": "driver_name",
                    "vehicle_plate_number": "vehicle_plate_number",
                    "name": "trip_reference",
                },
                "validation": {
                    "docstatus": ["=", 0],
                },
            }
        },
        target_doc,
        postprocess=None,
        ignore_permissions=ignore_permissions,
    )

    return docs


@frappe.whitelist(allow_guest=True)
def check_trip_status(**args):
    args = frappe._dict(args)
    frappe.msgprint("ok")

    existing_trip = frappe.db.get_value(
        "Trips", {"main_file_number": args.file_number}
    )
    if existing_trip:
        doc = frappe.get_doc("Trips", existing_trip)
        status = doc.status
        frappe.msgprint(status)
        if status != "Closed":
            frappe.msgprint(
                "Cannot Close the File because it's Trip is not closed,Please Create the Trip"
            )
        else:
            return status
    else:
        frappe.msgprint(
            "Cannot Close because Trip has not been created yet for the current file"
        )

@frappe.whitelist()
def create_stock_out_entry(doc, fuel_stock_out):
    doc = frappe.get_doc(json.loads(doc))
    if doc.stock_out_entry:
        return frappe.get_doc("Stock Entry", doc.stock_out_entry)
    fuel_item = frappe.get_value("Transport Settings", None, "fuel_item")
    if not fuel_item:
        frappe.throw(_("Please Set Fuel Item in Transport Settings"))
    warehouse = frappe.get_value("Truck", doc.truck_number, "trans_ms_fuel_warehouse")
    if not warehouse:
        frappe.throw(_("Please Set Fuel Warehouse in Vehicle"))
    item = {"item_code": fuel_item, "qty": float(fuel_stock_out)}
    stock_entry_doc = frappe.get_doc(
        dict(
            doctype="Stock Entry",
            from_bom=0,
            posting_date=nowdate(),
            posting_time=now(),
            items=[item],
            stock_entry_type="Material Issue",
            purpose="Material Issue",
            from_warehouse=warehouse,
            # to_warehouse=dispatch_bay_wh,
            company=doc.company,
            remarks="Transfer for {0} in truck {1}".format(
                doc.assigned_driver,
                doc.truck_number,
            ),
        )
    )
    set_dimension(doc, stock_entry_doc)
    set_dimension(doc, stock_entry_doc, tr_child=stock_entry_doc.items[0])
    stock_entry_doc.insert(ignore_permissions=True)
    doc.stock_out_entry = stock_entry_doc.name
    doc.save()
    return stock_entry_doc


@frappe.whitelist()
def create_purchase_order(request_doc, item):
    # frappe.throw(request_doc)
    item = frappe._dict(json.loads(item))
    request_doc = frappe._dict(json.loads(request_doc))
    set_warehouse = frappe.get_value(
        "Truck", request_doc.truck_number, "trans_ms_fuel_warehouse"
    )
    if not set_warehouse:
        frappe.throw(_("Fuel Stock Warehouse not set in Truck"))
    if item.purchase_order:
        frappe.throw(_("Purchase Order is already exists"))
    doc = frappe.new_doc("Purchase Order")
    doc.company = request_doc.company
    doc.department = item.supplier
    doc.supplier = item.supplier
    doc.currency = item.currency
    if item.transaction_date:
        doc.transaction_date = item.transaction_date
        doc.schedule_date = item.transaction_date
    else:
        doc.schedule_date = nowdate()
    # doc.docstatus = 1
    doc.set_warehouse = set_warehouse
    new_item = doc.append("items", {})
    new_item.item_code = item.item_code
    new_item.qty = item.quantity
    new_item.rate = item.cost_per_litre
    new_item.source_name = "fuel_requests"
    set_dimension(request_doc, doc)
    set_dimension(request_doc, doc, tr_child=new_item)
    doc.insert(ignore_permissions=True)
    frappe.msgprint(_("Purchase Order {0} is created").format(doc.name))
    frappe.set_value(item.doctype, item.name, "purchase_order", doc.name)
    return doc.name

@frappe.whitelist()
def create_breakdown(docname):
    trip = frappe.get_doc("Trips", docname)
    trip.trip_status = "Breakdown"
    trip.status = "Not Re-Assigned"
    trip.breakdown_date = now()
    trip.save()
    return "successful"

@frappe.whitelist()
def create_resumption_trip(docname):
    old_trip = frappe.get_doc("Trips", docname)

    new_trip = frappe.new_doc("Trips")

    new_trip.update(old_trip.as_dict())
    new_trip.location_update = []
    new_trip.trip_status = "Pending"
    new_trip.stock_out_entry = ""

    new_trip.insert()

    if new_trip.transporter_type == "In House":
        funds_args = {
            "reference_doctype": "Trips",
            "reference_docname": new_trip.name,
            "manifest": new_trip.manifest,
            "truck": new_trip.truck_number,
            "truck_driver": new_trip.assigned_driver,
            "trip_route": new_trip.route
            }
        request_funds(**funds_args)
    if new_trip.round_trip:
        round_trip = frappe.get_doc("Round Trip",new_trip.round_trip)
        round_trip.append("trip_details",{
            "trip_id":new_trip.name
            })
        round_trip.save()
        
    old_trip.resumption_trip = new_trip.name
    old_trip.status = "Re-Assigned"
    old_trip.save()
    return new_trip.as_dict()


