import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Events() {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = () => {
            axios.get('/api/events/', {
                headers: { Authorization: `Token ${localStorage.getItem('token')}` }
            })
            .then(response => setEvents(response.data))
            .catch(error => console.error('Error fetching events', error));
        };

        fetchEvents();
    }, []);

    return (
        <div>
            <h2>Events</h2>
            <ul>
                {events.map(event => (
                    <li key={event.id}>
                        {event.event_name} - {event.date} at {event.time}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Events;
