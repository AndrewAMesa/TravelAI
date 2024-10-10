from Parsing import TextParsingProblem, greeting_grammer, greeting_check, generateGreeting
from postgresConnection import *
import getpass
from FlightPlanner import *
from ItineraryPlanner import *
from LLaMaTravelAI import *
from PhiLocalAI import *

def run_trip_planner(loggedUser, description, greeting):
    if greeting:
        current_output = ""
        prompt = description
        for output in generateGreeting(prompt):
            current_output += output
        print(current_output)
        postHistory(user_login=loggedUser, title_message=description, ai_response=current_output)

    else:
        print(f"Generating trip plan for: {description}\n")

        try:
            # Try to generate key points from API
            current_output = ""
            for output in generate_key_itinerary_points(description):
                current_output += output

            plan = parse_plan_output(current_output, description)
        except Exception as e:
            # Cannot generate output locally that breaks it up into days, too resource intensive and not possible
            print(f"API failed with error: {e}, falling back to local model.")
            plan = get_trip_planning_suggestions_local(description)

        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=plan)

def run_flight_planner(loggedUser, description, greeting):
    current_output = ""
    if greeting:
        for output in generateGreeting(description):
            current_output += output
        print(current_output)
        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=current_output)

    else:
        print(f"Generating flight plan for: {description}\n")

        try:
            # Generate key points using API
            for output in generate_key_airplane_points(description):
                current_output += output

            plan = parse_flight_output(current_output, description)
        except Exception as e:
            # Cannot generate output locally that breaks it up into days, too resource intensive and not possible
            print(f"API failed with error: {e}, falling back to local model.")
            plan = get_trip_planning_suggestions_local(description)

        if loggedUser != "None":
            postHistory(user_login=loggedUser, title_message=description, ai_response=plan)


# Example command-line interface loop
def main():
    print("Welcome to the AI Trip Planner!")
    choice = input("Would you like to login (1), create a new user (2), or not login (3)?\n")
    if choice == "1":
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        loggedUser = checkLogin(username=username, password=password)
        if loggedUser is None:
            exit()
        else:
            print(f"Welcome, {loggedUser}")

        disp_history = input("Would you like to view your previous chat history?\nYes(y) or No(n)?\n")
        if disp_history == "y":
            history = fetchHistory(loggedUser)
            if history:
                for entry in history:
                    print(f"{entry['title']}")
                    print(f"{entry['response']}")
                    print(f"{entry['timestamp']}\n")
            else:
                print("No current chat history.")
        else:
            pass
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
    elif choice == "3":
        while True:
            print("\nEnter a trip description (or type 'exit' to quit):")
            description = input("> ").strip()
            initial_state = description.lower().split()
            print(initial_state)
            greeting_problem = TextParsingProblem(initial=initial_state, grammar=greeting_grammer, goal='S')
            print(description)
            if description.lower() == "exit":
                print("\n Hope you have a good trip!")
                break
            run_flight_planner(loggedUser="None", description=description, greeting=greeting_check(greeting_problem))
    else:
        print("Invalid choice. Please try again.")
        exit()


if __name__ == "__main__":
    main()
