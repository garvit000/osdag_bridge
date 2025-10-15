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
KEY_DISP_PROJECT_LOCATION = "City in India*"
DISP_TITLE_GEOMETRIC = "Geometric Details"
KEY_DISP_SPAN = "Span (m)* [20-45]"
KEY_DISP_CARRIAGEWAY_WIDTH = "Carriageway Width (m)* [≥4.25]"
KEY_DISP_FOOTPATH = "Footpath (Default: None)"
KEY_DISP_SKEW_ANGLE = "Skew Angle (degrees) [≤30, Default: 0]"
DISP_TITLE_MATERIAL = "Material Inputs"
KEY_DISP_GIRDER = "Girder"
KEY_DISP_CROSS_BRACING = "Cross Bracing"
KEY_DISP_DECK = "Deck"

# Sample values
# Type of Structure: Defines the application of the steel girder bridge
# Currently only covers highway bridge
VALUES_STRUCTURE_TYPE = ["Highway Bridge", "Other"]

# Project Location: Cities in India for load calculations
# Organized by regions for easier navigation
VALUES_PROJECT_LOCATION = [
    "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad",
    "Ahmedabad", "Pune", "Surat", "Jaipur", "Lucknow", "Kanpur",
    "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad",
    "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik",
    "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivali", "Vasai-Virar", "Varanasi",
    "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad",
    "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada",
    "Jodhpur", "Madurai", "Raipur", "Kota", "Chandigarh", "Guwahati",
    "Custom"  # Allow custom location entry
]

# Footpath: Left or right edge or none or both
# Default: None
# Note: IRC 5 Clause 101.41 requires safety kerb when footpath is not present
VALUES_FOOTPATH = ["None", "Left Edge", "Right Edge", "Both Edges"]

VALUES_MATERIAL = ["E250 (Fe 410W)A", "E300 (Fe 440)", "E350 (Fe 490)", "E410 (Fe 540)", "E450 (Fe 570)", "E550 (Fe 650)"]

# Validation limits
# Span: Between 20 to 45 meters
SPAN_MIN = 20.0
SPAN_MAX = 45.0

# Carriageway Width: Minimum 4.25 m as per IRC 5 Clause 104.3.1
CARRIAGEWAY_WIDTH_MIN = 4.25

# Skew Angle: IRC 5 Clause 105.3.3 recommends <= 30 degrees
# Default: 0 degrees
SKEW_ANGLE_MIN = 0.0
SKEW_ANGLE_MAX = 30.0
SKEW_ANGLE_DEFAULT = 0.0

def connectdb(table_name, popup=None):
    """Mock database connection - returns sample data"""
    if table_name == "Material":
        return VALUES_MATERIAL
    return []