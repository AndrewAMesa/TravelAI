from flask import Flask, request, jsonify
from Backend.Database.postgresConnection import *
import getpass
from Backend.ActionButtonAPIs.FlightPlanner import *
from Backend.ActionButtonAPIs.ItineraryPlanner import *
from Backend.ActionButtonAPIs.LodgingPlanner import *
import Backend.Models.LLaMaTravelAI as lAI
import Backend.Models.FalconAI as fAI
from Backend.Models.PhiLocalAI import *
from flask_cors import CORS
from Backend.Models.Parsing import *

app = Flask(__name__)
CORS(app)

# Trip planner using AI models or fallback logic
def run_trip_planner(logged_user, description, greeting):
    if greeting:
        # Use NLP to understand a general greeting and return response
        current_output = "".join(generateGreeting(description))
    else:
        try:
            # Use LLaMa for itinerary generation
            current_output = "".join(generate_key_itinerary_points(description))
            current_output = parse_plan_output(current_output, description)
        except Exception:
            try:
                # Use Falcon AI if LLaMa fails
                current_output = "".join(fAI.generate_key_itinerary_points(description))
            except Exception:
                # Local fallback if both API calls fail
                current_output = get_trip_planning_suggestions_local(description)

        if logged_user != "None":
            postHistory(user_login=logged_user, title_message=description, ai_response=current_output)

    return current_output

# Flight planner with similar fallback logic
def run_flight_planner(logged_user, description, greeting):
    if greeting:
        # Use NLP to understand a general greeting and return response
        current_output = "".join(generateGreeting(description))
    else:
        try:
            # Generate flight options with LLaMa AI
            current_output = "".join(generate_key_airplane_points(description))
            current_output = parse_flight_output(current_output, description)
        except Exception:
            try:
                # Use Falcon AI as fallback
                current_output = "".join(fAI.generate_key_airplane_points(description))
            except Exception:
                # Local fallback if both API calls fail
                current_output = get_flight_planning_suggestions_local(description)

        if logged_user != "None":
            postHistory(user_login=logged_user, title_message=description, ai_response=current_output)

    return current_output

# Lodging planner using the same pattern
def run_lodging_planner(logged_user, description, greeting):
    if greeting:
        # Use NLP to understand a general greeting and return response
        current_output = "".join(generateGreeting(description))
    else:
        try:
            # Use LLaMa AI for lodging suggestions
            current_output = "".join(generate_key_lodging_points(description))
            current_output = parse_lodging_output(current_output, description)
        except Exception:
            try:
                # Use Falcon AI fallback
                current_output = "".join(fAI.generate_key_lodging_points(description))
            except Exception:
                # Local fallback if both API calls fail
                current_output = get_lodging_planning_suggestions_local(description)

        if logged_user != "None":
            postHistory(user_login=logged_user, title_message=description, ai_response=current_output)

    return current_output

# Generic inquiry handling with AI or fallback logic
def run_generic_planner(logged_user, description, greeting):
    if greeting:
        # Use NLP to understand a general greeting and return response
        current_output = "".join(generateGreeting(description))
    else:
        try:
            # Use LLaMa AI for responses
            current_output = "".join(lAI.generate_generic_travel_prompt(description))
        except Exception:
            try:
                # Use Falcon AI as fallback
                current_output = "".join(fAI.generate_generic_travel_prompt(description))
            except Exception:
                # Local fallback if both API calls fail
                current_output = get_generic_planning_suggestions_local(description)

        if logged_user != "None":
            postHistory(user_login=logged_user, title_message=description, ai_response=current_output)

    print(current_output)
    return current_output

# Flask endpoint for trip planning
@app.route('/run_trip_planner', methods=['POST'])
def trip_planner():
    data = request.json
    description = data.get('description')
    logged_user = data.get('loggedUser', "None")

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    greeting_problem = TextParsingProblem(description.lower().split(), greeting_grammer, 'S')
    plan = run_generic_planner(logged_user, description, greeting_check(greeting_problem))
    return jsonify({'plan': plan}), 200

# Flask endpoint for itinerary planning
@app.route('/run_itinerary_planner', methods=['POST'])
def itinerary_planner():
    data = request.json
    description = data.get('description')
    logged_user = data.get('loggedUser', "None")

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    greeting_problem = TextParsingProblem(description.lower().split(), greeting_grammer, 'S')
    plan = run_trip_planner(logged_user, description, greeting_check(greeting_problem))
    return jsonify({'plan': plan}), 200

# Flask endpoint for flight planning
@app.route('/run_flight_planner', methods=['POST'])
def flight_planner():
    data = request.json
    description = data.get('description')
    logged_user = data.get('loggedUser', "None")

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    greeting_problem = TextParsingProblem(description.lower().split(), greeting_grammer, 'S')
    plan = run_flight_planner(logged_user, description, greeting_check(greeting_problem))
    return jsonify({'plan': plan}), 200

# Flask endpoint for lodging planning
@app.route('/run_lodging_planner', methods=['POST'])
def lodging_planner():
    data = request.json
    description = data.get('description')
    logged_user = data.get('loggedUser', "None")

    if not description:
        return jsonify({'error': 'Missing description'}), 400

    greeting_problem = TextParsingProblem(description.lower().split(), greeting_grammer, 'S')
    plan = run_lodging_planner(logged_user, description, greeting_check(greeting_problem))
    return jsonify({'plan': plan}), 200

# CLI interface or Flask server selection
def main():
    print("Welcome to the AI Trip Planner!")
    choice = input("Would you like to run the command line interface (1) or the Flask server (2)?\n> ")

    if choice == "1":
        # CLI-based interaction
        choice = input("Would you like to login (1), create a new user (2), or not log in (3)?\n> ")
        logged_user = "None"

        if choice == "1":
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            logged_user = checkLogin(username, password)
            if not logged_user:
                print("Invalid login. Exiting.")
                return
            print(f"Welcome, {logged_user}")
            if input("View chat history? (y/n): ").lower() == "y":
                history = fetchHistory(logged_user)
                if history:
                    for entry in history:
                        print(f"{entry['title']}\n{entry['response']}\n{entry['timestamp']}\n")
                else:
                    print("No chat history available.")
            print("Welcome")

        elif choice == "2":
            username = input("Enter Username: ")
            while True:
                password = getpass.getpass("Choose Password: ")
                if password == getpass.getpass("Confirm Password: "):
                    logged_user = createUser(username, password)
                    if logged_user:
                        print(f"Welcome, {logged_user}")
                        break
                print("Passwords do not match. Try again.")
            print("Welcome")

        elif choice == "3":
            print("Welcome")
            # Continuing as guest
        else:
            print("Invalid choice. Exiting.")
            return

        # Main interaction loop for planning options
        while True:
            plan_type = input("Would you like to create an itinerary (1), find flights (2), find lodging (3), or generic inquiry (4)?\n> ")
            description = input("What would you like help with?\n> ").strip()
            initial_state = description.lower().split()
            greeting_problem = TextParsingProblem(initial_state, greeting_grammer, 'S')

            # Call the appropriate planner based on user choice
            if plan_type == "1":
                run_trip_planner(logged_user, description, greeting_check(greeting_problem))
            elif plan_type == "2":
                run_flight_planner(logged_user, description, greeting_check(greeting_problem))
            elif plan_type == "3":
                run_lodging_planner(logged_user, description, greeting_check(greeting_problem))
            elif plan_type == "4":
                run_generic_planner(logged_user, description, greeting_check(greeting_problem))
            else:
                print("Invalid option. Try again.")

            # Exit prompt
            print("Do you want to exit (Y/N): ")
            if input("> ").lower() == "y":
                print("Hope you have a great trip!")
                break

    elif choice == "2":
        # Run Flask server
        app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()