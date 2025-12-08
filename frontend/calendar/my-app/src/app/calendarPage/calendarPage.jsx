import {ScheduleXCalendar, useCalendarApp} from "@schedule-x/react"
import {createViewWeek, createViewMonthGrid} from "@schedule-x/calendar"
import "@schedule-x/theme-default/dist/index.css"
import {useState} from 'react'


function Calendar(){
    const [events,setEvents]=useState([
        // {
        //     id:"1",
        //     title:"Test event",
        //     start:Temporal.ZonedDateTime.from('2025-01-17T10:00:00+02:00[Europe/Bucharest]'),
        //     end:Temporal.ZonedDateTime.from('2025-01-17T11:00:00+02:00[Europe/Bucharest]'),
        // }
    ])
    const calendarApp=useCalendarApp({
        views:[
            createViewWeek(),
            createViewMonthGrid(),
        ],
        events,
    })


    return (
        <>
            <div>
                <h1>Calendar</h1>
                <ScheduleXCalendar calendarApp={calendarApp}/>
            </div>
        </>
    )
}

export default Calendar;