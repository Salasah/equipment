# Copyright (c) 2025, Equipment and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
from frappe.utils import date_diff

class EquipmentLeaseContract(Document):

    def on_submit(self):
        self.calculate_contract_days()
        subscription = self.create_subscription()
        self.link_subscription(subscription)
        self.update_asset_status()

    def calculate_contract_days(self):
        if self.start_date and self.end_date:
            days = date_diff(self.end_date, self.start_date) + 1
            self.contract_days = days

    def create_subscription(self):
        subscription = frappe.new_doc("Subscription")
        subscription.customer = self.lessee
        subscription.start_date = self.start_date
        subscription.end_date = self.end_date
        subscription.frequency = "Monthly"
        subscription.payment_terms_template = self.payment_terms
        subscription.related_lease_contract = self.name

        subscription.append("plans", {
            "item": "Equipment Rental Service",
            "rate": self.monthly_lease_amount,
            "qty": 1
        })

        subscription.insert(ignore_permissions=True)
        subscription.submit()
        return subscription

    def link_subscription(self, subscription):
        self.subscription_related = subscription.name
        self.active_is = 1
        self.save(ignore_permissions=True)

    def update_asset_status(self):
        if self.leased_equipment:
            asset = frappe.get_doc("Asset", self.leased_equipment)
            asset.status_asset = "Leased"
            asset.save(ignore_permissions=True)
            frappe.msgprint(f"Asset {asset.name} status changed to Leased", alert=True)
