from common import *

class BackendOsBridge:
    """Backend for Highway Bridge Design"""
    
    def __init__(self):
        self.module = KEY_DISP_FINPLATE
        self.design_status = False
        self.design_button_status = False
        
    def module_name(self):
        return KEY_DISP_FINPLATE
    
    def input_values(self):
        """Return list of input fields for the UI"""
        options_list = []

        t1 = (KEY_MODULE, KEY_DISP_FINPLATE, TYPE_MODULE, None, True, 'No Validator')
        options_list.append(t1)

        # Type of Structure section
        t2 = (None, DISP_TITLE_STRUCTURE, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_STRUCTURE_TYPE, KEY_DISP_STRUCTURE_TYPE, TYPE_COMBOBOX, VALUES_STRUCTURE_TYPE, True, 'No Validator')
        options_list.append(t3)

        # Project Location section
        t4 = (None, DISP_TITLE_PROJECT, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_PROJECT_LOCATION, KEY_DISP_PROJECT_LOCATION, TYPE_COMBOBOX, VALUES_PROJECT_LOCATION, True, 'No Validator')
        options_list.append(t5)

        # Geometric Details section
        t6 = (None, DISP_TITLE_GEOMETRIC, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t6)

        t7 = (KEY_SPAN, KEY_DISP_SPAN, TYPE_TEXTBOX, None, True, 'Double Validator')
        options_list.append(t7)

        t8 = (KEY_CARRIAGEWAY_WIDTH, KEY_DISP_CARRIAGEWAY_WIDTH, TYPE_TEXTBOX, None, True, 'Double Validator')
        options_list.append(t8)

        t9 = (KEY_FOOTPATH, KEY_DISP_FOOTPATH, TYPE_COMBOBOX, VALUES_FOOTPATH, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_SKEW_ANGLE, KEY_DISP_SKEW_ANGLE, TYPE_TEXTBOX, None, True, 'Double Validator')
        options_list.append(t10)

        # Material Inputs section
        t11 = (None, DISP_TITLE_MATERIAL, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_GIRDER, KEY_DISP_GIRDER, TYPE_COMBOBOX, connectdb("Material"), True, 'No Validator')
        options_list.append(t12)

        t13 = (KEY_CROSS_BRACING, KEY_DISP_CROSS_BRACING, TYPE_COMBOBOX, connectdb("Material"), True, 'No Validator')
        options_list.append(t13)

        t14 = (KEY_DECK, KEY_DISP_DECK, TYPE_COMBOBOX, connectdb("Material"), True, 'No Validator')
        options_list.append(t14)

        t15 = (KEY_DECK_CONCRETE_GRADE_BASIC, KEY_DISP_DECK_CONCRETE_GRADE, TYPE_COMBOBOX, VALUES_DECK_CONCRETE_GRADE, True, 'No Validator')
        options_list.append(t15)

        return options_list
    
    def customized_input(self):
        """Return empty list for now"""
        return []
    
    def input_value_changed(self):
        """Return None - no dynamic changes needed"""
        return None
    
    def set_osdaglogger(self, key):
        """Mock logger setup"""
        print("Logger set up (mock)")
    
    def output_values(self, flag):
        """Mock output values"""
        return []
    
    def func_for_validation(self, design_inputs):
        """Validate user inputs according to IRC 5 specifications"""
        errors = []
        
        # Validate Span
        if KEY_SPAN in design_inputs:
            try:
                span = float(design_inputs[KEY_SPAN])
                if span < SPAN_MIN or span > SPAN_MAX:
                    errors.append(f"Span must be between {SPAN_MIN} m and {SPAN_MAX} m. Current value: {span} m")
            except (ValueError, TypeError):
                errors.append("Span must be a valid number")
        
        # Validate Carriageway Width
        if KEY_CARRIAGEWAY_WIDTH in design_inputs:
            try:
                width = float(design_inputs[KEY_CARRIAGEWAY_WIDTH])
                if width < CARRIAGEWAY_WIDTH_MIN:
                    errors.append(f"Carriageway Width must be at least {CARRIAGEWAY_WIDTH_MIN} m as per IRC 5 Clause 104.3.1. Current value: {width} m")
            except (ValueError, TypeError):
                errors.append("Carriageway Width must be a valid number")
        
        # Validate Skew Angle
        if KEY_SKEW_ANGLE in design_inputs:
            try:
                angle = float(design_inputs[KEY_SKEW_ANGLE])
                if angle < SKEW_ANGLE_MIN or angle > SKEW_ANGLE_MAX:
                    errors.append(f"Skew Angle must be between {SKEW_ANGLE_MIN}° and {SKEW_ANGLE_MAX}°. IRC 24 (2010) requires detailed analysis when skew angle exceeds ±15 degrees. No calculations will be performed. Current value: {angle}°")
            except (ValueError, TypeError):
                errors.append("Skew Angle must be a valid number")
        
        if errors:
            return "\n".join(errors)
        return None
    
    def get_3d_components(self):
        """Mock 3D components"""
        return []