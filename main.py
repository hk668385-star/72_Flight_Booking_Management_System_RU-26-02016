
import csv


# Flight Class
class Flight:

    def __init__(self, flight_no, origin, destination, seats, fare):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.seats = seats
        self.fare = fare

    # Book seats
    def book_seats(self, number):
        if number < 1:
            return False

        if self.seats == 0:
            return False

        if number > self.seats:
            return False

        self.seats -= number
        return True

    # Cancel seats
    def cancel_seats(self, number):
        self.seats += number


# Load flights from CSV
def load_flights(filename):
    flights = []

    try:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                flight = Flight(
                    row["FlightNo"].strip(),
                    row["Origin"].strip(),
                    row["Destination"].strip(),
                    int(row["Seats"]),
                    int(row["Fare"])
                )

                flights.append(flight)

    except FileNotFoundError:
        print("Error: flights.csv file not found.")

    except (ValueError, KeyError):
        print("Error: Invalid flight data in CSV file.")

    return flights


# Search flights
def search_flights(flights):
    origin = input("Origin: ").strip()
    destination = input("Destination: ").strip()

    found = False

    for flight in flights:
        if (flight.origin.lower() == origin.lower()
                and flight.destination.lower() == destination.lower()):

            print(
                f"{flight.flight_no} | "
                f"{flight.origin} -> {flight.destination} | "
                f"Seats: {flight.seats} | "
                f"Fare: Rs. {flight.fare} per seat"
            )

            found = True

    if not found:
        print("No flights found.")


# Book flight
def book_flight(flights, bookings, booking_counter):

    flight_no = input("Flight: ").strip()
    passenger = input("Passenger: ").strip()

    try:
        number = int(input("Seats: "))
    except ValueError:
        print("Invalid number of seats.")
        return booking_counter

    if number < 1:
        print("Number of seats must be at least 1.")
        return booking_counter

    flight = None

    for item in flights:
        if item.flight_no.lower() == flight_no.lower():
            flight = item
            break

    if flight is None:
        print("Flight not found.")
        return booking_counter

    if flight.seats == 0:
        print(f"Flight {flight.flight_no} is full.")
        return booking_counter

    if number > flight.seats:
        print(
            f"Only {flight.seats} seat(s) available "
            f"on {flight.flight_no}."
        )
        return booking_counter

    # Book the seats
    flight.book_seats(number)

    total = number * flight.fare
    booking_id = "BK" + str(booking_counter)

    # Store booking information
    booking = {
        "id": booking_id,
        "passenger": passenger,
        "flight": flight,
        "seats": number,
        "total": total,
        "cancelled": False
    }

    bookings.append(booking)

    print(
        f"Booking confirmed. ID: {booking_id} | "
        f"{passenger} | {flight.flight_no} | "
        f"{number} seat(s) | Total: Rs. {total} | "
        f"Seats left: {flight.seats}"
    )

    return booking_counter + 1


# Cancel booking
def cancel_booking(bookings):

    booking_id = input("ID: ").strip()

    for booking in bookings:

        if booking["id"].lower() == booking_id.lower():

            if booking["cancelled"]:
                print("Booking already cancelled.")
                return

            booking["flight"].cancel_seats(booking["seats"])
            booking["cancelled"] = True

            flight = booking["flight"]

            print(
                f"Booking {booking_id} cancelled. "
                f"Seats left on {flight.flight_no}: {flight.seats}"
            )

            return

    print("Booking ID not found.")


# Main Program
def main():

    flights = load_flights("flights.csv")
    bookings = []

    booking_counter = 1

    while True:

        menu = input("\nMenu: ").strip().lower()

        if menu in ("search flights", "search"):
            search_flights(flights)

        elif menu == "book":
            booking_counter = book_flight(
                flights, bookings, booking_counter
            )

        elif menu in ("cancel booking", "cancel"):
            cancel_booking(bookings)

        elif menu in ("exit", "quit"):
            print("Thank you for using Flight Booking System.")
            break

        else:
            print("Invalid menu option.")


# Program execution
if __name__ == "__main__":
    main()
    