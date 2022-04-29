import importlib

pf_profiles = {'DY': ['http://entsoe.eu/CIM/Dynamics/3/1'], 'EQ': ['http://entsoe.eu/CIM/EquipmentCore/3/1',
                                                                   'http://entsoe.eu/CIM/EquipmentOperation/3/1', 'http://entsoe.eu/CIM/EquipmentShortCircuit/3/1'],
               'GL': ['http://entsoe.eu/CIM/GeographicalLocation/2/1'], 'SSH': ['http://entsoe.eu/CIM/SteadyStateHypothesis/1/1'],
               'TP': ['http://entsoe.eu/CIM/Topology/4/1'], 'DL': ['http://entsoe.eu/CIM/DiagramLayout/3/1'],
               'SV': ['http://entsoe.eu/CIM/StateVariables/4/1']}  # Profiles accepted by PF


def sincal_Pf(import_result):
    import_result['meta_info']['namespaces'] = adjust_namespaces(
        import_result['meta_info']['namespaces'])
    import_result["meta_info"]['profiles'] = adjust_profiles(
        import_result["meta_info"]['profiles'], pf_profiles)
    add_dependentOn(import_result)
    add_missingProperties(import_result, op_limittType_mRID(import_result))
    return import_result


def add_missingProperties(import_result, ls):
    counter = 0
    for mRID, value in import_result['topology'].items():
        ####################################Add properties to synch machines####################################
        if "SynchronousMachineTimeConstantReactance" == import_result['topology'][mRID].__class__.__name__:
            if "modelType" in import_result['topology'][mRID].__dict__.keys().__str__() and import_result['topology'][mRID].__dict__["modelType"] is None:
                import_result['topology'][mRID].__dict__[
                    'modelType'] = "%URL%http://iec.ch/TC57/2013/CIM-schema-cim16#SynchronousMachineModelKind.subtransient"
            if "rotorType" in import_result['topology'][mRID].__dict__.keys().__str__() and import_result['topology'][mRID].__dict__["rotorType"] is None:
                import_result['topology'][mRID].__dict__[
                    'rotorType'] = "%URL%http://iec.ch/TC57/2013/CIM-schema-cim16#RotorKind.roundRotor"
            if import_result['topology'][mRID].__dict__['inertia'] == 0:
                import_result['topology'][mRID].__dict__['inertia'] = 4
        # add names to properties
        elif "ControlAreaGeneratingUnit" in import_result['topology'][mRID].__class__.__name__:
            import_result['topology'][mRID].__dict__['name'] = "CAGU"+mRID[:5]
        elif "TapChangerControl" in import_result['topology'][mRID].__class__.__name__:
            import_result['topology'][mRID].__dict__['name'] = "TCC"+mRID[:5]
        # filter out
        elif "PowerTransformer" == import_result['topology'][mRID].__class__.__name__:
            if import_result['topology'][mRID].__dict__['beforeShortCircuitAnglePf'] == 0.0:
                import_result['topology'][mRID].__dict__[
                    'beforeShortCircuitAnglePf'] = None
            if import_result['topology'][mRID].__dict__['highSideMinOperatingU'] == 0:
                import_result['topology'][mRID].__dict__[
                    'highSideMinOperatingU'] = None
            if import_result['topology'][mRID].__dict__['beforeShCircuitHighestOperatingCurrent'] == 0.0:
                import_result['topology'][mRID].__dict__[
                    'beforeShCircuitHighestOperatingCurrent'] = None
            if import_result['topology'][mRID].__dict__['beforeShCircuitHighestOperatingVoltage'] == 0:
                import_result['topology'][mRID].__dict__[
                    'beforeShCircuitHighestOperatingVoltage'] = None


def op_limittType_mRID(import_result):  # get the mRID for "OperationalLimitType"
    ls = []
    for mRID, value in import_result['topology'].items():
        if value.__class__.__name__ == "OperationalLimitType":
            ls.append(value.__dict__["mRID"])

    return ls


def adjust_profiles(profiles, pf_profile):  # adding PF accepted namespaces
    newprofile = {}
    for profile in profiles.keys():
        for pfprofile in pf_profile.keys():
            if profile == pfprofile:
                newprofile[pfprofile] = pf_profile[pfprofile]
    return newprofile


def adjust_namespaces(namespaces_dict):  # Adjust namespace to PF
    namespaces = {}
    namespaces_PF = ["rdf", "entsoe", "cim", "md"]
    for key, value in namespaces_dict.items():
        if key in namespaces_PF:
            namespaces[key] = value
    return namespaces


def add_dependentOn(import_result):  # TO DO
    profiledepON = {"TP": ["EQ"], "SV": ["TP", "SSH"], "SSH": ["EQ"], "DY": [
        "EQ"], "DL": ["EQ", "TP"], "GL": ["TP", "EQ"]}  # which profile depends on which
    if "DependentOn" not in import_result['meta_info']['profile_about'].keys():
        import_result['meta_info']['profile_about']["DependentOn"] = {}
        for key, value in profiledepON.items():
            if key not in import_result['meta_info']['profile_about']['DependentOn'] and key in import_result['meta_info']['profile_about'].keys():
                import_result['meta_info']['profile_about']['DependentOn'][key] = {}
                import_result['meta_info']['profile_about']['DependentOn'][key]["resource"] = [
                ]
                for v in value:
                    if v in import_result['meta_info']['profile_about'].keys():
                        import_result['meta_info']['profile_about']['DependentOn'][key]["resource"].append(
                            import_result["meta_info"]["profile_about"][v])
