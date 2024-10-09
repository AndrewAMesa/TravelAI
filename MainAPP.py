from LLaMaTravelAI import  *
from postgresConnection import *
import getpass
from PhiLocalAI import *

def run_trip_planner(description):
    print(f"Generating trip plan for: {description}\n")

    try:
        # Try to generate key points from API
        current_output = ""
        for output in generate_key_points(description):
            current_output += output
        print("Generated key points using API")
    except Exception as e:
        # If the API fails, fallback to the local model
        print(f"API failed with error: {e}, falling back to local model.")

        # Using the local model (replace this with your actual LLaMaTravelAI logic)
        current_output = get_trip_planning_suggestions(description)

        # Cannot generate output locally that breaks it up into days, to resource intensive and not possible
        return

    # Parse the output
    dataframe, rationale = parse_llm_output(current_output)
    print(rationale)

    # Geocode the addresses
    coordinates = geocode_addresses(dataframe["name"])
    dataframe["lat"] = [cords["lat"] if cords else None for cords in coordinates]
    dataframe["lon"] = [cords["lon"] if cords else None for cords in coordinates]

    num_days = extract_num_days_from_prompt(description)
    if len(dataframe) < num_days:
        print(f"Warning: Not enough locations to fill {num_days} days. You may need to adjust your trip description.")

    # Split the trip into days
    days = split_trip_into_days(dataframe, num_days)

    # Display the trip plan, split by days
    for day, activities in days.items():
        print(f"\n{day}:\n")
        for _, row in activities.iterrows():
            print(
                f"Location: {row['name']}\nDescription: {row['description']}\nCoordinates: ({row['lat']}, {row['lon']})\n")


# Example command-line interface loop
def main():
    print("Welcome to the AI Trip Planner!")
    choice = input("Would you like to login (1) or create a new user (2)?\n")
    if choice == "1":
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        loggedUser = checkLogin(username=username, password=password)
        if loggedUser is None:
            exit()
        else:
            print(f"Welcome, {loggedUser}")
    elif choice == "2":
        username = input("Please Enter Username: ")
        password = getpass.getpass("Please Choose a Password: ")
        redo_pass = getpass.getpass("Please Confirm Password: ")
        while redo_pass != password:
            password = getpass.getpass("Passwords Do Not Match, Please Try Again: ")  
            redo_pass = getpass.getpass("Please Confirm Password: ")
        loggedUser = createUser(username=username, password=password)
        if loggedUser is None:
            exit()
        else: 
            print(f"Welcome, {loggedUser}")
    else:
        print("Invalid choice. Please try again.")
        exit()


    while True:
        print("\nEnter a trip description (or type 'exit' to quit):")
        description = input("> ").strip()
        if description.lower() == "exit":
            print("\n Hope you have a good trip!")
            break
        run_trip_planner(description)


if __name__ == "__main__":
    main()
