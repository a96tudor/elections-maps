class VotingSection:
    def __init__(self, number, name, searchable_name, latitude=None, longitude=None):
        self.number = number
        self.name = name
        self.searchable_name = searchable_name
        self.latitude = latitude
        self.longitude = longitude

        self.voting_information = None
        self.icon_color = None
        self._mayor_voting_results = None
        self._local_council_voting_results = None

    @property
    def mayor_voting_results(self):
        return self._mayor_voting_results

    @mayor_voting_results.setter
    def mayor_voting_results(self, mvr):
        self._mayor_voting_results = mvr.sorted

        for vr in self._mayor_voting_results:
            vr.percentage = vr.votes / self.voting_information.total_voters

    @property
    def local_council_voting_results(self):
        return self._local_council_voting_results

    @local_council_voting_results.setter
    def local_council_voting_results(self, lcvr):
        self._local_council_voting_results = lcvr.sorted

        for vr in self._local_council_voting_results:
            vr.percentage = vr.votes / self.voting_information.total_voters

    @property
    def marker(self):
        jinja_env = jinja2.Environment(loader=jinja2.BaseLoader)
        rendered_html = jinja_env.from_string(POPUP_HTML).render(
            title=f"Sectia {self.number} - {self.name}",
            total_possible_voters=self.voting_information.total_possible_voters,
            attendance=self.voting_information.total_voters,
            attendance_percentage=self.voting_information.attendance_percentage,
            genders_plot_b64=from_png_file_to_b64(
                os.path.join("plots", "genders", f"{self.number}.png"),
            ),
            ages_plot_b64=from_png_file_to_b64(
                os.path.join("plots", "ages", f"{self.number}.png"),
            ),
            mayor_voting_results=self.mayor_voting_results,
            local_council_voting_results=self.local_council_voting_results,
        )

        popup = folium.Popup(folium.IFrame(rendered_html, width=500, height=250))

        return folium.Marker(
            location=[self.latitude, self.longitude],
            icon=plugins.BeautifyIcon(
                background_color=self.icon_color,
                icon_shape="marker",
            ),
            radius=3,
            popup=popup,
            tooltip=self.voting_information.attendance_percentage,
            lazy=True,
        )

    def to_dict(self):
        return {
            "number": self.number,
            "name": self.name,
            "searchable_name": self.searchable_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @classmethod
    def from_dict_csv(cls, voting_section):
        return cls(
            number=voting_section["number"],
            name=voting_section["name"],
            searchable_name=voting_section["searchable_name"],
            latitude=float(voting_section["latitude"]),
            longitude=float(voting_section["longitude"]),
        )
