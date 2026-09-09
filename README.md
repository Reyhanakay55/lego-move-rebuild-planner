# LEGO Move & Rebuild Planner

A Python desktop application for organizing LEGO sets during moving, storage, and rebuilding.

I created this project around a real problem: LEGO models may need to be disassembled during a move, and it can become difficult to remember which set is stored in which box, whether pieces are missing, and how much of the model has been rebuilt.

The application stores this information in a local SQLite database and provides a graphical user interface for managing the collection.

## Features

- Add LEGO sets
- View saved LEGO sets
- Update existing LEGO sets
- Delete LEGO sets with confirmation
- Store data permanently using SQLite
- Organize sets by storage box
- Track missing pieces
- Track rebuilding progress from 0 to 100%
- Add notes for each LEGO set
- Select set status:
  - Complete
  - Disassembled
  - Damaged
  - Rebuilding
- Filter LEGO sets by status
- Validate user input
- Automatically create storage box records
- Load saved data again after restarting the application

## Technologies

- Python
- Tkinter
- SQLite
- SQL
- Object-Oriented Programming (OOP)
- Git
- GitHub

## Project Structure

### `main.py`

Contains the graphical user interface and application logic.

The `LegoPlannerApp` class manages:

- form fields
- buttons
- the LEGO set table
- status filtering
- user interaction
- input validation
- communication with the database layer

### `database.py`

Contains the `DatabaseManager` class.

It handles:

- creating database tables
- inserting records
- reading records
- updating records
- deleting records
- connecting LEGO sets to storage boxes
- retrieving individual LEGO set information

### `models.py`

Contains model classes representing application data such as:

- `LegoSet`
- `StorageBox`

These classes were created to practice separating real-world entities into an object-oriented structure.

## Database Design

The application uses two SQLite tables:

### `storage_boxes`

Stores information about storage boxes.

### `lego_sets`

Stores LEGO set information including:

- name
- set number
- status
- storage box
- missing pieces
- rebuild progress
- notes

The tables are connected using a foreign key.

One storage box can contain multiple LEGO sets, creating a one-to-many relationship.

## CRUD Operations

The project implements the four main CRUD operations:

- **Create** — add a new LEGO set
- **Read** — display saved LEGO sets
- **Update** — edit an existing LEGO set
- **Delete** — remove a LEGO set

## Input Validation

The application checks important user input before saving data.

For example:

- LEGO set name cannot be empty
- storage box number cannot be empty
- rebuild progress must be a number
- rebuild progress must stay between 0 and 100

Invalid input displays an error message instead of crashing the application.

## How to Run

1. Make sure Python 3 is installed.

2. Clone or download the repository.

3. Open the project folder in a terminal.

4. Run:

```bash
python3 main.py