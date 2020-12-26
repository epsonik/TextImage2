class Pred():
    def __init__(self, predicate_id=0, confidence_factor=0, usage_pointer=0, number_of_reference_object=0,
                 number_of_sec_obj_for_relation=0, property_rule_or_rel_number=0, used_in_rules=0):
        self.predicate_id = predicate_id
        self.confidence_factor = confidence_factor
        self.usage_pointer = usage_pointer
        self.number_of_reference_object = number_of_reference_object
        self.number_of_sec_obj_for_relation = number_of_sec_obj_for_relation
        self.property_rule_or_rel_number = property_rule_or_rel_number
        self.used_in_rules = used_in_rules
