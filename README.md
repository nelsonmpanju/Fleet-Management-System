---

# Fleet Management System

## Overview

The **Fleet Management System** is a robust application built on ERPNext, leveraging the Frappe Framework to deliver a seamless solution for managing transportation operations. Designed to enhance efficiency, this system offers comprehensive tools to oversee cargo, vehicles, drivers, routes, and trips—from foundational data setup to real-time operational tracking and reporting.

---

## Features

The Fleet Management System empowers users with a wide range of capabilities tailored to streamline transport operations. Key highlights include:

- **Master Data Management**: Organize cargo types, vehicles, drivers, and routes effortlessly.  
- **Operational Efficiency**: Track trips in real time, manage fuel, and schedule vehicle maintenance.  
- **Compliance & Reporting**: Generate manifests, ensure regulatory compliance, and access detailed reports.  
- **Intuitive Design**: Navigate and configure transport operations with ease.

### Detailed Feature Breakdown

#### Master Data Management
- **Cargo Types**: Categorize and manage various cargo types for operational clarity.  
- **Countries & Locations**: Define geographic data for precise route planning.  
- **Fixed Expenses**: Monitor transportation-related costs systematically.  
- **Fuel Requests**: Simplify fuel requisition and tracking processes.  
- **Unit of Measure (UOM)**: Standardize measurements for fuel and inventory.  
- **Truck, Trailer & Driver Management**: Maintain detailed records of vehicles and personnel.  
- **Trip Routes & Locations**: Configure and optimize transportation pathways.  
- **Transportation Orders**: Manage orders with structured workflows.  
- **Vehicle Inspections**: Utilize templates and logs to ensure vehicle readiness.

#### Settings Configuration
- **Accounting Dimensions**: Enable granular financial tracking.  
- **Cost Centers**: Allocate expenses by department or project.  
- **Currency & Tax Settings**: Adapt to regional financial requirements.  
- **Customer & Supplier Management**: Streamline stakeholder interactions.  
- **Warehouse & Inventory Management**: Oversee storage and stock efficiently.  
- **Document & Naming Conventions**: Implement consistent documentation standards.  
- **Cargo Allocation & Trip Planning**: Optimize cargo distribution and trip schedules.

#### Transport Operations
- **Real-Time Trip Tracking**: Monitor trip progress instantly.  
- **Fuel Management**: Track consumption and streamline fuel requests.  
- **Vehicle Maintenance**: Schedule upkeep and inspections proactively.  
- **Manifest Preparation**: Create compliant transport manifests with ease.  
- **Round Trip Planning**: Maximize efficiency with optimized routing.

#### User Training & Support
- **Cargo Registration**: Learn to input cargo data effectively.  
- **Manifest Preparation**: Master manifest creation and management.  
- **Trip Management**: Gain skills in planning and tracking trips.

---

## Installation

Follow these steps to integrate the Fleet Management System into your ERPNext environment:

1. **Access Your Frappe Bench Directory**:  
   ```bash
   cd /path/to/frappe-bench
   ```

2. **Retrieve the Application**:  
   ```bash
   bench get-app https://github.com/VVSD-LTD/vsd_fleet_ms.git
   ```

3. **Install on Your ERPNext Site**:  
   Replace `[your-site-name]` with your actual site name.  
   ```bash
   bench --site [your-site-name] install-app vsd_fleet_ms
   ```

4. **Apply Changes**:  
   ```bash
   bench --site [your-site-name] migrate
   ```

**Note**: Ensure your ERPNext instance is fully configured and operational before proceeding.

---

## Usage

Once installed, the Fleet Management System is accessible via the ERPNext interface. Get started with these steps:

1. **Initialize Master Data**: Set up cargo types, vehicles, drivers, and routes in the Transport module.  
2. **Customize Settings**: Adjust accounting, tax, and operational preferences to your needs.  
3. **Handle Operations**: Manage trips, track vehicles, oversee fuel, and schedule maintenance.  
4. **Analyze Performance**: Generate reports on trips, costs, and vehicle metrics for informed decision-making.

For a detailed guide, visit our [documentation](#) (replace with your actual documentation link).

---

## Contribution

We welcome contributions to enhance the Fleet Management System! Whether it’s fixing bugs or adding features, here’s how you can get involved:

### How to Contribute
1. **Fork the Repository**: Create your own copy on GitHub.  
2. **Create a Branch**:  
   ```bash
   git checkout -b feature-or-bugfix-name
   ```
3. **Commit Changes**:  
   ```bash
   git commit -m "Detailed description of your changes."
   ```
4. **Push to Your Fork**:  
   ```bash
   git push origin feature-or-bugfix-name
   ```
5. **Submit a Pull Request**: Open a pull request on GitHub for review.

**Guidelines**: Please adhere to our coding standards and test your changes thoroughly.

---

## License

This project is licensed under the **GNU General Public License (GPL)**. See the [LICENSE](LICENSE) file for details.

---

## Support

For assistance, reach out via [GitHub Issues](https://github.com/VVSD-LTD/vsd_fleet_ms/issues) or email us at [support@email.com](nelsonnorbert87@gmail.com).

---
