# Constants for input types
TYPE_MODULE = "module"
TYPE_TITLE = "title"
TYPE_COMBOBOX = "combobox"
TYPE_COMBOBOX_CUSTOMIZED = "combobox_customized"
TYPE_TEXTBOX = "textbox"
TYPE_IMAGE = "image"

# Keys for inputs
KEY_MODULE = "Module"
KEY_CONN = "Connectivity"
KEY_IMAGE = "Image"
KEY_SUPTNGSEC = "Column Section"
KEY_SUPTDSEC = "Beam Section"
KEY_MATERIAL = "Material"
KEY_SHEAR = "Shear Force"
KEY_AXIAL = "Axial Force"
KEY_D = "Bolt Diameter"
KEY_TYP = "Bolt Type"
KEY_GRD = "Bolt Grade"
KEY_PLATETHK = "Plate Thickness"

# Display names
KEY_DISP_FINPLATE = "Fin Plate Connection"
DISP_TITLE_CM = "Connection Properties"
KEY_DISP_CONN = "Connectivity"
KEY_DISP_COLSEC = "Column Section"
KEY_DISP_BEAMSEC = "Beam Section"
KEY_DISP_MATERIAL = "Material"
DISP_TITLE_FSL = "Load Details"
KEY_DISP_SHEAR = "Shear Force (kN)"
KEY_DISP_AXIAL = "Axial Force (kN)"
DISP_TITLE_BOLT = "Bolt Details"
KEY_DISP_D = "Diameter (mm)"
KEY_DISP_TYP = "Type"
KEY_DISP_GRD = "Grade"
DISP_TITLE_PLATE = "Plate Details"
KEY_DISP_PLATETHK = "Thickness (mm)"

# Sample values
VALUES_CONN = ["Column flange-Beam web", "Column web-Beam web"]
VALUES_MATERIAL = ["E250 (Fe 410W)A", "E300 (Fe 440)", "E350 (Fe 490)", "E410 (Fe 540)", "E450 (Fe 570)", "E550 (Fe 650)"]
VALUES_D = ["All", "Customized"]
VALUES_TYP = ["Bearing Bolt", "Friction Grip Bolt"]
VALUES_GRD = ["All", "Customized"]
VALUES_PLATETHK = ["All", "Customized"]


def connectdb(table_name, popup=None):
    """Mock database connection - returns sample data"""
    if table_name == "Columns":
        return ["UC 305x305x240", "UC 305x305x198", "UC 305x305x158", "UC 254x254x167"]
    elif table_name == "Beams":
        return ["UB 914x419x388", "UB 914x305x289", "UB 838x292x226", "UB 762x267x197"]
    elif table_name == "Material":
        return VALUES_MATERIAL
    return []