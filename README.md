# Student Conference — Knowledge Representation

A Python-based implementation of two fundamental AI knowledge-representation techniques applied to a **Student Conference** domain:

1. **Semantic Network** — graph of nodes (entities) connected by labelled relationship edges
2. **Frame-Based Model** — structured frames with typed slots, values, and default values

---

## Project Structure

```
SEMANTIC NETWORKS AND FRAMES/
├── semantic_network.py   # Semantic network: nodes, edges, query functions
├── frame_model.py        # Frame model: Slot/Frame classes, 8 entity subclasses
├── main.py               # Demo script exercising both representations
└── README.md
```

---

## Domain Overview

### Entities (8 types)

| Entity         | Description                              |
|----------------|------------------------------------------|
| **Conference** | The conference event itself               |
| **Student**    | A student participant                     |
| **Speaker**    | A keynote or session speaker              |
| **Organizer**  | A person organizing the conference        |
| **Session**    | A talk, keynote, or panel discussion      |
| **Venue**      | A physical room or auditorium             |
| **Schedule**   | A time slot on the conference schedule    |
| **Registration** | A student's registration record         |

### Relationships

| Relationship     | Example                                  |
|------------------|------------------------------------------|
| `attends`        | Student attends a Session                |
| `presents`       | Speaker presents in a Session            |
| `organizes`      | Organizer organizes the Conference       |
| `held_at`        | Session is held at a Venue               |
| `scheduled_in`   | Session is scheduled in a time slot      |
| `registered_for` | Registration links to a Student          |
| `is_a`           | Student is a participant of Conference   |
| `part_of`        | Session is part of Conference            |

---

## How to Run

**Prerequisites:** Python 3.6+

```bash
cd "SEMANTIC NETWORKS AND FRAMES"
python main.py
```

The output includes:
- Full semantic network overview (all nodes and edges)
- 6 example queries (sessions by student, speakers in session, venue mapping, etc.)
- Frame displays with `[value]` / `[default]` annotations
- Slot access and mutation examples

---

## Module Details

### `semantic_network.py`

Represents knowledge as a **directed labelled graph**.

- **`nodes`** — dictionary mapping node IDs to attribute dictionaries
- **`edges`** — list of `(subject, relationship, object)` triples

Key functions:

| Function                        | Purpose                                         |
|---------------------------------|-------------------------------------------------|
| `add_node(id, attrs)`          | Add an entity node                               |
| `add_edge(subj, rel, obj)`    | Add a relationship edge                          |
| `query_by_relation(rel)`       | Get all pairs sharing a relationship             |
| `get_node_relations(id)`       | Get all relationships involving a node           |
| `get_sessions_attended_by(id)` | Sessions a specific student attends              |
| `get_speakers_in_session(id)`  | Speakers presenting in a specific session        |
| `display_network()`            | Print full network summary                       |

### `frame_model.py`

Represents knowledge as **structured frames** with slots.

- **`Slot`** — holds `name`, `value`, `default`, and `slot_type`
- **`Frame`** — base class with slot management (`_add_slot`, `set_slot`, `get_slot`, `display`)
- **8 subclasses**: `ConferenceFrame`, `StudentFrame`, `SpeakerFrame`, `OrganizerFrame`, `SessionFrame`, `VenueFrame`, `ScheduleFrame`, `RegistrationFrame`

Each slot returns its `value` if set, otherwise falls back to `default`.

---

## Example Queries

```python
from semantic_network import *

# Build the network
build_conference_network()

# What sessions does Alice attend?
sessions = get_sessions_attended_by("student_alice")
for s in sessions:
    print(nodes[s]["name"])
# Output: AI in Healthcare, Ethics in AI

# Who speaks in the AI session?
speakers = get_speakers_in_session("session_ai")
for sp in speakers:
    print(nodes[sp]["name"])
# Output: Dr. Sarah Kim
```

```python
from frame_model import *

# Build frames
frames = build_conference_frames()

# Access a slot value
print(frames["student_alice"].get_slot("university"))
# Output: University of Nairobi

# Access a default value (not yet assigned)
print(frames["reg_bob"].get_slot("confirmation_number"))
# Output: Pending
```

---

## Extending the System

The design is **scalable** — to add new entity types (e.g., Sponsors, Workshops):

1. **Semantic Network**: add new nodes with `add_node()` and connect them with `add_edge()`
2. **Frame Model**: create a new subclass of `Frame` with appropriate slots

```python
# Example: adding a Sponsor
class SponsorFrame(Frame):
    def __init__(self, name="Unknown", tier="Bronze", contribution=0):
        super().__init__(frame_name=name, frame_type="Sponsor")
        self._add_slot("name", value=name, default="Unknown")
        self._add_slot("tier", value=tier, default="Bronze")
        self._add_slot("contribution", value=str(contribution), default="0", slot_type="int")
```

---

## Author

Built as an academic demonstration of **Semantic Networks** and **Frame-Based Knowledge Representation** in Artificial Intelligence.
