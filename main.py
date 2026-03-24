"""
=============================================================================
 MAIN -- Student Conference Knowledge Representation Demo
=============================================================================
 This script demonstrates BOTH knowledge-representation approaches:

   1. Semantic Network  - graph of nodes & labelled edges
   2. Frame-Based Model - structured frames with slots, values & defaults

 Run:   python main.py
=============================================================================
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from semantic_network import (
    build_conference_network,
    display_network,
    query_by_relation,
    get_node_relations,
    get_sessions_attended_by,
    get_speakers_in_session,
    nodes,
)

from frame_model import build_conference_frames


# ===================================================================
#  PART 1  —  SEMANTIC NETWORK
# ===================================================================

def demo_semantic_network():
    """Build the network, display it, then run several example queries."""

    # 1-a. Build
    build_conference_network()

    # 1-b. Display full network
    display_network()

    # 1-c. QUERY — sessions attended by Alice
    print("=" * 60)
    print("  QUERY 1: Sessions attended by student_alice")
    print("=" * 60)
    sessions = get_sessions_attended_by("student_alice")
    for s in sessions:
        info = nodes[s]
        print(f"  → {info['name']}  (topic: {info['topic']})")

    # 1-d. QUERY — sessions attended by Bob
    print("\n" + "=" * 60)
    print("  QUERY 2: Sessions attended by student_bob")
    print("=" * 60)
    sessions = get_sessions_attended_by("student_bob")
    for s in sessions:
        info = nodes[s]
        print(f"  → {info['name']}  (topic: {info['topic']})")

    # 1-e. QUERY — who presents in the AI session?
    print("\n" + "=" * 60)
    print("  QUERY 3: Speakers presenting in session_ai")
    print("=" * 60)
    speakers = get_speakers_in_session("session_ai")
    for sp in speakers:
        info = nodes[sp]
        print(f"  → {info['name']}  ({info['affiliation']})")

    # 1-f. QUERY — all "attends" relationships
    print("\n" + "=" * 60)
    print("  QUERY 4: All 'attends' relationships")
    print("=" * 60)
    for subj, obj in query_by_relation("attends"):
        print(f"  {nodes[subj]['name']:20s}  attends  {nodes[obj]['name']}")

    # 1-g. QUERY — all relationships involving the AI session
    print("\n" + "=" * 60)
    print("  QUERY 5: All relationships involving session_ai")
    print("=" * 60)
    relations = get_node_relations("session_ai")
    for r in relations:
        direction = "⟶" if r["direction"] == "outgoing" else "⟵"
        other = nodes[r["other_node"]]["name"]
        print(f"  {direction}  {r['relationship']:18s}  {other}")

    # 1-h. QUERY — where is each session held?
    print("\n" + "=" * 60)
    print("  QUERY 6: Session → Venue mapping (held_at)")
    print("=" * 60)
    for subj, obj in query_by_relation("held_at"):
        print(f"  {nodes[subj]['name']:35s}  held at  {nodes[obj]['name']}")


# ===================================================================
#  PART 2  —  FRAME-BASED MODEL
# ===================================================================

def demo_frame_model():
    """Build frame instances and demonstrate slot access & display."""

    # 2-a. Build
    frames = build_conference_frames()

    # 2-b. Display selected frames
    print("=" * 60)
    print("  FRAME DISPLAY: Conference")
    print("=" * 60)
    frames["conference"].display()

    print("=" * 60)
    print("  FRAME DISPLAY: Student — Alice Mwangi")
    print("=" * 60)
    frames["student_alice"].display()

    print("=" * 60)
    print("  FRAME DISPLAY: Speaker — Dr. Sarah Kim")
    print("=" * 60)
    frames["speaker_dr_kim"].display()

    print("=" * 60)
    print("  FRAME DISPLAY: Session — AI in Healthcare")
    print("=" * 60)
    frames["session_ai"].display()

    print("=" * 60)
    print("  FRAME DISPLAY: Registration — Alice")
    print("=" * 60)
    frames["reg_alice"].display()

    print("=" * 60)
    print("  FRAME DISPLAY: Schedule — Morning Slot")
    print("=" * 60)
    frames["schedule_morning"].display()

    # 2-c. Demonstrate slot access
    print("=" * 60)
    print("  SLOT ACCESS EXAMPLES")
    print("=" * 60)

    # Access a filled slot
    print(f"\n  Alice's university   : {frames['student_alice'].get_slot('university')}")
    print(f"  Alice's sessions     : {frames['student_alice'].get_slot('sessions_attending')}")

    # Access a slot that uses its DEFAULT value
    print(f"  Bob's confirmation # : {frames['reg_bob'].get_slot('confirmation_number')}"
          f"  ← (default, not yet assigned)")

    # Access session venue
    print(f"  AI session venue     : {frames['session_ai'].get_slot('venue')}")
    print(f"  CV session speaker   : {frames['session_cv'].get_slot('speaker')}")

    # 2-d. Demonstrate updating a slot
    print("\n  --- Updating Bob's fee_paid to True ---")
    frames["reg_bob"].set_slot("fee_paid", "True")
    print(f"  Bob fee_paid (after) : {frames['reg_bob'].get_slot('fee_paid')}")

    # 2-e. Show all frames summary
    print("\n" + "=" * 60)
    print("  ALL FRAMES SUMMARY")
    print("=" * 60)
    for key, frame in frames.items():
        print(f"  {key:25s} │ Type: {frame.frame_type:15s} │ Slots: {len(frame.slots)}")


# ===================================================================
#  RUN THE DEMO
# ===================================================================

if __name__ == "__main__":
    print("\n" + "+" + "=" * 68 + "+")
    print("|  STUDENT CONFERENCE -- Knowledge Representation Demo" + " " * 14 + "|")
    print("+" + "=" * 68 + "+\n")

    print("*" * 70)
    print("  PART 1: SEMANTIC NETWORK")
    print("*" * 70)
    demo_semantic_network()

    print("\n\n")
    print("*" * 70)
    print("  PART 2: FRAME-BASED MODEL")
    print("*" * 70)
    demo_frame_model()

    print("\n" + "+" + "=" * 68 + "+")
    print("|  Demo complete -- both models demonstrated successfully!  " + " " * 10 + "|")
    print("+" + "=" * 68 + "+\n")
