"""Cedar raised garden bed with soil and six plants in a row."""

from __future__ import annotations

from typing import Any

from build123d import Sphere
from python_cad_tools.elements import Dimensions
from python_cad_tools.geometry import cylinder_between
from python_cad_tools.units import INCH, to_mm

from models.shared import ZERO


def add_garden_bed(builder: Any, cfg: Any) -> None:
    """Add the raised cedar garden bed, soil fill, and six plants."""
    x0, y0 = cfg.GARDEN_BED_X, cfg.GARDEN_BED_Y
    length, width = cfg.GARDEN_BED_LENGTH, cfg.GARDEN_BED_WIDTH
    height = cfg.GARDEN_BED_HEIGHT
    thickness = cfg.GARDEN_BED_BOARD_THICKNESS
    soil_height = cfg.GARDEN_BED_SOIL_HEIGHT

    x1 = x0 + length
    y1 = y0 + width
    cedar_color = cfg.GARDEN_BED_CEDAR_COLOR
    soil_color = cfg.GARDEN_BED_SOIL_COLOR
    plant_color = cfg.GARDEN_BED_PLANT_COLOR

    parent = builder.add_box(
        "site",
        "Raised Cedar Garden Bed",
        length,
        thickness,
        height,
        x0,
        y1 - thickness,
        ZERO,
        cedar_color,
        stable_id="complex.site.raised_cedar_garden_bed",
        properties={
            "complex_type": "raised_garden_bed",
            "assembly_role": "primary_structure",
            "board_nominal_thickness_in": 1.5,
        },
    )
    parent_id = parent.id

    builder.add_box(
        "site",
        "Raised Garden Bed Cedar Board South",
        length,
        thickness,
        height,
        x0,
        y0,
        ZERO,
        cedar_color,
        parent_id=parent_id,
        properties={"complex_type": "raised_garden_bed_board", "assembly_role": "south_wall"},
    )
    builder.add_box(
        "site",
        "Raised Garden Bed Cedar Board West",
        thickness,
        width - 2 * thickness,
        height,
        x0,
        y0 + thickness,
        ZERO,
        cedar_color,
        parent_id=parent_id,
        properties={"complex_type": "raised_garden_bed_board", "assembly_role": "west_wall"},
    )
    builder.add_box(
        "site",
        "Raised Garden Bed Cedar Board East",
        thickness,
        width - 2 * thickness,
        height,
        x1 - thickness,
        y0 + thickness,
        ZERO,
        cedar_color,
        parent_id=parent_id,
        properties={"complex_type": "raised_garden_bed_board", "assembly_role": "east_wall"},
    )
    builder.add_box(
        "site",
        "Raised Garden Bed Soil",
        length - 2 * thickness,
        width - 2 * thickness,
        soil_height,
        x0 + thickness,
        y0 + thickness,
        ZERO,
        soil_color,
        parent_id=parent_id,
        properties={"complex_type": "garden_soil_fill", "assembly_role": "growing_medium"},
    )

    pitch = 15.5 * INCH
    center_x = x0 + length / 2
    plant_y = y0 + width / 2
    stem_height = 12 * INCH
    crown_radius = 6 * INCH

    for i in range(6):
        px = center_x + (i - 2.5) * pitch
        stem_base_z = soil_height
        stem_top_z = stem_base_z + stem_height
        stem = cylinder_between(
            (px, plant_y, stem_base_z),
            (px, plant_y, stem_top_z),
            0.5 * INCH,
        )
        crown = Sphere(to_mm(crown_radius)).solid().translate((to_mm(px), to_mm(plant_y), to_mm(stem_top_z)))
        plant_shape = stem.fuse(crown)
        builder.add_shape(
            "site",
            f"Raised Garden Bed Plant {i + 1:02d}",
            plant_shape,
            plant_color,
            Dimensions(
                to_mm(2 * crown_radius),
                to_mm(2 * crown_radius),
                to_mm(stem_height + crown_radius),
            ),
            placement=(px - crown_radius, plant_y - crown_radius, stem_base_z),
            parent_id=parent_id,
            properties={"complex_type": "garden_plant", "assembly_role": "plant_vegetation"},
        )
