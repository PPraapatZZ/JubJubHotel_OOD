import math
import pandas as pd
import os

class Visitor:
    def __init__(self, travel_method: str):
        self.travel_method = travel_method

    def __str__(self):
        return str(self.travel_method)

class InfiniteHotel:
    def __init__(self, room_count: int):
        self.total_rooms = room_count
        self.rooms = [None] * room_count
        self.guest_count = 0
        self.current_guests = []

    def __str__(self) -> str:
        result = "#RoomID\tGuest\n"
        for i in range(self.total_rooms):
            result += f"#{i + 1}\t{self.rooms[i] if self.rooms[i] else 'None'}\n"
        result += "------------------------------"
        return result

    def save_to_csv(self, file_path: str) -> None:
        data = [{'RoomID': i + 1, 'Guest': room.travel_method if room else 'None'} for i, room in enumerate(self.rooms)]
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    def available_room_count(self) -> int:
        return self.total_rooms - self.guest_count

    def available_room_list(self) -> list:
        return [index + 1 for index in range(self.total_rooms) if self.rooms[index] is None]

    def calculate_room_id(self, guest_number: int, travel_method: str) -> int:
        travel_values = {'walk': 1, 'car': 2, 'boat': 3, 'plane': 4}
        travel_value = travel_values.get(travel_method, 1)
        return (2 ** guest_number * 3 ** travel_value) % self.total_rooms

    def expand_hotel(self, factor: int) -> None:
        previous_rooms = self.rooms.copy()
        self.total_rooms *= factor
        self.rooms = [None] * self.total_rooms
        self.guest_count = 0
        for guest in previous_rooms:
            if guest:
                self.assign_guest_to_room(self.calculate_room_id(self.guest_count, guest.travel_method), guest.travel_method)
        print(f"Hotel size increased to {self.total_rooms} rooms.")

    def remove_guest_from_room(self, room_id: int) -> bool:
        if self.rooms[room_id] is not None:
            self.rooms[room_id] = None
            self.guest_count -= 1
            return True
        return False

    def assign_guest_to_room(self, room_id: int, travel_method: str) -> None:
        if self.rooms[room_id] is None:
            self.rooms[room_id] = Visitor(travel_method)
            self.guest_count += 1
            self.current_guests.append(self.rooms[room_id])

    def add_new_guest(self, guest_number: int, travel_method: str) -> None:
        room_id = self.calculate_room_id(guest_number, travel_method)
        while self.rooms[room_id] is not None:
            room_id = (room_id + 1) % self.total_rooms
        self.assign_guest_to_room(room_id, travel_method)

    def check_in_guests(self, guests: list[int]) -> None:
        guest_distribution = {"walk": guests[0], "car": guests[1], "boat": guests[2], "plane": guests[3]}
        total_guests = sum(guest_distribution.values())
        available_rooms = self.available_room_count()

        if total_guests <= available_rooms:
            available_rooms_list = self.available_room_list()
            available_room_index = 0
            for travel_method, guest_count in guest_distribution.items():
                for _ in range(guest_count):
                    self.assign_guest_to_room(available_rooms_list[available_room_index] - 1, travel_method)
                    available_room_index += 1
        else:
            current_room_count = self.total_rooms
            expansion_factor = math.ceil((total_guests + current_room_count) / current_room_count) + 1
            previous_guests = self.current_guests.copy()
            self.expand_hotel(expansion_factor)
            for i, previous_guest in enumerate(previous_guests):
                self.add_new_guest(i, previous_guest.travel_method)
            for travel_method, guest_count in guest_distribution.items():
                for guest in range(guest_count):
                    self.add_new_guest(guest, travel_method) 

MENU = '''
------------------------------
1. Check in guest
2. Check available room
3. Check detail roomID
4. Delete guest from roomID
5. Export CSV file
6. Exit
------------------------------
'''

def get_guest_input() -> list[int]:
    walk_guests = int(input("Number of guests from 'walk': "))
    car_guests = int(input("Number of guests from 'car': "))
    boat_guests = int(input("Number of guests from 'boat': "))
    plane_guests = int(input("Number of guests from 'plane': "))
    return [walk_guests, car_guests, boat_guests, plane_guests]

jub_jub_hotel = InfiniteHotel(room_count=1)
print("Welcome to Jub Jub Hotel")
while True:
    print(MENU)
    try:
        service = int(input("Choose a service (Press a number): "))

        match service:
            case 1:  # Check in guest
                guests = get_guest_input()
                if any(guest < 0 for guest in guests):
                    print("Guest number must be positive")
                    continue
                jub_jub_hotel.check_in_guests(guests)
                print(jub_jub_hotel)
                print(f"Total rooms: {jub_jub_hotel.total_rooms}")
                print(f"Available rooms: {jub_jub_hotel.available_room_count()} - {jub_jub_hotel.available_room_list()}")
                print("")
            case 2:  # Check available room
                print(f"Available rooms: {jub_jub_hotel.available_room_count()} - {jub_jub_hotel.available_room_list()}")
            case 3:  # Check detail roomID
                room_id = int(input("Enter roomID: "))
                print(f"RoomID: {room_id} - Guest: {jub_jub_hotel.rooms[room_id - 1]}")
            case 4:  # Delete guest from roomID
                room_id = int(input("Enter roomID: "))
                if jub_jub_hotel.remove_guest_from_room(room_id - 1):
                    print(f"Guest in roomID {room_id} has been deleted")
                else:
                    print(f"RoomID {room_id} is already empty")
            case 5:  # Export CSV file
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, 'Jub_Jub_Hotel.csv')
                jub_jub_hotel.save_to_csv(file_path)
                print(f"Exported to {file_path}")
            case 6:  # Exit
                print("Goodbye Jub Jub ❤️")
                break
            case _:
                print("Please choose a service again")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")