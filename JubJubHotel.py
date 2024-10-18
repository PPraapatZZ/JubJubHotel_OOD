import math
import pandas as pd
import os

class Visitor:
    def __init__(self, travel_method: str, number: int):
        self.travel_method = travel_method
        self.number = number

    def __str__(self):
        return (f"{self.travel_method}-{self.number}")

class InfiniteHotel:
    global travel_values
    travel_values = {'walk': 1, 'car': 2, 'boat': 3, 'plane': 4}
    
    def __init__(self, room_count: int):
        self.total_rooms = room_count
        self.rooms = [None] * room_count
        self.guest_count = 0
        self.current_guests = []
        self.count_guest = {
            "walk": 0,
            "car": 0,
            "boat": 0,
            "plane": 0
        }
        

    def __str__(self) -> str:
        result = "#RoomID\tGuest\n"
        for i in range(self.total_rooms):
            result += f"#{i + 1}\t{self.rooms[i] if self.rooms[i] else 'None'}\n"
        result += "------------------------------"
        return result

    def save_to_csv(self, file_path: str) -> None:
        data = [{'RoomID': i + 1, 'Guest': f"{room.travel_method}_{room.number}" if room else 'None'} for i, room in enumerate(self.rooms)]
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    
    def add_count_guest(self, travel_method: str) -> None:
        self.guest_count += 1
        self.count_guest[travel_method] += 1
        
    def get_detail(self, room_id: int) -> str:
        return f"RoomID: {room_id} - Guest: {self.rooms[room_id - 1]}"
    
    def set_room_count(self, room_count: int) -> None:
        self.total_rooms = room_count
        self.rooms = [None] * room_count
    
    def available_room_count(self) -> int:
        return self.total_rooms - self.guest_count

    def available_room_list(self) -> list:
        return [index + 1 for index in range(self.total_rooms) if self.rooms[index] is None]

    def calculate_room_id(self, guest_number: int, travel_method: str) -> int:
        travel_value = travel_values[travel_method]
        return (2 ** guest_number * 3 ** travel_value) % self.total_rooms

    
    def binary_search_empty_room(self, low: int, high: int) -> int:
        high = min(high, self.total_rooms - 1) 
        print(f"Searching for empty room between {low} and {high}")
        if low > high:
            return self.binary_search_empty_room(0, high)
        
        mid = (low + high) // 2
        if self.rooms[mid] is None:
            if mid == 0 or self.rooms[mid - 1] is not None:  # previous room is not empty
                return mid
            return self.binary_search_empty_room(low, mid - 1)
        else:
            return self.binary_search_empty_room(mid + 1, high)
        
    def find_empty_room(self) -> int:
        """Public method to find the first empty room."""
        return self.binary_search_empty_room(0, self.total_rooms - 1)
    
    def expand_hotel(self, factor: int) -> None:
        self.total_rooms *= factor
        self.rooms = [None] * self.total_rooms
        self.guest_count = 0
        self.count_guest = {
            "walk": 0,
            "car": 0,
            "boat": 0,
            "plane": 0
        }
        print(f"Hotel size increased to {self.total_rooms} rooms.")

    
    def remove_guest_from_room(self, room_id: int) -> bool:
        if self.rooms[room_id] is not None:
            travel_method = self.rooms[room_id].travel_method  # Store before removing
            self.rooms[room_id] = None
            self.guest_count -= 1
            self.count_guest[travel_method] -= 1  # Use stored travel method
            return True
        return False

    def room_is_empty(self, room_id: int) -> bool:
        return self.rooms[room_id] is None
    
    def assign_guest_to_room(self, room_id: int, travel_method: str) -> None:
        if self.rooms[room_id] is None:
            self.rooms[room_id] = Visitor(travel_method, self.count_guest[travel_method] + 1)
            self.add_count_guest(travel_method)
            self.current_guests.append(self.rooms[room_id])

    def add_new_guest(self, guest_number: int, travel_method: str) -> None:
        room_id = self.calculate_room_id(guest_number, travel_method)
        
        if self.rooms[room_id] is not None:
            while self.rooms[room_id] is not None:
                room_id = self.find_empty_room()
        
            
        if room_id != -1:
            self.assign_guest_to_room(room_id, travel_method)
            
        else:
            print("No available room for this guest")
      
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
            
            for guest in previous_guests:
                if guest.travel_method == "walk":
                    guest_distribution["walk"] += 1
                elif guest.travel_method == "car":
                    guest_distribution["car"] += 1
                elif guest.travel_method == "boat":
                    guest_distribution["boat"] += 1
                elif guest.travel_method == "plane":
                    guest_distribution["plane"] += 1
            
            for travel_method, guest_count in guest_distribution.items():
                for guest in range(guest_count):
                    self.add_new_guest(guest, travel_method) 
                    
MENU = '''
------------------------------
1. Check in guest
2. Check available room
3. Check detail roomID
4. Check out guest 
5. Check in guest to roomID
6. Export CSV file
7. Exit
------------------------------
'''

def get_guest_input() -> list[int]:
    walk_guests = int(input("Number of guests from 'walk': "))
    car_guests = int(input("Number of guests from 'car': "))
    boat_guests = int(input("Number of guests from 'boat': "))
    plane_guests = int(input("Number of guests from 'plane': "))
    return [walk_guests, car_guests, boat_guests, plane_guests]

jub_jub_hotel = InfiniteHotel(room_count=0)
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
                
                if jub_jub_hotel.total_rooms == 0:
                    room_count = sum(guests)
                    jub_jub_hotel.set_room_count(room_count)
                    print(f"Hotel has been created with {room_count} rooms")
                    
                jub_jub_hotel.check_in_guests(guests)
                print(jub_jub_hotel)
                print(f"Total rooms: {jub_jub_hotel.total_rooms}")
                print(f"Available rooms: {jub_jub_hotel.available_room_count()} - {jub_jub_hotel.available_room_list()}")
                print("")
            case 2:  # Check available room
                print(f"Available rooms: {jub_jub_hotel.available_room_count()} - {jub_jub_hotel.available_room_list()}")
            case 3:  # Check detail roomID
                room_id = int(input("Enter roomID: "))
                if room_id < 1 or room_id > jub_jub_hotel.total_rooms:
                    print(f"Invalid roomID. Please enter a roomID between 1 and {jub_jub_hotel.total_rooms}")
                    continue
                print(jub_jub_hotel.get_detail(room_id))
                
            case 4:  # Check-out guest from roomID
                room_id = int(input("Enter roomID: "))
                if jub_jub_hotel.remove_guest_from_room(room_id - 1):
                    print(f"Guest has been checked out from roomID {room_id}")
                else:
                    print(f"RoomID {room_id} is already empty")
                    
            case 5:  # Check in guest to roomID
                room_id = int(input("Enter roomID: "))
                travel_method = input("Enter travel method(walk, car, boat, plane): ")
                if room_id < 1 or room_id > jub_jub_hotel.total_rooms:
                    print(f"Invalid roomID. Please enter a roomID between 1 and {jub_jub_hotel.total_rooms}")
                    continue
                
                if not jub_jub_hotel.room_is_empty(room_id - 1):
                    print(f"RoomID {room_id} is already occupied")
                    continue  
                
                jub_jub_hotel.assign_guest_to_room(room_id - 1, travel_method)
                print(f"Guest has been checked in to roomID {room_id}")
                print(jub_jub_hotel)
                
            case 6:  # Export CSV file
                current_directory = os.getcwd()
                file_path = os.path.join(current_directory, 'Jub_Jub_Hotel.csv')
                jub_jub_hotel.save_to_csv(file_path)
                print(f"Exported to {file_path}")
            case 7:  # Exit
                print("Goodbye Jub Jub ❤️")
                break
            case _:
                print("Please choose a service again")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")