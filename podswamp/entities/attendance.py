class Attendance:
    def __init__(self, episodes):
        self.episodes = episodes

    def getAttendance(self, guest):
        dates = [episode.published for episode in sorted(self.episodes.values(), key=lambda e: e.position)]
        attended_dates = [ep.published for ep in guest.episodes]
        mean_attendance = (100.0 * len(attended_dates))/(1.0 * len(dates))
        attended = [{'date':d.strftime("%Y-%m-%d"), 'present': int(d in attended_dates), 'mean_attendance':mean_attendance} for d in dates]

        attendance = 0
        for i, entry in enumerate(attended):
            if entry['present'] or i == 0 or i == (len(attended) - 1):
                attendance += entry['present']
                entry['running_mean'] = (attendance * 100.0)/(i+1) # - mean_attendance

        return attended
