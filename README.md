# Simple Phonebook DApp

## About

The Enhanced Cartesi Phonebook DApp is a decentralized application (dApp) leveraging Cartesi Rollups technology to offer a comprehensive and secure contact management solution. This dApp allows users to manage contacts, organize them into groups, log calls, and even receive birthday reminders, all within the decentralized environment that ensures data security and ownership integrity.

## Getting Started

Below are the steps to set up this dApp locally.

### Prerequisites

Ensure the following are installed on your system:

- Python

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/suitret/simple-phonebook.git
   cd simple-phonebook
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the DApp**:
   ```bash
   python main.py
   ```

## Usage

This section covers examples of how to interact with the dApp's available features.

### Advanced Handlers

- **ADD_CONTACT**

  - **Description**: Add a new contact.
  - **Parameters**: {name, phone, email, address, birthday}

  **Sample Data(please hex encode these variables)**:

  ```json
  {
    "command": "ADD_CONTACT",
    "data": {
      "name": "John Doe",
      "phone": "123-456-7890",
      "email": "john@example.com",
      "address": "123 Main St, City, Country",
      "birthday": "1990-05-15"
    }
  }
  ```

- **CREATE_GROUP**

  - **Description**: Create a new contact group.
  - **Parameters**: {group_name, members}

  **Sample Data**:

  ```json
  {
    "command": "CREATE_GROUP",
    "data": {
      "group_name": "Family",
      "members": ["John Doe", "Jane Doe"]
    }
  }
  ```

- **LOG_CALL**

  - **Description**: Log a phone call.
  - **Parameters**: {caller, recipient, duration}

  **Sample Data**:

  ```json
  {
    "command": "LOG_CALL",
    "data": {
      "caller": "John Doe",
      "recipient": "Jane Doe",
      "duration": "00:05:30"
    }
  }
  ```

### Inspect Handlers

- **/contact/:name**
  - **Description**: Retrieve details for a specific contact.
- **/contacts**
  - **Description**: List all contacts in the phonebook.
- **/search/:query**
  - **Description**: Search for contacts by name, phone number, email, or address.
- **/group/:name**
  - **Description**: Retrieve details for a specific group.
- **/groups**
  - **Description**: List all groups.
- **/call_log**
  - **Description**: Retrieve the call log.
- **/birthday_reminders**
  - **Description**: Get birthday reminders for the current day.

## Logging

The dApp utilizes Python's `logging` module to provide debug information, aiding in tracking the application's internal state and troubleshooting.

## Contributing

We welcome contributions to enhance this dApp. Feel free to submit issues or pull requests.
