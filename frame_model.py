"""
=============================================================================
 FRAME-BASED MODEL — Student Conference Domain
=============================================================================
 A frame organises knowledge into structured units:
   * FRAME  = a stereotyped entity (like a class / record)
   * SLOT   = a named attribute of the frame
   * VALUE  = the concrete data stored in a slot
   * DEFAULT= a fallback value used when no specific data is provided

 Implementation approach:
   - A base `Frame` class holds a dictionary of `Slot` objects.
   - Specialised subclasses (StudentFrame, SessionFrame …) predefine
     their expected slots together with types and defaults.
=============================================================================
"""


# ---------------------------------------------------------------------------
# 1. Slot — represents a single attribute inside a frame
# ---------------------------------------------------------------------------

class Slot:
    """
    A single slot within a frame.

    Attributes
    ----------
    name         : str   - human-readable name of the slot
    value        : any   - current value (None means "not yet filled")
    default      : any   - fallback value when 'value' is None
    slot_type    : str   - expected data type (informational / documentation)
    """

    def __init__(self, name, value=None, default=None, slot_type="str"):
        self.name = name
        self.value = value
        self.default = default
        self.slot_type = slot_type

    def get_value(self):
        """Return the stored value, falling back to default if necessary."""
        return self.value if self.value is not None else self.default

    def __repr__(self):
        val = self.get_value()
        return f"Slot({self.name}={val!r}, type={self.slot_type})"


# ---------------------------------------------------------------------------
# 2. Frame — base class for all entity frames
# ---------------------------------------------------------------------------

class Frame:
    """
    Base frame class.  Subclasses should call  _add_slot(...)  in their
    __init__  to declare domain-specific slots.
    """

    def __init__(self, frame_name, frame_type="Generic"):
        self.frame_name = frame_name      # unique identifier
        self.frame_type = frame_type      # category label
        self.slots = {}                   # slot_name → Slot object

    # --- Slot management ---------------------------------------------------

    def _add_slot(self, name, value=None, default=None, slot_type="str"):
        """Create and store a new slot inside this frame."""
        self.slots[name] = Slot(name, value, default, slot_type)

    def set_slot(self, name, value):
        """Update an existing slot's value."""
        if name in self.slots:
            self.slots[name].value = value
        else:
            print(f"  [!] Slot '{name}' does not exist in frame '{self.frame_name}'.")

    def get_slot(self, name):
        """Retrieve the effective value of a slot (value or default)."""
        if name in self.slots:
            return self.slots[name].get_value()
        print(f"  [!] Slot '{name}' not found in frame '{self.frame_name}'.")
        return None

    # --- Display -----------------------------------------------------------

    def display(self):
        """Pretty-print the frame and all its slots."""
        print(f"\n{'-' * 55}")
        print(f"  FRAME : {self.frame_name}  ({self.frame_type})")
        print(f"{'-' * 55}")
        for slot in self.slots.values():
            val = slot.get_value()
            src = "value" if slot.value is not None else "default"
            print(f"  {slot.name:25s} | {str(val):30s} [{src}]")
        print(f"{'-' * 55}\n")


# ---------------------------------------------------------------------------
# 3. Specialised Frame Subclasses
# ---------------------------------------------------------------------------

class ConferenceFrame(Frame):
    """Frame for the conference itself."""

    def __init__(self, name="Unnamed Conference", theme="General",
                 year=2026, location="TBD"):
        super().__init__(frame_name=name, frame_type="Conference")
        self._add_slot("name",     value=name,     default="Unnamed Conference")
        self._add_slot("theme",    value=theme,    default="General")
        self._add_slot("year",     value=str(year), default="2026", slot_type="int")
        self._add_slot("location", value=location, default="TBD")
        self._add_slot("status",   value=None,     default="Upcoming")


class StudentFrame(Frame):
    """Frame representing a student participant."""

    def __init__(self, name="Unknown", university="Unknown",
                 program="Undergraduate", email=None):
        super().__init__(frame_name=name, frame_type="Student")
        self._add_slot("name",       value=name,       default="Unknown")
        self._add_slot("university", value=university,  default="Unknown")
        self._add_slot("program",    value=program,     default="Undergraduate")
        self._add_slot("email",      value=email,       default="not provided")
        self._add_slot("sessions_attending", value=None, default="[]", slot_type="list")


class SpeakerFrame(Frame):
    """Frame representing a keynote / session speaker."""

    def __init__(self, name="Unknown", affiliation="Independent",
                 expertise="General", bio=None):
        super().__init__(frame_name=name, frame_type="Speaker")
        self._add_slot("name",        value=name,        default="Unknown")
        self._add_slot("affiliation", value=affiliation,  default="Independent")
        self._add_slot("expertise",   value=expertise,    default="General")
        self._add_slot("bio",         value=bio,          default="No bio available")
        self._add_slot("sessions_presenting", value=None, default="[]", slot_type="list")


class OrganizerFrame(Frame):
    """Frame representing a conference organizer."""

    def __init__(self, name="Unknown", role="Volunteer",
                 department="General", contact=None):
        super().__init__(frame_name=name, frame_type="Organizer")
        self._add_slot("name",       value=name,       default="Unknown")
        self._add_slot("role",       value=role,       default="Volunteer")
        self._add_slot("department", value=department,  default="General")
        self._add_slot("contact",    value=contact,     default="not provided")


class SessionFrame(Frame):
    """Frame representing a conference session / talk."""

    def __init__(self, name="Untitled Session", topic="General",
                 duration_minutes=60, session_type="Talk"):
        super().__init__(frame_name=name, frame_type="Session")
        self._add_slot("name",             value=name,             default="Untitled Session")
        self._add_slot("topic",            value=topic,            default="General")
        self._add_slot("duration_minutes", value=str(duration_minutes), default="60", slot_type="int")
        self._add_slot("session_type",     value=session_type,     default="Talk")
        self._add_slot("speaker",          value=None,             default="TBA")
        self._add_slot("venue",            value=None,             default="TBA")


class VenueFrame(Frame):
    """Frame representing a physical venue / room."""

    def __init__(self, name="Unknown Venue", building="Main Campus",
                 capacity=100, has_projector=True):
        super().__init__(frame_name=name, frame_type="Venue")
        self._add_slot("name",          value=name,              default="Unknown Venue")
        self._add_slot("building",      value=building,          default="Main Campus")
        self._add_slot("capacity",      value=str(capacity),     default="100", slot_type="int")
        self._add_slot("has_projector", value=str(has_projector), default="True", slot_type="bool")


class ScheduleFrame(Frame):
    """Frame representing a time-slot in the conference schedule."""

    def __init__(self, name="Unnamed Slot", date="TBD",
                 time_slot="TBD", session=None, venue=None):
        super().__init__(frame_name=name, frame_type="Schedule")
        self._add_slot("name",      value=name,      default="Unnamed Slot")
        self._add_slot("date",      value=date,      default="TBD")
        self._add_slot("time_slot", value=time_slot, default="TBD")
        self._add_slot("session",   value=session,   default="Unassigned")
        self._add_slot("venue",     value=venue,     default="Unassigned")


class RegistrationFrame(Frame):
    """Frame representing a student's registration record."""

    def __init__(self, student_name="Unknown", registration_date="TBD",
                 fee_paid=False, registration_type="Standard"):
        super().__init__(frame_name=f"Reg-{student_name}", frame_type="Registration")
        self._add_slot("student_name",       value=student_name,       default="Unknown")
        self._add_slot("registration_date",  value=registration_date,  default="TBD")
        self._add_slot("fee_paid",           value=str(fee_paid),      default="False", slot_type="bool")
        self._add_slot("registration_type",  value=registration_type,  default="Standard")
        self._add_slot("confirmation_number", value=None,              default="Pending")


# ---------------------------------------------------------------------------
# 4. Build a Sample Set of Frames
# ---------------------------------------------------------------------------

def build_conference_frames():
    """
    Create and return a dictionary of populated frames for the
    Student Conference scenario.
    """

    print("\n>>> Building Frame-Based Model …\n")

    frames = {}

    # --- Conference ---
    frames["conference"] = ConferenceFrame(
        name="TechSummit 2026",
        theme="AI & Data Science",
        year=2026,
        location="Nairobi, Kenya"
    )

    # --- Students ---
    frames["student_alice"] = StudentFrame(
        name="Alice Mwangi",
        university="University of Nairobi",
        program="MSc Computer Science",
        email="alice@uon.ac.ke"
    )
    frames["student_alice"].set_slot(
        "sessions_attending", "AI in Healthcare, Ethics in AI"
    )

    frames["student_bob"] = StudentFrame(
        name="Bob Ochieng",
        university="Kenyatta University",
        program="BSc Information Technology",
        email="bob@ku.ac.ke"
    )
    frames["student_bob"].set_slot(
        "sessions_attending", "AI in Healthcare, Advances in Computer Vision"
    )

    # --- Speakers ---
    frames["speaker_dr_kim"] = SpeakerFrame(
        name="Dr. Sarah Kim",
        affiliation="MIT",
        expertise="Natural Language Processing",
        bio="Leading researcher in biomedical NLP with 50+ publications."
    )
    frames["speaker_dr_kim"].set_slot(
        "sessions_presenting", "AI in Healthcare, Ethics in AI"
    )

    frames["speaker_prof_lee"] = SpeakerFrame(
        name="Prof. James Lee",
        affiliation="Stanford University",
        expertise="Computer Vision",
        bio="Pioneer of real-time object detection architectures."
    )
    frames["speaker_prof_lee"].set_slot(
        "sessions_presenting", "Advances in Computer Vision"
    )

    # --- Organizer ---
    frames["organizer_carol"] = OrganizerFrame(
        name="Carol Njeri",
        role="Conference Chair",
        department="Computer Science Dept.",
        contact="carol@uon.ac.ke"
    )

    # --- Sessions ---
    frames["session_ai"] = SessionFrame(
        name="AI in Healthcare",
        topic="Artificial Intelligence",
        duration_minutes=90,
        session_type="Keynote"
    )
    frames["session_ai"].set_slot("speaker", "Dr. Sarah Kim")
    frames["session_ai"].set_slot("venue",   "Main Auditorium")

    frames["session_cv"] = SessionFrame(
        name="Advances in Computer Vision",
        topic="Computer Vision",
        duration_minutes=60,
        session_type="Talk"
    )
    frames["session_cv"].set_slot("speaker", "Prof. James Lee")
    frames["session_cv"].set_slot("venue",   "Lab B")

    frames["session_ethics"] = SessionFrame(
        name="Ethics in AI",
        topic="AI Ethics",
        duration_minutes=45,
        session_type="Panel Discussion"
    )
    frames["session_ethics"].set_slot("speaker", "Dr. Sarah Kim")
    frames["session_ethics"].set_slot("venue",   "Main Auditorium")

    # --- Venues ---
    frames["venue_main"] = VenueFrame(
        name="Main Auditorium",
        building="Science Complex",
        capacity=500,
        has_projector=True
    )

    frames["venue_lab_b"] = VenueFrame(
        name="Lab B",
        building="Engineering Block",
        capacity=80,
        has_projector=True
    )

    # --- Schedules ---
    frames["schedule_morning"] = ScheduleFrame(
        name="Morning Slot",
        date="2026-06-15",
        time_slot="09:00 - 12:00",
        session="AI in Healthcare",
        venue="Main Auditorium"
    )

    frames["schedule_afternoon"] = ScheduleFrame(
        name="Afternoon Slot",
        date="2026-06-15",
        time_slot="14:00 - 17:00",
        session="Advances in Computer Vision / Ethics in AI",
        venue="Lab B / Main Auditorium"
    )

    # --- Registrations ---
    frames["reg_alice"] = RegistrationFrame(
        student_name="Alice Mwangi",
        registration_date="2026-05-01",
        fee_paid=True,
        registration_type="Early Bird"
    )
    frames["reg_alice"].set_slot("confirmation_number", "CONF-2026-0012")

    frames["reg_bob"] = RegistrationFrame(
        student_name="Bob Ochieng",
        registration_date="2026-05-10",
        fee_paid=False,
        registration_type="Standard"
    )

    print(">>> Frame-Based Model built successfully!\n")
    return frames
