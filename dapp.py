import json
import logging
from datetime import datetime
from typing import Dict, List

from cartesi import DApp, Rollup, RollupData, URLRouter
from cartesi.models import _str2hex

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

dapp = DApp()
url_router = URLRouter()

phonebook: Dict[str, Dict[str, str]] = {}
groups: Dict[str, List[str]] = {}
call_log: List[Dict[str, str]] = []


@dapp.advance()
def handle_advance(rollup: Rollup, data: RollupData) -> bool:
    raw_payload = data.str_payload()
    payload = json.loads(raw_payload)
    command = payload.get("command")

    if command == "ADD_CONTACT":
        name = payload["data"]["name"]
        phone = payload["data"]["phone"]
        email = payload["data"].get("email", "")
        address = payload["data"].get("address", "")
        birthday = payload["data"].get("birthday", "")

        phonebook[name] = {
            "phone": phone,
            "email": email,
            "address": address,
            "birthday": birthday,
            "created_at": datetime.now().isoformat(),
        }
        rollup.notice(f"Added contact: {name}")

    elif command == "UPDATE_CONTACT":
        name = payload["data"]["name"]
        if name in phonebook:
            for key, value in payload["data"].items():
                if key != "name" and value:
                    phonebook[name][key] = value
            phonebook[name]["updated_at"] = datetime.now().isoformat()
            rollup.notice(f"Updated contact: {name}")
        else:
            rollup.notice(f"Contact not found: {name}")

    elif command == "DELETE_CONTACT":
        name = payload["data"]["name"]
        if name in phonebook:
            del phonebook[name]
            # Remove from groups
            for group in groups.values():
                if name in group:
                    group.remove(name)
            rollup.notice(f"Deleted contact: {name}")
        else:
            rollup.notice(f"Contact not found: {name}")

    elif command == "GET_CONTACT":
        name = payload["data"]["name"]
        if name in phonebook:
            contact = phonebook[name]
            rollup.notice(f"Contact {name}: {json.dumps(contact)}")
        else:
            rollup.notice(f"Contact not found: {name}")

    elif command == "LIST_CONTACTS":
        contacts_list = [
            {"name": name, **details} for name, details in phonebook.items()
        ]
        rollup.notice(f"All contacts: {json.dumps(contacts_list)}")

    elif command == "CREATE_GROUP":
        group_name = payload["data"]["group_name"]
        members = payload["data"]["members"]
        groups[group_name] = [member for member in members if member in phonebook]
        rollup.notice(f"Created group: {group_name} with members: {groups[group_name]}")

    elif command == "ADD_TO_GROUP":
        group_name = payload["data"]["group_name"]
        member = payload["data"]["member"]
        if group_name in groups and member in phonebook:
            if member not in groups[group_name]:
                groups[group_name].append(member)
                rollup.notice(f"Added {member} to group: {group_name}")
            else:
                rollup.notice(f"{member} is already in group: {group_name}")
        else:
            rollup.notice("Invalid group name or member")

    elif command == "REMOVE_FROM_GROUP":
        group_name = payload["data"]["group_name"]
        member = payload["data"]["member"]
        if group_name in groups and member in groups[group_name]:
            groups[group_name].remove(member)
            rollup.notice(f"Removed {member} from group: {group_name}")
        else:
            rollup.notice("Invalid group name or member not in group")

    elif command == "LOG_CALL":
        caller = payload["data"]["caller"]
        recipient = payload["data"]["recipient"]
        duration = payload["data"]["duration"]
        timestamp = datetime.now().isoformat()
        call_log.append(
            {
                "caller": caller,
                "recipient": recipient,
                "duration": duration,
                "timestamp": timestamp,
            }
        )
        rollup.notice(f"Logged call: {caller} to {recipient}, duration: {duration}")

    else:
        rollup.notice("Invalid command")

    return True


@url_router.inspect("/contact/:name")
def get_contact(name: str):
    if name in phonebook:
        return {"name": name, **phonebook[name]}
    return {"error": "Contact not found"}


@url_router.inspect("/contacts")
def list_contacts():
    return [{"name": name, **details} for name, details in phonebook.items()]


@url_router.inspect("/search/:query")
def search_contacts(query: str):
    query = query.lower()
    results = [
        {"name": name, **details}
        for name, details in phonebook.items()
        if query in name.lower()
        or query in details["phone"]
        or query in details["email"].lower()
        or query in details["address"].lower()
    ]
    return results


@url_router.inspect("/group/:name")
def get_group(name: str):
    if name in groups:
        return {"group_name": name, "members": groups[name]}
    return {"error": "Group not found"}


@url_router.inspect("/groups")
def list_groups():
    return [
        {"group_name": name, "members": members} for name, members in groups.items()
    ]


@url_router.inspect("/call_log")
def get_call_log():
    return call_log


@url_router.inspect("/birthday_reminders")
def get_birthday_reminders():
    today = datetime.now().strftime("%m-%d")
    reminders = [
        {"name": name, "birthday": details["birthday"]}
        for name, details in phonebook.items()
        if details["birthday"].endswith(today)
    ]
    return reminders


if __name__ == "__main__":
    dapp.run()
