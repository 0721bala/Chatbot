import sqlite3
from datetime import datetime


DATABASE = "support_tickets.db"


# =========================================================
# CONNECT TO DATABASE
# =========================================================

def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# CREATE DATABASE
# =========================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket_id TEXT UNIQUE NOT NULL,

            date TEXT NOT NULL,

            employee_name TEXT,

            laptop_brand TEXT,

            laptop_model TEXT,

            asset_id TEXT,

            problem TEXT,

            error_message TEXT,

            status TEXT,

            troubleshooting_steps TEXT

        )
    """)


    connection.commit()

    connection.close()


# =========================================================
# CREATE TICKET
# =========================================================

def create_ticket(
    employee_name,
    laptop_brand,
    laptop_model,
    asset_id,
    problem,
    error_message,
    status,
    troubleshooting_steps
):

    connection = get_connection()

    cursor = connection.cursor()


    # Get next ticket number

    cursor.execute(
        "SELECT COUNT(*) FROM tickets"
    )

    count = cursor.fetchone()[0]

    ticket_number = count + 1

    ticket_id = f"TICKET-{ticket_number:04d}"


    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # Convert troubleshooting list to text

    steps_text = "\n".join(
        troubleshooting_steps
    )


    cursor.execute("""
        INSERT INTO tickets (

            ticket_id,
            date,
            employee_name,
            laptop_brand,
            laptop_model,
            asset_id,
            problem,
            error_message,
            status,
            troubleshooting_steps

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        ticket_id,
        date,
        employee_name,
        laptop_brand,
        laptop_model,
        asset_id,
        problem,
        error_message,
        status,
        steps_text

    ))


    connection.commit()

    connection.close()


    return ticket_id


# =========================================================
# GET ALL TICKETS
# =========================================================

def get_all_tickets():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM tickets
        ORDER BY id DESC
    """)


    rows = cursor.fetchall()

    connection.close()


    tickets = []


    for row in rows:

        ticket = dict(row)


        steps_text = ticket.get(
            "troubleshooting_steps",
            ""
        )


        if steps_text:

            ticket["troubleshooting_steps"] = (
                steps_text.split("\n")
            )

        else:

            ticket["troubleshooting_steps"] = []


        tickets.append(ticket)


    return tickets


# =========================================================
# GET SINGLE TICKET
# =========================================================

def get_ticket(ticket_id):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))


    row = cursor.fetchone()

    connection.close()


    if row is None:

        return None


    ticket = dict(row)


    steps_text = ticket.get(
        "troubleshooting_steps",
        ""
    )


    if steps_text:

        ticket["troubleshooting_steps"] = (
            steps_text.split("\n")
        )

    else:

        ticket["troubleshooting_steps"] = []


    return ticket


# =========================================================
# DATABASE STATISTICS
# =========================================================

def get_statistics():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM tickets"
    )

    total = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE status = 'Resolved'
    """)

    resolved = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COUNT(*)
        FROM tickets
        WHERE status = 'Escalation Required'
    """)

    escalated = cursor.fetchone()[0]


    connection.close()


    return {

        "total": total,

        "resolved": resolved,

        "escalated": escalated

    }


# =========================================================
# INITIALIZE DATABASE
# =========================================================

initialize_database()