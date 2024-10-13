# Jub Jub Hotel Management System

Welcome to the **Jub Jub Hotel Management System**! This program simulates a hotel with an infinite number of rooms, allowing guests to check in, check room availability, and export data to CSV.

## Features

- **Check-in Guests**: Guests can be checked into the hotel based on their travel method (walk, car, boat, plane).
- **Check Available Rooms**: Quickly see how many rooms are available and their IDs.
- **Room Details**: View the details of a specific room, including the guest assigned to it.
- **Remove Guests**: Guests can be removed from their assigned rooms.
- **Export to CSV**: Save the current state of the hotel to a CSV file for further analysis.
- **Dynamic Room Expansion**: The hotel automatically expands to accommodate more guests if needed.

## Requirements

- Python 3.x
- Pandas library (install using `pip install pandas`)

## How to Run

1. Clone this repository or download the code.
2. Ensure you have Python installed on your machine.
3. Install the required library by running:
   ```bash
   pip install pandas
4. Run the program using:
   ```bash
   python3 jub_jub_hotel.py
   ```
## Usage
Upon running the program, you will see a menu with the following options:

1. Check in guest: Input the number of guests based on their travel methods.
2. Check available room: Display the count and list of available rooms.
3. Check detail roomID: View the guest assigned to a specific room.
4. Delete guest from roomID: Remove a guest from a specified room.
5. Export CSV file: Save the current room assignments to a CSV file.
6. Exit: Close the program.

## Example Interaction

Welcome to Jub Jub Hotel
------------------------------
1. Check in guest
2. Check available room
3. Check detail roomID
4. Delete guest from roomID
5. Export CSV file
6. Exit
------------------------------
Choose a service (Press a number): 1
Number of guests from 'walk': 2
Number of guests from 'car': 1
Number of guests from 'boat': 0
Number of guests from 'plane': 1
#RoomID  Guest
#1       Visitor(walk)
#2       Visitor(walk)
#3       Visitor(car)
#4       Visitor(plane)
...

## Contributing
Feel free to fork the repository and submit pull requests. Any contributions or suggestions for improvements are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
The idea for this project is inspired by hotel management systems and is designed for educational purposes.

## Enjoy managing your virtual hotel! 🏨
