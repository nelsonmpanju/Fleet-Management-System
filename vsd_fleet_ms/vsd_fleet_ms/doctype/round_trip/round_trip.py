# Copyright (c) 2023, VV SYSTEMS DEVELOPER LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RoundTrip(Document):
	def after_insert(self):
		"""Update trips after Round Trip is created"""
		self.update_trips()

	def on_update(self):
		"""Update trips when Round Trip is modified"""
		if not self.is_new():
			self.update_trips()
			self.refresh_trip_details()
			self.update_status()

	def update_trips(self):
		"""Link trips to this Round Trip"""
		for trips in self.trip_details:
			trip = frappe.get_doc("Trips", trips.trip_id)
			if trip.round_trip != self.name:
				trip.round_trip = self.name
				# Prevent recursive updates
				trip.flags.ignore_round_trip_update = True
				trip.save()

	def refresh_trip_details(self):
		"""Refresh trip details from linked trips (fetched fields)"""
		for trip_row in self.trip_details:
			trip = frappe.get_doc("Trips", trip_row.trip_id)
			trip_row.trip_driver = trip.driver_name
			trip_row.trip_start_date = trip.date
			trip_row.trip_end_date = trip.trip_completed_date

	def update_status(self):
		"""Auto-update Round Trip status based on trip completion"""
		if not self.trip_details:
			self.status = "In Progress"
			self.trip_completed = 0
			return

		# Get all trips and check their completion status
		all_completed = True
		any_in_progress = False

		for trip_row in self.trip_details:
			trip = frappe.get_doc("Trips", trip_row.trip_id)
			if not trip.trip_completed:
				all_completed = False
			if trip.trip_status == "Pending":
				any_in_progress = True

		# Update status based on trip states
		if all_completed:
			self.status = "Completed"
			self.trip_completed = 1
		elif any_in_progress:
			self.status = "In Progress"
			self.trip_completed = 0
		else:
			self.status = "In Progress"
			self.trip_completed = 0
