import csv
import os
import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "data")

NUM_USERS = 10_000
NUM_VEHICLES = 3_000
NUM_RIDES = 20_000
NUM_PAYMENTS = 16_000
NUM_RATINGS = 12_000

# Ensure enough completed rides can support payments
# and ratings.
COMPLETED_RIDE_RATIO = 0.90

os.makedirs(CSV_DIR, exist_ok=True)

# --------------------------------------------------
# Helpers
# --------------------------------------------------


def write_csv(filename, rows, fieldnames):
    filepath = os.path.join(CSV_DIR, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {filename}: {len(rows):,} rows")


def random_datetime(start_date, end_date):
    delta = end_date - start_date
    seconds = random.randint(0, int(delta.total_seconds()))
    return start_date + timedelta(seconds=seconds)


# --------------------------------------------------
# 1. Users
# --------------------------------------------------

users = []

# First 3,000 users are drivers.
# Remaining 7,000 users are riders.
for user_id in range(1, NUM_USERS + 1):
    user_type = "driver" if user_id <= NUM_VEHICLES else "rider"

    users.append(
        {
            "user_id": user_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": f"user{user_id}@example.com",
            "phone": f"{random.randint(6000000000, 9999999999)}",
            "city": random.choice(
                [
                    "Bhubaneswar",
                    "Cuttack",
                    "Puri",
                    "Rourkela",
                    "Sambalpur",
                    "Berhampur",
                ]
            ),
            "province": "Odisha",
            "user_type": user_type,
            "signup_date": fake.date_between(
                start_date="-3y",
                end_date="today",
            ).isoformat(),
            "is_active": random.choice([True, True, True, False]),
        }
    )

write_csv(
    "users.csv",
    users,
    [
        "user_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "province",
        "user_type",
        "signup_date",
        "is_active",
    ],
)

driver_ids = list(range(1, NUM_VEHICLES + 1))
rider_ids = list(range(NUM_VEHICLES + 1, NUM_USERS + 1))

# --------------------------------------------------
# 2. Vehicles
# --------------------------------------------------

vehicles = []

makes_models = {
    "Maruti Suzuki": ["Swift", "Dzire", "Baleno"],
    "Hyundai": ["i10", "i20", "Aura"],
    "Tata": ["Tiago", "Tigor", "Altroz"],
    "Honda": ["Amaze", "City"],
    "Toyota": ["Glanza", "Etios"],
}

for vehicle_id in range(1, NUM_VEHICLES + 1):
    make = random.choice(list(makes_models.keys()))

    vehicles.append(
        {
            "vehicle_id": vehicle_id,
            "driver_id": driver_ids[vehicle_id - 1],
            "make": make,
            "model": random.choice(makes_models[make]),
            "year": random.randint(2016, 2026),
            "license_plate": f"OD{random.randint(1, 35):02d}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000, 9999)}",
            "color": random.choice(
                [
                    "White",
                    "Black",
                    "Silver",
                    "Grey",
                    "Blue",
                    "Red",
                ]
            ),
            "is_active": random.choice([True, True, True, False]),
        }
    )

write_csv(
    "vehicles.csv",
    vehicles,
    [
        "vehicle_id",
        "driver_id",
        "make",
        "model",
        "year",
        "license_plate",
        "color",
        "is_active",
    ],
)

# --------------------------------------------------
# 3. Rides
# --------------------------------------------------

rides = []

start_date = datetime.now() - timedelta(days=365)
end_date = datetime.now()

ride_statuses = ["completed"] * 90 + ["cancelled"] * 7 + ["requested"] * 3

for ride_id in range(1, NUM_RIDES + 1):
    rider_id = random.choice(rider_ids)
    driver_id = random.choice(driver_ids)

    requested_at = random_datetime(start_date, end_date)
    status = random.choice(ride_statuses)

    pickup_time = None
    dropoff_time = None

    if status == "completed":
        pickup_time = requested_at + timedelta(minutes=random.randint(2, 15))
        dropoff_time = pickup_time + timedelta(minutes=random.randint(10, 90))

    elif status == "cancelled":
        pickup_time = None
        dropoff_time = None

    distance_km = round(random.uniform(1.0, 40.0), 2)
    surge_multiplier = round(random.uniform(1.0, 2.0), 2)
    base_fare = 40 + distance_km * random.uniform(10, 20)
    fare = round(base_fare * surge_multiplier, 2)

    rides.append(
        {
            "ride_id": ride_id,
            "rider_id": rider_id,
            "driver_id": driver_id,
            "requested_at": requested_at.isoformat(sep=" "),
            "pickup_time": (pickup_time.isoformat(sep=" ") if pickup_time else ""),
            "dropoff_time": (dropoff_time.isoformat(sep=" ") if dropoff_time else ""),
            "pickup_latitude": round(random.uniform(20.20, 20.40), 6),
            "pickup_longitude": round(random.uniform(85.75, 85.90), 6),
            "dropoff_latitude": round(random.uniform(20.20, 20.40), 6),
            "dropoff_longitude": round(random.uniform(85.75, 85.90), 6),
            "distance_km": distance_km,
            "fare": fare,
            "surge_multiplier": surge_multiplier,
            "status": status,
            "cancellation_reason": (
                random.choice(
                    [
                        "Driver unavailable",
                        "Rider cancelled",
                        "Long waiting time",
                        "Changed plans",
                    ]
                )
                if status == "cancelled"
                else ""
            ),
        }
    )

write_csv(
    "rides.csv",
    rides,
    [
        "ride_id",
        "rider_id",
        "driver_id",
        "requested_at",
        "pickup_time",
        "dropoff_time",
        "pickup_latitude",
        "pickup_longitude",
        "dropoff_latitude",
        "dropoff_longitude",
        "distance_km",
        "fare",
        "surge_multiplier",
        "status",
        "cancellation_reason",
    ],
)

# Only completed rides can receive payments and ratings.
completed_rides = [ride for ride in rides if ride["status"] == "completed"]

if len(completed_rides) < max(NUM_PAYMENTS, NUM_RATINGS):
    raise ValueError(
        "Not enough completed rides to generate the requested " "payments and ratings."
    )

# --------------------------------------------------
# 4. Payments
# --------------------------------------------------

# Use distinct rides so each payment belongs to a unique ride.
payment_rides = random.sample(completed_rides, NUM_PAYMENTS)
payments = []

for payment_id, ride in enumerate(payment_rides, start=1):
    payment_time = datetime.fromisoformat(ride["dropoff_time"])

    payments.append(
        {
            "payment_id": payment_id,
            "ride_id": ride["ride_id"],
            "user_id": ride["rider_id"],
            "amount": ride["fare"],
            "payment_method": random.choice(
                [
                    "UPI",
                    "Credit Card",
                    "Debit Card",
                    "Cash",
                    "Wallet",
                ]
            ),
            "payment_status": random.choices(
                ["successful", "failed", "refunded"],
                weights=[94, 4, 2],
                k=1,
            )[0],
            "transaction_id": f"TXN{payment_id:010d}",
            "payment_time": (
                payment_time + timedelta(minutes=random.randint(0, 30))
            ).isoformat(sep=" "),
        }
    )

write_csv(
    "payments.csv",
    payments,
    [
        "payment_id",
        "ride_id",
        "user_id",
        "amount",
        "payment_method",
        "payment_status",
        "transaction_id",
        "payment_time",
    ],
)

# --------------------------------------------------
# 5. Ratings
# --------------------------------------------------

# Use distinct completed rides for ratings.
rating_rides = random.sample(completed_rides, NUM_RATINGS)
ratings = []

comments_by_rating = {
    1: ["Very poor experience", "Long delay", "Unsafe driving"],
    2: ["Below average service", "Could be improved"],
    3: ["Average ride", "Service was acceptable"],
    4: ["Good experience", "Clean vehicle", "Polite driver"],
    5: ["Excellent service", "Great driver", "Very comfortable"],
}

for rating_id, ride in enumerate(rating_rides, start=1):
    rated_at = datetime.fromisoformat(ride["dropoff_time"])

    rating_value = random.choices(
        [1, 2, 3, 4, 5],
        weights=[3, 5, 15, 32, 45],
        k=1,
    )[0]

    ratings.append(
        {
            "rating_id": rating_id,
            "ride_id": ride["ride_id"],
            "rider_id": ride["rider_id"],
            "driver_id": ride["driver_id"],
            "rating": rating_value,
            "comment": random.choice(comments_by_rating[rating_value]),
            "rated_at": (rated_at + timedelta(hours=random.randint(0, 48))).isoformat(
                sep=" "
            ),
        }
    )

write_csv(
    "ratings.csv",
    ratings,
    [
        "rating_id",
        "ride_id",
        "rider_id",
        "driver_id",
        "rating",
        "comment",
        "rated_at",
    ],
)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\nData generation completed.")
print(f"Users:    {len(users):,}")
print(f"Vehicles: {len(vehicles):,}")
print(f"Rides:    {len(rides):,}")
print(f"Payments: {len(payments):,}")
print(f"Ratings:  {len(ratings):,}")
print(f"\nCSV directory: {CSV_DIR}")
