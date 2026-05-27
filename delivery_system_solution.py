import json
import math

# -------------------------
# Step 1: Read JSON File
# -------------------------
with open("base_case.json", "r") as file:
    data = json.load(file)

warehouses = data["warehouses"]
agents = data["agents"]
packages = data["packages"]

# -------------------------
# Step 2: Euclidean Distance Function
# -------------------------
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# -------------------------
# Step 3: Prepare Report Dictionary
# -------------------------
report = {}

for agent in agents:
    report[agent] = {
        "packages_delivered": 0,
        "total_distance": 0
    }

# -------------------------
# Step 4: Assign Packages to Nearest Agent
# -------------------------
for package in packages:

    warehouse_name = package["warehouse"]
    warehouse_location = warehouses[warehouse_name]
    destination = package["destination"]

    nearest_agent = None
    min_distance = float("inf")

    # Find nearest agent
    for agent, agent_location in agents.items():
        d = distance(agent_location, warehouse_location)

        if d < min_distance:
            min_distance = d
            nearest_agent = agent

    # Delivery distance:
    # Agent -> Warehouse + Warehouse -> Destination
    delivery_distance = (
        distance(agents[nearest_agent], warehouse_location) +
        distance(warehouse_location, destination)
    )

    # Update report
    report[nearest_agent]["packages_delivered"] += 1
    report[nearest_agent]["total_distance"] += round(delivery_distance, 2)

# -------------------------
# Step 5: Calculate Efficiency
# Efficiency = total_distance / packages_delivered
# Lower value = better
# -------------------------
best_agent = None
best_efficiency = float("inf")

for agent in report:

    packages_count = report[agent]["packages_delivered"]
    total_distance = report[agent]["total_distance"]

    if packages_count > 0:
        efficiency = round(total_distance / packages_count, 2)
    else:
        efficiency = 0

    report[agent]["efficiency"] = efficiency

    if packages_count > 0 and efficiency < best_efficiency:
        best_efficiency = efficiency
        best_agent = agent

report["best_agent"] = best_agent

# -------------------------
# Step 6: Save Report to JSON
# -------------------------
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

# -------------------------
# Step 7: Print Final Report
# -------------------------
print(json.dumps(report, indent=4))
