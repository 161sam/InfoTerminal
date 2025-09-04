"""ASCII chart helpers using plotext or asciichartpy."""
from __future__ import annotations


def line(series, xs=None, width: int = 80, height: int = 16) -> None:
    """Render a simple line chart."""
    try:
        import plotext as plt

        plt.clear_figure()
        if xs is None:
            xs = list(range(1, len(series) + 1))
        plt.plot(xs, series)
        plt.canvas_color("default")
        plt.axes_color("default")
        plt.figure_size(width, height)
        plt.show()
    except Exception:
        from asciichartpy import plot

        print(plot(series, {"height": min(12, height)}))
