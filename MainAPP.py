from LLaMaTravelAI import  *
from postgresConnection import *

def run_trip_planner(description):
    print(f"Generating trip plan for: {description}\n")

    # Generate key points from LLM
    current_output = ""
    for output in generate_key_points(description):
        current_output += output

    current_output = current_output.replace("</s>", "")

    # Parse the output
    dataframe, rationale = parse_llm_output(current_output)
    print(rationale)

    # Geocode the addresses
    coordinates = geocode_addresses(dataframe["name"])
    dataframe["lat"] = [cords["lat"] if cords else None for cords in coordinates]
    dataframe["lon"] = [cords["lon"] if cords else None for cords in coordinates]

    # Split the trip into days
    days = split_trip_into_days(dataframe, num_days=extract_num_days_from_prompt(description))

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
        password = input("Password: ")
        loggedUser = checkLogin(username=username, password=password)
        if loggedUser is None:
            exit()
        else:
            print(f"Welcome, {loggedUser}")


    while True:
        print("\nEnter a trip description (or type 'exit' to quit):")
        description = input("> ").strip()
        if description.lower() == "exit":
            break
        run_trip_planner(description)


if __name__ == "__main__":
    main()
