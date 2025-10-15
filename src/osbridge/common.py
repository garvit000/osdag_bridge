# Constants for input types
TYPE_MODULE = "module"
TYPE_TITLE = "title"
TYPE_COMBOBOX = "combobox"
TYPE_COMBOBOX_CUSTOMIZED = "combobox_customized"
TYPE_TEXTBOX = "textbox"
TYPE_IMAGE = "image"

# Keys for inputs
KEY_MODULE = "Module"
KEY_STRUCTURE_TYPE = "Structure Type"
KEY_PROJECT_LOCATION = "Project Location"
KEY_SPAN = "Span"
KEY_CARRIAGEWAY_WIDTH = "Carriageway Width"
KEY_FOOTPATH = "Footpath"
KEY_SKEW_ANGLE = "Skew Angle"
KEY_GIRDER = "Girder"
KEY_CROSS_BRACING = "Cross Bracing"
KEY_DECK = "Deck"

# Display names
KEY_DISP_FINPLATE = "Highway Bridge Design"
DISP_TITLE_STRUCTURE = "Type of Structure"
KEY_DISP_STRUCTURE_TYPE = "Structure Type"
DISP_TITLE_PROJECT = "Project Location"
KEY_DISP_PROJECT_LOCATION = "Project Location"
DISP_TITLE_GEOMETRIC = "Geometric Details"
KEY_DISP_SPAN = "Span (m):"
KEY_DISP_CARRIAGEWAY_WIDTH = "Carriageway Width (m):"
KEY_DISP_FOOTPATH = "Footpath"
KEY_DISP_SKEW_ANGLE = "Skew Angle (degrees):"
DISP_TITLE_MATERIAL = "Material Inputs"
KEY_DISP_GIRDER = "Girder"
KEY_DISP_CROSS_BRACING = "Cross Bracing"
KEY_DISP_DECK = "Deck"

# Sample values
VALUES_STRUCTURE_TYPE = ["Simply Supported Bridge", "Continuous Bridge", "Cable-Stayed Bridge", "Arch Bridge"]
VALUES_PROJECT_LOCATION = ["Location 1", "Location 2", "Location 3"]
VALUES_FOOTPATH = ["None", "One Side", "Both Sides"]
VALUES_MATERIAL = ["E250 (Fe 410W)A", "E300 (Fe 440)", "E350 (Fe 490)", "E410 (Fe 540)", "E450 (Fe 570)", "E550 (Fe 650)"]

def connectdb(table_name, popup=None):
    """Mock database connection - returns sample data"""
    if table_name == "Material":
        return VALUES_MATERIAL
    return []