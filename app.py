import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

from ollama import chat

from database import (
    create_ticket,
    get_all_tickets,
    get_ticket,
    get_statistics
)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

# =========================================================
# TROUBLESHOOTING DATABASE
# =========================================================

TROUBLESHOOTING = {

    "touchpad": {

        "name": "Touchpad",

        "steps": [

            {
                "instruction":
                    "Check whether the touchpad has been disabled "
                    "using the laptop's touchpad enable/disable "
                    "function key.",

                "question":
                    "Did the touchpad start working?"
            },

            {
                "instruction":
                    "Open Windows Settings → Bluetooth & devices "
                    "→ Touchpad. Make sure Touchpad is switched ON.",

                "question":
                    "Did the touchpad start working?"
            },

            {
                "instruction":
                    "Open Device Manager and look under Human "
                    "Interface Devices for a touchpad-related device.",

                "question":
                    "Is the touchpad working after checking the device?"
            },

            {
                "instruction":
                    "Restart the laptop and test the touchpad again.",

                "question":
                    "Is the touchpad working after the restart?"
            }

        ],

        "escalation":
            "The approved touchpad troubleshooting steps "
            "have been completed."
    },


    "wifi": {

        "name": "Wi-Fi",

        "steps": [

            {
                "instruction":
                    "Open Windows Settings → Network & Internet "
                    "→ Wi-Fi. Make sure Wi-Fi is switched ON.",

                "question":
                    "Did Wi-Fi start working?"
            },

            {
                "instruction":
                    "Open Windows Settings → Network & Internet "
                    "and make sure Airplane mode is turned OFF.",

                "question":
                    "Did Wi-Fi start working?"
            },

            {
                "instruction":
                    "Turn Wi-Fi OFF, wait a few seconds, "
                    "and then turn Wi-Fi ON again.",

                "question":
                    "Did Wi-Fi start working?"
            },

            {
                "instruction":
                    "Restart the laptop and try connecting to Wi-Fi.",

                "question":
                    "Can the laptop connect to Wi-Fi now?"
            }

        ],

        "escalation":
            "The approved basic Wi-Fi troubleshooting steps "
            "have been completed."
    },


    "bluetooth": {

        "name": "Bluetooth",

        "steps": [

            {
                "instruction":
                    "Open Windows Settings → Bluetooth & devices. "
                    "Make sure Bluetooth is switched ON.",

                "question":
                    "Did Bluetooth start working?"
            },

            {
                "instruction":
                    "Turn Bluetooth OFF, wait a few seconds, "
                    "and then turn Bluetooth ON again.",

                "question":
                    "Did Bluetooth start working?"
            },

            {
                "instruction":
                    "Restart the laptop and try connecting the "
                    "Bluetooth device again.",

                "question":
                    "Is the Bluetooth device working now?"
            },

            {
                "instruction":
                    "Open Device Manager and check whether the "
                    "Bluetooth adapter is present and enabled.",

                "question":
                    "Is Bluetooth working after checking the adapter?"
            }

        ],

        "escalation":
            "The approved Bluetooth troubleshooting steps "
            "have been completed."
    },


    "charging": {

        "name": "Charging / Battery",

        "steps": [

            {
                "instruction":
                    "Check that the charger is properly connected "
                    "to the laptop and power socket.",

                "question":
                    "Is the laptop charging now?"
            },

            {
                "instruction":
                    "Try another working power socket.",

                "question":
                    "Is the laptop charging now?"
            },

            {
                "instruction":
                    "Check whether Windows shows a charging indicator.",

                "question":
                    "Does Windows show that the laptop is charging?"
            },

            {
                "instruction":
                    "Restart the laptop and check the charging status.",

                "question":
                    "Is the laptop charging after the restart?"
            }

        ],

        "escalation":
            "The approved charging troubleshooting steps "
            "have been completed."
    },


    "keyboard": {

        "name": "Keyboard",

        "steps": [

            {
                "instruction":
                    "Check whether one key is affected or multiple "
                    "keys are not working.",

                "question":
                    "Is the keyboard working normally?"
            },

            {
                "instruction":
                    "Restart the laptop and test the keyboard again.",

                "question":
                    "Is the keyboard working after restart?"
            },

            {
                "instruction":
                    "Connect an external keyboard if available.",

                "question":
                    "Does the external keyboard work?"
            },

            {
                "instruction":
                    "Open Device Manager → Keyboards and check "
                    "whether the keyboard device is present.",

                "question":
                    "Is the keyboard working after checking the device?"
            }

        ],

        "escalation":
            "The approved keyboard troubleshooting steps "
            "have been completed."
    },


    "overheating": {

        "name": "Overheating",

        "steps": [

            {
                "instruction":
                    "Place the laptop on a hard, flat surface and "
                    "make sure ventilation openings are not blocked.",

                "question":
                    "Has the overheating stopped?"
            },

            {
                "instruction":
                    "Close unnecessary applications and check Task Manager "
                    "for unusually high CPU usage.",

                "question":
                    "Has the overheating stopped?"
            },

            {
                "instruction":
                    "Check whether the laptop fan is running normally.",

                "question":
                    "Has the overheating stopped?"
            },

            {
                "instruction":
                    "Restart the laptop and check whether overheating continues.",

                "question":
                    "Has the overheating stopped after restart?"
            }

        ],

        "escalation":
            "The approved overheating troubleshooting steps "
            "have been completed."
    },


    "display": {

        "name": "Display / Screen",

        "steps": [

            {
                "instruction":
                    "Check whether the laptop powers on and whether "
                    "the display is completely black or simply dim.",

                "question":
                    "Is the display working?"
            },

            {
                "instruction":
                    "Check the screen brightness and increase it.",

                "question":
                    "Is the display visible now?"
            },

            {
                "instruction":
                    "Restart the laptop and check the display again.",

                "question":
                    "Is the display working after restart?"
            },

            {
                "instruction":
                    "If an external monitor is available, connect it "
                    "and check whether an image appears.",

                "question":
                    "Is the display working now?"
            }

        ],

        "escalation":
            "The approved display troubleshooting steps "
            "have been completed."
    },


    "bitlocker": {

        "name": "BitLocker",

        "steps": [

            {
                "instruction":
                    "Confirm whether Windows is showing a BitLocker "
                    "recovery screen and requesting a recovery key.",

                "question":
                    "Is the BitLocker recovery screen no longer appearing?"
            },

            {
                "instruction":
                    "Determine whether the laptop is company-managed "
                    "or personally owned.",

                "question":
                    "Has the BitLocker issue been resolved?"
            },

            {
                "instruction":
                    "Check whether you have access to the Microsoft "
                    "account or organization account associated with "
                    "the laptop.",

                "question":
                    "Has the BitLocker issue been resolved?"
            }

        ],

        "escalation":
            "BitLocker recovery requires appropriate account "
            "or administrative access.\n\n"
            "Do not delete partitions, format the drive, or "
            "reinstall Windows."
    }

}


# =========================================================
# AI CLASSIFICATION
# =========================================================

def detect_problem(message):

    prompt = f"""
You are a laptop IT support classification system.

Classify the user's problem into EXACTLY ONE category.

Allowed categories:

touchpad
wifi
bluetooth
charging
keyboard
overheating
display
bitlocker
unknown

User message:

{message}

Return ONLY one category.
"""

    try:

        response = chat(

            model="qwen2.5:1.5b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.message.content.strip().lower()

        allowed = [

            "touchpad",
            "wifi",
            "bluetooth",
            "charging",
            "keyboard",
            "overheating",
            "display",
            "bitlocker",
            "unknown"

        ]

        if result in allowed:

            return result

        return "unknown"

    except Exception as error:

        print(
            "AI classification error:",
            error
        )

        return "unknown"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================================
# CHAT
# =========================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat_endpoint():

    data = request.get_json()

    user_message = data.get(
        "message",
        ""
    ).strip()


    if not user_message:

        return jsonify({
            "response":
                "Please enter a message."
        })


    answer = user_message.lower().strip()


    current_problem = session.get(
        "problem"
    )

    current_step = session.get(
        "step",
        0
    )


    # =====================================================
    # EMPLOYEE
    # =====================================================

    if session.get(
        "waiting_for_employee"
    ):

        session["employee_name"] = user_message

        session.pop(
            "waiting_for_employee"
        )

        session["waiting_for_brand"] = True

        return jsonify({

            "response":
                "Thanks! 👍\n\n"
                "What is the laptop brand?\n\n"
                "Example: ASUS, HP, Dell, Lenovo"

        })


    # =====================================================
    # BRAND
    # =====================================================

    if session.get(
        "waiting_for_brand"
    ):

        session["laptop_brand"] = user_message

        session.pop(
            "waiting_for_brand"
        )

        session["waiting_for_model"] = True

        return jsonify({

            "response":
                "Thanks! 👍\n\n"
                "What is the laptop model?\n\n"
                "Example: ASUS VivoBook 15"

        })


    # =====================================================
    # MODEL
    # =====================================================

    if session.get(
        "waiting_for_model"
    ):

        session["laptop_model"] = user_message

        session.pop(
            "waiting_for_model"
        )

        session["waiting_for_asset"] = True

        return jsonify({

            "response":
                "Got it 👍\n\n"
                "What is the Asset ID?\n\n"
                "Example: LAP-1025\n\n"
                "If unavailable, type:\n"
                "Not available"

        })


    # =====================================================
    # ASSET
    # =====================================================

    if session.get(
        "waiting_for_asset"
    ):

        session["asset_id"] = user_message

        session.pop(
            "waiting_for_asset"
        )

        session["waiting_for_error"] = True

        return jsonify({

            "response":
                "Thanks! 👍\n\n"
                "Describe the error or problem "
                "you are seeing.\n\n"
                "If there is no error message, type:\n"
                "No error message"

        })


    # =====================================================
    # ERROR
    # =====================================================

    if session.get(
        "waiting_for_error"
    ):

        session["error_message"] = user_message

        session.pop(
            "waiting_for_error"
        )

        problem = session.get(
            "problem"
        )

        procedure = TROUBLESHOOTING.get(
            problem
        )


        if not procedure:

            session.clear()

            return jsonify({

                "response":
                    "I couldn't start troubleshooting."

            })


        session["step"] = 1

        session["completed_steps"] = []


        first_step = procedure[
            "steps"
        ][0]


        return jsonify({

            "response":
                f"Thanks! 👍\n\n"
                f"I identified a "
                f"{procedure['name']} issue.\n\n"
                f"🔧 Step 1\n\n"
                f"{first_step['instruction']}\n\n"
                f"{first_step['question']}\n\n"
                "Reply YES or NO."

        })


    # =====================================================
    # ANSWERS
    # =====================================================

    yes_answers = [

        "yes",
        "y",
        "yeah",
        "yep",
        "working",
        "it works",
        "working now",
        "fixed",
        "solved",
        "problem solved"

    ]


    no_answers = [

        "no",
        "n",
        "nope",
        "still not working",
        "not working",
        "not fixed",
        "didn't work",
        "didnt work",
        "doesn't work",
        "doesnt work",
        "same issue",
        "still the same",
        "not solved",
        "not fixed yet"

    ]


    # =====================================================
    # TROUBLESHOOTING
    # =====================================================

    if current_problem:

        procedure = TROUBLESHOOTING.get(
            current_problem
        )


        if not procedure:

            session.clear()

            return jsonify({

                "response":
                    "The troubleshooting session "
                    "could not be continued."

            })


        if current_step < 1:

            current_step = 1

            session["step"] = 1


        current_step_data = procedure[
            "steps"
        ][current_step - 1]


        # =================================================
        # YES
        # =================================================

        if answer in yes_answers:

            completed_steps = session.get(
                "completed_steps",
                []
            )


            completed_steps.append(

                f"Step {current_step}: "
                f"{current_step_data['instruction']} "
                f"→ Resolved"

            )


            session[
                "completed_steps"
            ] = completed_steps


            ticket_id = create_ticket(

                session.get(
                    "employee_name",
                    "Not provided"
                ),

                session.get(
                    "laptop_brand",
                    "Not provided"
                ),

                session.get(
                    "laptop_model",
                    "Not provided"
                ),

                session.get(
                    "asset_id",
                    "Not provided"
                ),

                procedure["name"],

                session.get(
                    "error_message",
                    "Not provided"
                ),

                "Resolved",

                completed_steps

            )


            employee = session.get(
                "employee_name",
                "Not provided"
            )

            brand = session.get(
                "laptop_brand",
                "Not provided"
            )

            model = session.get(
                "laptop_model",
                "Not provided"
            )

            asset_id = session.get(
                "asset_id",
                "Not provided"
            )

            error_message = session.get(
                "error_message",
                "Not provided"
            )


            session.clear()


            return jsonify({

                "response":
                    "Great! 🎉 The issue appears "
                    "to be resolved.\n\n"

                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "IT SUPPORT TICKET\n"
                    "━━━━━━━━━━━━━━━━━━━━\n\n"

                    f"🎫 Ticket ID: {ticket_id}\n"
                    f"👤 Employee: {employee}\n"
                    f"💻 Laptop: {brand} {model}\n"
                    f"🏷️ Asset ID: {asset_id}\n"
                    f"🔧 Issue: {procedure['name']}\n"
                    f"📝 Error: {error_message}\n"
                    "📌 Status: Resolved"

            })


        # =================================================
        # NO
        # =================================================

        elif answer in no_answers:

            completed_steps = session.get(
                "completed_steps",
                []
            )


            completed_steps.append(

                f"Step {current_step}: "
                f"{current_step_data['instruction']} "
                f"→ Did not resolve the issue"

            )


            session[
                "completed_steps"
            ] = completed_steps


            next_step = current_step + 1


        else:

            return jsonify({

                "response":
                    "Please reply YES or NO to "
                    "continue the troubleshooting process."

            })


        # =================================================
        # NEXT STEP
        # =================================================

        if next_step <= len(
            procedure["steps"]
        ):

            session["step"] = next_step

            step = procedure[
                "steps"
            ][next_step - 1]


            return jsonify({

                "response":
                    f"🔧 Step {next_step}\n\n"
                    f"{step['instruction']}\n\n"
                    f"{step['question']}\n\n"
                    "Reply YES or NO."

            })


        # =================================================
        # ESCALATION
        # =================================================

        completed_steps = session.get(
            "completed_steps",
            []
        )


        ticket_id = create_ticket(

            session.get(
                "employee_name",
                "Not provided"
            ),

            session.get(
                "laptop_brand",
                "Not provided"
            ),

            session.get(
                "laptop_model",
                "Not provided"
            ),

            session.get(
                "asset_id",
                "Not provided"
            ),

            procedure["name"],

            session.get(
                "error_message",
                "Not provided"
            ),

            "Escalation Required",

            completed_steps

        )


        employee = session.get(
            "employee_name",
            "Not provided"
        )

        brand = session.get(
            "laptop_brand",
            "Not provided"
        )

        model = session.get(
            "laptop_model",
            "Not provided"
        )

        asset_id = session.get(
            "asset_id",
            "Not provided"
        )

        error_message = session.get(
            "error_message",
            "Not provided"
        )


        escalation = procedure[
            "escalation"
        ]


        session.clear()


        return jsonify({

            "response":

                "🚨 TROUBLESHOOTING COMPLETED\n\n"

                f"{escalation}\n\n"

                "━━━━━━━━━━━━━━━━━━━━\n"
                "IT SUPPORT TICKET\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"

                f"🎫 Ticket ID: {ticket_id}\n"
                f"👤 Employee: {employee}\n"
                f"💻 Laptop: {brand} {model}\n"
                f"🏷️ Asset ID: {asset_id}\n"
                f"🔧 Issue: {procedure['name']}\n"
                f"📝 Error: {error_message}\n"
                "📌 Status: Escalation Required"

        })


    # =====================================================
    # NEW PROBLEM
    # =====================================================

    problem = detect_problem(
        user_message
    )


    if problem != "unknown":

        procedure = TROUBLESHOOTING.get(
            problem
        )


        if procedure:

            session["problem"] = problem

            session["step"] = 0

            session[
                "waiting_for_employee"
            ] = True


            return jsonify({

                "response":
                    f"I think this is a "
                    f"{procedure['name']} issue.\n\n"
                    "Before we start troubleshooting, "
                    "what is your name?"

            })


    # =====================================================
    # UNKNOWN
    # =====================================================

    return jsonify({

        "response":
            "I couldn't identify the exact laptop problem.\n\n"
            "Please describe what is happening in more detail.\n\n"
            "For example:\n"
            "• My cursor is not moving\n"
            "• My Wi-Fi cannot connect\n"
            "• My laptop is overheating\n"
            "• My screen is black\n"
            "• Windows is asking for a BitLocker recovery key"

    })


# =========================================================
# RESET
# =========================================================

@app.route(
    "/reset",
    methods=["POST"]
)
def reset_chat():

    session.clear()

    return jsonify({

        "response":
            "Conversation reset."

    })


# =========================================================
# GET ALL TICKETS
# =========================================================

@app.route("/tickets")
def tickets():

    return jsonify(
        get_all_tickets()
    )


# =========================================================
# GET SINGLE TICKET
# =========================================================

@app.route(
    "/tickets/<ticket_id>"
)
def single_ticket(ticket_id):

    ticket = get_ticket(
        ticket_id
    )


    if ticket is None:

        return jsonify({

            "error":
                "Ticket not found."

        }), 404


    return jsonify(ticket)


# =========================================================
# STATISTICS
# =========================================================

@app.route("/statistics")
def statistics():

    return jsonify(
        get_statistics()
    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )