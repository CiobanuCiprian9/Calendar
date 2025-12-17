import { useState } from "react";
import "./CreateEventModal.css";

function CreateEventModal({ open, onClose, onEventCreated, apiBase }) {
  const [form, setForm] = useState({
    title: "",
    event_date: "",
    start_time: "",
    end_time: "",
    description: "",
    location: "",
  });

  const [participantSearch, setParticipantSearch] = useState("");
  const [participantSuggestions, setParticipantSuggestions] = useState([]);
  const [selectedParticipants, setSelectedParticipants] = useState([]);
  const [showSuggestions, setShowSuggestions]=useState(false)
  if (!open) return null;
  const handleFormChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleParticipantSearchChange = async (e) => {
  const value = e.target.value;
  setParticipantSearch(value);

  if (!value.trim()) {
    setParticipantSuggestions([]);
    setShowSuggestions(false);
    return;
  }

  await fetchUsers(value);
};


  const fetchUsers = async (query) => {
    try {
      const res = await fetch(
        `${apiBase}/search?q=${encodeURIComponent(query)}`
      );
      if (!res.ok) {
        console.error("Failed to search users", res.status);
        return;
      }
      const data = await res.json();
      setParticipantSuggestions(data);
      setShowSuggestions(true);
    } catch (err) {
      console.error("Error searching users:", err);
    }
  };
const handleParticipantFocus = () => {
  if (participantSuggestions.length > 0) {
    setShowSuggestions(true);
  }
};

  const handleAddParticipant = (user) => {
    if (selectedParticipants.some((p) => p.id === user.id)) return;
    setSelectedParticipants((prev) => [...prev, user]);
    setParticipantSearch("");
    setParticipantSuggestions([]);
    setShowSuggestions(false);
  };

  const handleRemoveParticipant = (id) => {
    setSelectedParticipants((prev) => prev.filter((p) => p.id !== id));
  };

  const handleCreateEvent = async () => {
    const {
      title,
      event_date,
      start_time,
      end_time,
      description,
      location,
    } = form;

    if (!title || !event_date || !start_time || !end_time) {
      alert("Title, event_date, start_time, end_time sunt obligatorii");
      return;
    }

    const participantIdsArray = selectedParticipants.map((p) => p.id);

    try {
      const userId = localStorage.getItem("user_id");

      const res = await fetch(
        `${apiBase}/create_event?user_id=${userId}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            title,
            event_date,
            start_time,
            end_time,
            description: description || null,
            location: location || null,
            participant_ids: participantIdsArray,
          }),
        }
      );

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        console.error("Failed to create event", res.status, errBody);
        alert("Nu am putut crea eventul");
        return;
      }

      await res.json();

      if (onEventCreated) {
        await onEventCreated();
      }

      setForm({
        title: "",
        event_date: "",
        start_time: "",
        end_time: "",
        description: "",
        location: "",
      });
      setSelectedParticipants([]);
      setParticipantSearch("");
      setParticipantSuggestions([]);
      onClose();
    } catch (err) {
      console.error("Error creating event:", err);
      alert("Eroare la creare event");
    }
  };


  const handleTimeChange = (field) => (e) => {
  let v = e.target.value;
  if (!v) {
    setForm((prev) => ({ ...prev, [field]: "" }));
    return;
  }

  const [hStr, mStr] = v.split(":");
  let h = parseInt(hStr, 10);
  let m = parseInt(mStr, 10);

  let slot = Math.round(m / 15) * 15;

  const hh = String(h).padStart(2, "0");
  const mm = String(slot).padStart(2, "0");
  const normalized = `${hh}:${mm}`;

  setForm((prev) => ({ ...prev, [field]: normalized }));
};


  return (
    <div className="event-modal">
      <div className="event-card">
        <h3>Create event</h3>

        <label className="field">
          <span>Title</span>
          <input
            type="text"
            value={form.title}
            onChange={handleFormChange("title")}
          />
        </label>

        <label className="field">
          <span>Date</span>
          <input
            type="date"
            value={form.event_date}
            onChange={handleFormChange("event_date")}
          />
        </label>

        <label className="field">
          <span>Start time</span>
          <input
            type="time"
            step="900"
            value={form.start_time}
            onChange={handleTimeChange("start_time")}
          />
        </label>

        <label className="field">
          <span>End time</span>
          <input
            type="time"
            step="900"
            value={form.end_time}
            onChange={handleTimeChange("end_time")}
          />
        </label>

        <label className="field">
          <span>Description</span>
          <textarea
            value={form.description}
            onChange={handleFormChange("description")}
            rows={3}
          />
        </label>

        <label className="field">
          <span>Location</span>
          <input
            type="text"
            value={form.location}
            onChange={handleFormChange("location")}
          />
        </label>

        <label className="field">
          <span>Participants (search by email)</span>
          <input
            type="text"
            value={participantSearch}
            onChange={handleParticipantSearchChange}
            onFocus={handleParticipantFocus}
          />
        </label>

        {showSuggestions && participantSuggestions.length > 0 && (
          <div className="user-search">
            {participantSuggestions.map((u) => (
              <div className="user-find"
                key={u.id}
                onClick={() => handleAddParticipant(u)}
              >
                {u.email} ({u.first_name} {u.last_name})
              </div>
            ))}
          </div>
        )}

        {selectedParticipants.length > 0 && (
          <div className="user-selected">
            {selectedParticipants.map((p) => (
              <span key={p.id} className="user-selected-box">
                {p.email}
                <button
                  className="user-cancel"
                  onClick={() => handleRemoveParticipant(p.id)}
                >
                  x
                </button>
              </span>
            ))}
          </div>
        )}

        <div className="finish-event-buttons">
          <button onClick={onClose}>Cancel</button>
          <button onClick={handleCreateEvent}>Save</button>
        </div>
      </div>
    </div>
  );
}

export default CreateEventModal;
