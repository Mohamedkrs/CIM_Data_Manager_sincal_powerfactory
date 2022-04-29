import cimpy
import importlib


class ManageElements:
    cgmesver = "cgmes_v2_4_15"
    # elems={}

    def __init__(self):
        self.elements = {}
        self.profile_elements = {}
        self.data = []

    def swapEnergySourceWithExternalGrid(self, source, val_name):
        mRID = self.profile_elements[source]
        EquipmentContainer = self.data["topology"][mRID].__dict__[
            "EquipmentContainer"]
        name = self.data["topology"][mRID].name
        shortName = self.data["topology"][mRID].shortName
        description = self.data["topology"][mRID].description
        externalGrid_module = importlib.import_module(
            'cimpy.cgmes_v2_4_15.'+'ExternalNetworkInjection')
        externalGrid_class = getattr(
            externalGrid_module, 'ExternalNetworkInjection')
        externalGrid_class.serializationProfile = {
            'class': 'EQ', 'p': 'SSH', 'q': 'SSH',
            'referencePriority': 'SSH', 'controlEnabled': 'SSH',
            'EquipmentContainer': 'EQ', 'governorSCD': 'EQ',
            'maxP': 'EQ', 'maxQ': 'EQ',
            'maxR0ToX0Ratio': 'EQ', 'maxR1ToX1Ratio': 'EQ',
            'maxZ0ToZ1Ratio': 'EQ', 'minInitialSymShCCurrent': 'EQ',
            'minP': 'EQ', 'minQ': 'EQ', 'minR0ToX0Ratio': 'EQ',
            'minR1ToX1Ratio': 'EQ', 'minZ0ToZ1Ratio': 'EQ',
            'name': 'EQ', 'RegulatingControl': 'EQ'}
        self.data["topology"][mRID] = externalGrid_class(mRID=mRID,
                                                         name=name,
                                                         EquipmentContainer=EquipmentContainer, shortName=shortName, description=description,
                                                         maxP=100000, maxQ=9999, maxInitialSymShCCurrent=15193.4, maxR0ToX0Ratio=0.1, maxR1ToX1Ratio=0.1, maxZ0ToZ1Ratio=1, minInitialSymShCCurrent=12154.7, minR0ToX0Ratio=0.1, minR1ToX1Ratio=0.1, minZ0ToZ1Ratio=1)
        self.profile_elements[val_name] = self.profile_elements.pop(
            source)

    def import_eq_data(self, profile):
        if self.elements:
            self.elements.clear()
        try:
            class_attributes_list = cimpy.cimexport._get_class_attributes_with_references(
                self.data, self.cgmesver)
            eq_classes_list = cimpy.cimexport._sort_classes_to_profile(class_attributes_list, [profile])[0][profile][
                'classes']
        except:
            eq_classes_list = self.data
        for _class in eq_classes_list:
            if 'mRID' in _class:
                if _class['mRID'] not in self.profile_elements.values():
                    if _class['mRID'] not in self.elements.values():
                        if _class['name'] not in self.elements.keys():
                            self.elements[_class['name']] = _class['mRID']
                            i = 1
                        else:
                            self.elements[_class['name'] +
                                          " " + str(i)] = _class['mRID']
                            i += 1
        for key, val in self.elements.items():
            self.profile_elements[key] = val
        return self.elements.keys()

    def filter_data(self, elemName='', elemProp='', detail='', elem_andor_prop='', prop_andor_elem=''):
        filtered_elements = {}
        elem_name_dict = {}
        prop_dict = {}
        detail_dict = {}
        for key, val in self.profile_elements.items():
            if elemName != '':
                if elemName.lower() in key.lower():
                    elem_name_dict[key] = val
            if elemProp != '':
                for k in self.data["topology"][val].__dict__.keys():
                    if elemProp.lower() in k.lower():
                        prop_dict[key] = val
                        break
            if detail != '':
                for v in self.data["topology"][val].__dict__.values():
                    if isinstance(v, (str, int, float, bool)):
                        if detail.lower() in str(v).lower():
                            detail_dict[key] = val
                            break
        if elem_andor_prop == "and" and prop_andor_elem == "and":
            if set(elem_name_dict.keys()) & set(prop_dict.keys()) & set(detail_dict.keys()):
                for item in set(detail_dict.keys()) & set(prop_dict.keys()):
                    filtered_elements[item] = self.profile_elements[item]
        elif elem_andor_prop == "and":
            if set(elem_name_dict.keys()) & set(prop_dict.keys()):
                for item in set(elem_name_dict.keys()) & set(prop_dict.keys()):
                    filtered_elements[item] = self.profile_elements[item]
        elif prop_andor_elem == "and":
            if set(detail_dict.keys()) & set(prop_dict.keys()):
                for item in set(detail_dict.keys()) & set(prop_dict.keys()):
                    filtered_elements[item] = self.profile_elements[item]
        else:
            filtered_elements = {**elem_name_dict, **prop_dict, **detail_dict}
        return filtered_elements.keys()
