(function(w) {
  w.calendarevents = {
    eventClick: function(base_url, event) {
      window.location.href = base_url+event.uid;
    },
    dayClick: function(base_url, event) {
    }
  };
})(window);
