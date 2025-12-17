
import { useEffect, useState, useCallback } from "react";
import { ScheduleXCalendar, useCalendarApp } from "@schedule-x/react";
import { createViewWeek, createViewMonthGrid } from "@schedule-x/calendar";
import { createEventsServicePlugin } from "@schedule-x/events-service";
import { createEventModalPlugin} from "@schedule-x/event-modal"
import "@schedule-x/theme-default/dist/index.css";
import { Temporal } from "@js-temporal/polyfill";

import CreateEventModal from "../events/CreateEventModal";

const API_BASE = process.env.REACT_APP_API_ORIGIN || "http://localhost:8000";

const toZonedDateTime = (iso) =>
  Temporal.ZonedDateTime.from(
    iso.includes("[") ? iso : iso + "[Europe/Bucharest]"
  );

const convertBackendEvent = (e) => ({
  id: String(e.id),
  title: e.title,
  start: toZonedDateTime(e.start_time),
  end: toZonedDateTime(e.end_time),
  description: e.description || "",
  location: e.location || "",
  participants: e.participants || "",
});

function CalendarPage() {
  const eventsService = useState(() => createEventsServicePlugin())[0];
  const [eventModalPlugin] = useState(() => createEventModalPlugin());

  const calendarApp = useCalendarApp({
    views: [createViewWeek(), createViewMonthGrid()],
    events: [],
    plugins: [eventsService,eventModalPlugin],
  });

  const [showModal, setShowModal] = useState(false);

  const loadMyEvents = useCallback(async () => {
    try {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        console.error("No user logged in");
        return;
      }

      const res = await fetch(
        `${API_BASE}/my_events?user_id=${userId}`
      );
      if (!res.ok) {
        console.error("Failed to fetch events", res.status);
        return;
      }

      const data = await res.json();
      const mapped = data.map(convertBackendEvent);
      eventsService.set(mapped);
    } catch (err) {
      console.error("Error fetching events:", err);
    }
  },[eventsService]);

  useEffect(() => {
    loadMyEvents();
  }, [loadMyEvents]);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <div style={{ width: 260, borderRight: "1px solid #ddd", padding: 16 }}>
        <h3>Calendar</h3>
        <button onClick={() => setShowModal(true)}>+ Create event</button>
      </div>

      <div style={{ flex: 1, padding: 16 }}>
        <ScheduleXCalendar calendarApp={calendarApp} />
      </div>

      <CreateEventModal
        open={showModal}
        onClose={() => setShowModal(false)}
        onEventCreated={loadMyEvents}
        apiBase={API_BASE}
      />
    </div>
  );
}

export default CalendarPage;
