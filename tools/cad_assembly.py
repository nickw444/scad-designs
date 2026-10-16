"""Keep named, placed build123d solids separate for rendering and inspection."""
from __future__ import annotations

from dataclasses import dataclass
from build123d import Compound, Shape


@dataclass(frozen=True)
class Component:
    name: str
    part_name: str
    shape: Shape


@dataclass(frozen=True)
class Assembly:
    components: tuple[Component, ...]

    def compound(self) -> Compound:
        """Return a compound without fusing the printed parts."""
        return Compound(children=[item.shape for item in self.components])

    def get(self, name: str) -> Shape:
        return next(item.shape for item in self.components if item.name == name)
