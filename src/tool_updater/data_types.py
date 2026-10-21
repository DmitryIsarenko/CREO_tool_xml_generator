"""Describe initialized tool data and catalog integration boundaries."""

from typing import Any, TypedDict


# Catalog families have different nested layouts (including insert catalogs).
# Keep dynamic typing at this legacy JSON boundary, not in computed tool data.
type Catalog = dict[str, Any]
type CutParameters = dict[str, float | str]
type CuttingData = dict[str, dict[str, CutParameters]]


class ToolData(TypedDict, total=False):
    """Describe parameters populated during tool initialization."""

    tool_name_str: str
    tool_name_for_geom_catalogue: str
    tool_name_for_cut_catalogue: float | str
    tool_name_for_xml: str
    tool_diam_float: float
    file_name_prefix: str
    file_name_suffix: str
    file_name: str
    tool_type: str
    cut_data_diam_group: str
    cut_data: CuttingData
    len_out_of_holder: float
    GAUGE_X_LENGTH: str
    GAUGE_Z_LENGTH: str
    COMP_OVERSIZE: str
    LENGTH_UNITS: str
    TOOL_LONG_FLAG: str
    SPINDLE_SENSE: str
    COOLANT_OPTION: str
    COOLANT_PRESSURE: str
    TOOL_MATERIAL: str
    TOOL_COMMENT: str
    CUTTER_DIAM: float | str
    NUM_OF_TEETH: int
    HOLDER_DIA: float
    HOLDER_LEN: float | str
    LENGTH: float
    FLUTE_LENGTH: float
    CORNER_RADIUS: float | str | None
    DRILL_DIAMETER: float | None
    DRILL_LENGTH: float | None
    POINT_ANGLE: float | None
    CSINK_ANGLE: float | None
    SIDE_ANGLE: float | None
    INSERT_LENGTH: float | None
    END_OFFSET: float | None
    SHANK_DIAM: float | None
    CHAMFER_LENGTH: float | None
    CUT_LENGTH: float | None
    TIP_LENGTH: float | None
    CUTTER_WIDTH: str
    CORNER_CHAMFER: str
    CORNER_CHAMFER_ANGLE: str


class MaterialModifiers(TypedDict):
    """Describe coefficients for a derived material group."""

    from_iso: str
    k_Vc: float
    k_Ae: float
    k_Ap: float
    k_Fz: float
