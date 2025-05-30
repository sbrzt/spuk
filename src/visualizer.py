import pygal
from pygal.style import Style
from typing import List, Dict
from src.profile import Profile


class Visualizer:
    def __init__(
        self, 
        profile: Profile
        ) -> None:
        self.profile = profile
        self.style = Style(
            background = "white",
            plot_background = "white",
            opacity = ".6",
            opacity_hover = ".8",
            value_colors = ("black",)
        )

    def _generate_bar(
        self, 
        title: str, 
        data: List[Dict[str, str | int]]
        ) -> str:
        bar_chart = pygal.HorizontalBar(
            style = self.style
            )
        bar_chart.title = title
        for d in data:
            bar_chart.add(d["label"], d["frequency"])
        return bar_chart.render(
            legend_at_bottom = True,
            legend_box_size = 5,
            legend_at_bottom_columns = 2,
            order_min = 1,
        ).decode("utf-8")

    def most_frequent_properties_chart(
        self
        ) -> str:
        data = [
            {
                "label": uri, 
                "frequency": freq
            }
            for uri, freq in self.profile.most_frequent_properties
        ]
        return self._generate_bar(f"{data[0]['label']} is the most used property", data)

    def most_frequent_classes_chart(
        self
        ) -> str:
        data = [
            {
                "label": uri, 
                "frequency": freq
            }
            for uri, freq in self.profile.most_frequent_classes
        ]
        return self._generate_bar(f"{data[0]['label']} is the most used class", data)

    def most_frequent_models_chart(
        self 
        ) -> str:

        data = [
            {
                "label": f"{prefix}: {ns}", 
                "frequency": freq
            }
            for prefix, ns, freq in self.profile.most_frequent_models
        ]
        return self._generate_bar(f"{data[0]['label']} is the most used model", data)

    def most_frequent_entities_chart(
        self
        ) -> str:
        data = [
            {
                "label": uri,
                "frequency": freq
            }
            for uri, freq in self.profile.most_frequent_entities
        ]
        return self._generate_bar(f"{data[0]['label']} is the most used entity", data)
