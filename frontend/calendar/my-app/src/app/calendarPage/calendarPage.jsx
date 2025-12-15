import {ScheduleXCalendar, useCalendarApp} from "@schedule-x/react"
import {createViewWeek, createViewMonthGrid} from "@schedule-x/calendar"
import "@schedule-x/theme-default/dist/index.css"
import {useState,useEffect,handleChange} from 'react'
import { Temporal } from '@js-temporal/polyfill'
import { createEventsServicePlugin } from '@schedule-x/events-service'
import {createDragAndDropPlugin} from "@schedule-x/drag-and-drop"
import {createEventModalPlugin} from "@schedule-x/event-modal"

const API_BASE="http://localhost:8000"

function Calendar(){
    const eventsService = createEventsServicePlugin()

    const convertBackendEvent = (e) => {
        return {
            id: String(e.id),
            title: e.title,
            start: Temporal.ZonedDateTime.from(e.start_time),
            end: Temporal.ZonedDateTime.from(e.end_time),
            extendedProps: {
                description: e.description,
                location: e.location,
                ownerId: e.owner_id,
                participants: e.participants,
            },
        }
    }

    const calendarApp=useCalendarApp({
        views:[
            createViewWeek(),
            createViewMonthGrid(),
        ],
        events:[],
        plugins:[eventsService,createDragAndDropPlugin(),createEventModalPlugin()],
    })

    const [showModal, setShowModal] = useState(false);
    const [form, setForm] = useState({
        title: '',
        event_date: '',
        start_time: '',
        end_time: '',
        description: '',
        location: '',
        participant_ids: '',
    });

    useEffect(() => {
    const loadEvents = async () => {
      try {
        const userId=localStorage.getItem("user_id");

        if(!userId){
          console.error("No user logged in");
          return;
        }

        const res = await fetch(`${API_BASE}/my_events?user_id=${userId}`);
        if (!res.ok) {
          console.error('Failed to fetch events', res.status);
          return;
        }

        const data = await res.json();
        console.log('Events from backend:', data);

        const mapped = data.map(convertBackendEvent);
        console.log('Mapped for Schedule X:', mapped);

        eventsService.set(mapped);
      } catch (err) {
        console.error('Error fetching events:', err);
      }
    }

    loadEvents();
  }, [eventsService])

    const handleCreateEvent = async () => {
        const {
            title,
            event_date,
            start_time,
            end_time,
            description,
            location,
            participant_ids,
        } = form

        if (!title || !event_date || !start_time || !end_time) {
            alert('Title, event_date, start_time, end_time sunt obligatorii')
            return
        }
        const participantIdsArray =
        participant_ids.trim() === ''
            ? []
            : participant_ids.split(',').map((id) => parseInt(id.trim(), 10))

        try {
        const res = await fetch(`${API_BASE}/events`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
            title,
            event_date,
            start_time,
            end_time,
            description: description || null,
            location: location || null,
            participant_ids: participantIdsArray,
            }),
        })

        if (!res.ok) {
            const errBody = await res.json().catch(() => ({}))
            console.error('Failed to create event', res.status, errBody)
            alert('Nu am putut crea eventul')
            return
        }

        const created = await res.json()
        const mapped = convertBackendEvent(created)

        eventsService.add(mapped)

        setForm({
            title: '',
            event_date: '',
            start_time: '',
            end_time: '',
            description: '',
            location: '',
            participant_ids: '',
        })
        setShowModal(false)
        } catch (err) {
        console.error('Error creating event:', err)
        alert('Eroare la creare event')
        }
    }

    return (
        <div style={{display:'flex'}}>
            <div style={{ width: 260, borderRight: '1px solid #ddd', padding: 16 }}>
                <h3>Calendar</h3>
                <button onClick={() => setShowModal(true)}>+ Create event</button>
            </div>

             <div style={{ flex: 1, padding: 16 }}>
                <ScheduleXCalendar calendarApp={calendarApp} />
            </div>
            {showModal && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0,0,0,0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <div
            style={{
              background: 'white',
              padding: 20,
              borderRadius: 8,
              width: 320,
            }}
          >
            <h3>Create event</h3>

            <label>
              Title
              <input
                type="text"
                value={form.title}
                onChange={handleChange('title')}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <label>
              Date (YYYY-MM-DD)
              <input
                type="date"
                value={form.event_date}
                onChange={handleChange('event_date')}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <label>
              Start time
              <input
                type="time"
                value={form.start_time}
                onChange={handleChange('start_time')}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <label>
              End time
              <input
                type="time"
                value={form.end_time}
                onChange={handleChange('end_time')}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <label>
              Description
              <textarea
                value={form.description}
                onChange={handleChange('description')}
                rows={3}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <label>
              Location
              <input
                type="text"
                value={form.location}
                onChange={handleChange('location')}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <label>
              Participant IDs (comma separated)
              <input
                type="text"
                placeholder="ex: 2,3,5"
                value={form.participant_ids}
                onChange={handleChange('participant_ids')}
                style={{ width: '100%', marginBottom: 8 }}
              />
            </label>

            <div style={{ marginTop: 12 }}>
              <button onClick={handleCreateEvent}>Save</button>
              <button
                onClick={() => setShowModal(false)}
                style={{ marginLeft: 8 }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
        </div>
    )
}

export default Calendar;