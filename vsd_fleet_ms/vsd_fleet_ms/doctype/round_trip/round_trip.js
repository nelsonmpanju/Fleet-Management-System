// Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Round Trip', {
	refresh: function(frm) {
		frm.set_query("trip_id", "trip_details", function () {
			return {
				filters: {
					truck_number: frm.doc.truck_on_trip,
					transporter_type: "In House",
					round_trip: ["in", ["", frm.doc.name]]
				}
			};
		});
	}
});
