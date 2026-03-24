"""
=============================================================================
 SEMANTIC NETWORK — Student Conference Domain
=============================================================================
 A semantic network represents knowledge as a directed graph:
   • NODES  = entities (students, speakers, sessions, venues …)
   • EDGES  = labelled relationships between entities
              (attends, presents, organizes, held_at …)

 Data structures used:
   nodes  - dict  { node_id: {attribute: value, ...} }
   edges  - list  [ (subject, relationship, object), ... ]
=============================================================================
"""


# ---------------------------------------------------------------------------
# 1. Core Data Structures
# ---------------------------------------------------------------------------

# Each node is stored as   node_id  ->  { attribute dictionary }
nodes = {}

# Each edge is a triple   (subject_id, relationship, object_id)
edges = []


# ---------------------------------------------------------------------------
# 2. Helper Functions — Building the Network
# ---------------------------------------------------------------------------

def add_node(node_id, attributes):
    """
    Add a node (entity) to the semantic network.


    Parameters
    ----------
    node_id    : str   - unique identifier for the node (e.g. "student_alice")
    attributes : dict  - properties of the entity
                         (e.g. {"name": "Alice", "type": "Student"})
    """
    nodes[node_id] = attributes
    print(f"  [+] Node added: {node_id}")


def add_edge(subject, relationship, obj):
    """
    Add a directed edge (relationship) between two nodes.

    Parameters
    ----------
    subject      : str - source node id
    relationship : str - label for the relationship (e.g. "attends")
    obj          : str - target node id
    """
    edges.append((subject, relationship, obj))
    print(f"  [+] Edge added: {subject} --({relationship})--> {obj}")


# ---------------------------------------------------------------------------
# 3. Query Functions — Retrieving Knowledge
# ---------------------------------------------------------------------------

def query_by_relation(relationship):
    """
    Return all (subject, object) pairs that share the given relationship.

    Example:  query_by_relation("attends")
              -> [("student_alice", "session_ai"), ...]
    """
    results = [(s, o) for s, r, o in edges if r == relationship]
    return results


def get_node_relations(node_id):
    """
    Return every relationship where *node_id* appears as subject OR object.

    Returns a list of dicts with keys: direction, relationship, other_node.
    """
    results = []
    for s, r, o in edges:
        if s == node_id:
            results.append({
                "direction": "outgoing",
                "relationship": r,
                "other_node": o
            })
        elif o == node_id:
            results.append({
                "direction": "incoming",
                "relationship": r,
                "other_node": s
            })
    return results


def get_sessions_attended_by(student_id):
    """
    Convenience query: return sessions attended by a specific student.
    """
    return [o for s, r, o in edges if s == student_id and r == "attends"]


def get_speakers_in_session(session_id):
    """
    Convenience query: return speakers presenting in a specific session.
    """
    return [s for s, r, o in edges if o == session_id and r == "presents"]


def display_network():
    """
    Print a human-readable summary of the entire semantic network.
    """
    print("\n" + "=" * 70)
    print("             SEMANTIC NETWORK -- Full Overview")
    print("=" * 70)

    # --- Nodes ---
    print("\n[NODES] (Entities)")
    print("-" * 50)
    for nid, attrs in nodes.items():
        attr_str = ", ".join(f"{k}: {v}" for k, v in attrs.items())
        print(f"  * {nid:30s} | {attr_str}")

    # --- Edges ---
    print(f"\n[EDGES] (Relationships)  - total: {len(edges)}")
    print("-" * 50)
    for s, r, o in edges:
        print(f"  {s}  --({r})-->  {o}")

    print("=" * 70 + "\n")


# ---------------------------------------------------------------------------
# 4. Build the Student Conference Semantic Network
# ---------------------------------------------------------------------------

def build_conference_network():
    """
    Populate the semantic network with sample Student Conference data.
    This function demonstrates 8 entity types and 12+ relationships.
    """

    print("\n>>> Building Semantic Network …\n")

    # ---------- Conference (root entity) ----------

    add_node("conference_techsummit", {
        "name": "TechSummit 2026",
        "type": "Conference",
        "theme": "AI & Data Science",
        "year": 2026
    })

    # ---------- Students ----------
    add_node("student_alice", {
        "name": "Alice Mwangi",
        "type": "Student",
        "university": "University of Nairobi",
        "program": "MSc Computer Science"
    })

    add_node("student_bob", {
        "name": "Bob Ochieng",
        "type": "Student",
        "university": "Kenyatta University",
        "program": "BSc Information Technology"
    })

    # ---------- Speakers ----------
    add_node("speaker_dr_kim", {
        "name": "Dr. Sarah Kim",
        "type": "Speaker",
        "affiliation": "MIT",
        "expertise": "Natural Language Processing"
    })

    add_node("speaker_prof_lee", {
        "name": "Prof. James Lee",
        "type": "Speaker",
        "affiliation": "Stanford University",
        "expertise": "Computer Vision"
    })

    # ---------- Organizer ----------
    add_node("organizer_carol", {
        "name": "Carol Njeri",
        "type": "Organizer",
        "role": "Conference Chair",
        "department": "Computer Science Dept."
    })

    # ---------- Sessions ----------
    add_node("session_ai", {
        "name": "AI in Healthcare",
        "type": "Session",
        "topic": "Artificial Intelligence",
        "duration_minutes": 90
    })

    add_node("session_cv", {
        "name": "Advances in Computer Vision",
        "type": "Session",
        "topic": "Computer Vision",
        "duration_minutes": 60
    })

    add_node("session_ethics", {
        "name": "Ethics in AI",
        "type": "Session",
        "topic": "AI Ethics",
        "duration_minutes": 45
    })

    # ---------- Venues ----------
    add_node("venue_main_hall", {
        "name": "Main Auditorium",
        "type": "Venue",
        "capacity": 500,
        "building": "Science Complex"
    })

    add_node("venue_lab_b", {
        "name": "Lab B",
        "type": "Venue",
        "capacity": 80,
        "building": "Engineering Block"
    })

    # ---------- Schedules ----------
    add_node("schedule_morning", {
        "name": "Morning Slot",
        "type": "Schedule",
        "date": "2026-06-15",
        "time_slot": "09:00 – 12:00"
    })

    add_node("schedule_afternoon", {
        "name": "Afternoon Slot",
        "type": "Schedule",
        "date": "2026-06-15",
        "time_slot": "14:00 – 17:00"
    })

    # ---------- Registrations ----------
    add_node("registration_alice", {
        "name": "Alice Registration",
        "type": "Registration",
        "registration_date": "2026-05-01",
        "fee_paid": True
    })

    add_node("registration_bob", {
        "name": "Bob Registration",
        "type": "Registration",
        "registration_date": "2026-05-10",
        "fee_paid": False
    })

    # ------------------------------------------------------------------
    #  RELATIONSHIPS  (edges)
    # ------------------------------------------------------------------
    print()

    # is_a / part_of (taxonomy)
    add_edge("student_alice",        "is_a",           "conference_techsummit")
    add_edge("student_bob",          "is_a",           "conference_techsummit")
    add_edge("session_ai",           "part_of",        "conference_techsummit")
    add_edge("session_cv",           "part_of",        "conference_techsummit")
    add_edge("session_ethics",       "part_of",        "conference_techsummit")

    # attends
    add_edge("student_alice",        "attends",        "session_ai")
    add_edge("student_alice",        "attends",        "session_ethics")
    add_edge("student_bob",          "attends",        "session_ai")
    add_edge("student_bob",          "attends",        "session_cv")

    # presents
    add_edge("speaker_dr_kim",       "presents",       "session_ai")
    add_edge("speaker_prof_lee",     "presents",       "session_cv")
    add_edge("speaker_dr_kim",       "presents",       "session_ethics")

    # organizes
    add_edge("organizer_carol",      "organizes",      "conference_techsummit")
    add_edge("organizer_carol",      "organizes",      "session_ai")

    # held_at  (session → venue)
    add_edge("session_ai",           "held_at",        "venue_main_hall")
    add_edge("session_cv",           "held_at",        "venue_lab_b")
    add_edge("session_ethics",       "held_at",        "venue_main_hall")

    # scheduled_in  (session → schedule)
    add_edge("session_ai",           "scheduled_in",   "schedule_morning")
    add_edge("session_cv",           "scheduled_in",   "schedule_afternoon")
    add_edge("session_ethics",       "scheduled_in",   "schedule_afternoon")

    # registered_for  (registration -> student)
    add_edge("registration_alice",   "registered_for", "student_alice")
    add_edge("registration_bob",     "registered_for", "student_bob")

    print("\n>>> Semantic Network built successfully!\n")
