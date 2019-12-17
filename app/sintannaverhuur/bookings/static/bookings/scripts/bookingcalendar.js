document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(document.getElementById('calendar0'), {
    
        locale: 'nl',
        plugins: [ 'dayGrid', 'interaction', 'googleCalendar'],
        defaultDate: new Date(),
        header: {
            left: 'title',
            center: '',
            right: 'prev today next'
        },
        // Prohibite user to book a date in the past or to book a date longer then 6 months upfront
        validRange: {
            start: new Date(),
            end: new Date().setMonth(new Date().getMonth() + 6)
        },
        // Load google events in calendar
        googleCalendarApiKey: 'AIzaSyB5Qs9AB4CFwehI7WvLbq9B0j8SLlmjekQ',
        events: {
            googleCalendarId: 'uhtbefspsip0e23u07cspnj2r4@group.calendar.google.com',
            overlap: false,
            color: '#ff9f89'
        },
        buttonText: {
            today: 'vandaag'
        },

        background: 'red',
        // Allow user to select dates
        selectable: true,
        select: function(info) {
            selectOverlap = false;
            overlap = false;            
            // Get start & end values of selected dates and enter them in variable
            var start = info.startStr;
            var end = info.endStr;
            document.getElementById("arrival_date").value = start;
            document.getElementById("departure_date").value = end;
            
        },

    });
    // load calendar
    calendar.render();
});