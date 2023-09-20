

import re

# Open and read data from test1.txt
with open('test1.txt', 'r') as file:
    data = file.read()

def extract_weapons(text):
    # Split by lines
    lines = text.split("\n")

    # Initialize variables
    weapons_by_type = {}
    current_weapon = None
    current_type = None

    # Types order
    weapon_types_order = [
        "AssaultRifle (Weapon)", "Handgun (Weapon)", "MachineGun (Weapon)", "SniperRifle (Weapon)",
        "SubmachineGun (Weapon)", "RocketLauncher (Weapon)", "Binocular (Item)", "AccessoryBipod (Item)",
        "AccessoryPointer (Item)", "AccessoryMuzzle (Item)", "Uniform (Equipment)", "Headgear (Equipment)",
        "Vest (Equipment)"
    ]

    # Loop through lines
    for line in lines:
        # Check if we're on a weapon line
        match = re.match(r'.*\s+([\w]+) \([\w]+\)', line)
        if match:
            current_weapon = match.group(1)
        
        # Check for type
        for wtype in weapon_types_order:
            if wtype in line:
                current_type = wtype
                break
        
        # Check for the desired config patches
        if ("Config Patch:   rhsusf_c_weapons" in line or "Config Patch:   rhsusf_c_troops" in line) and current_weapon and current_type:
            weapons_by_type.setdefault(current_type, []).append(current_weapon)
            current_weapon = None
            current_type = None

    return weapons_by_type

# Call the function
weapons_by_type = extract_weapons(data)

with open('extractedWeapons.txt', 'w') as output_file:
    for wtype in [
        "AssaultRifle (Weapon)", "Handgun (Weapon)", "MachineGun (Weapon)", "SniperRifle (Weapon)",
        "SubmachineGun (Weapon)", "RocketLauncher (Weapon)", "Binocular (Item)", "AccessoryBipod (Item)",
        "AccessoryPointer (Item)", "AccessoryMuzzle (Item)", "Uniform (Equipment)", "Headgear (Equipment)",
        "Vest (Equipment)"
    ]:
        for weapon in weapons_by_type.get(wtype, []):
            output_file.write(f"{weapon}\n")
with open('extractedTypes.txt', 'w') as output_file:
    for wtype in [
        "AssaultRifle (Weapon)", "Handgun (Weapon)", "MachineGun (Weapon)", "SniperRifle (Weapon)",
        "SubmachineGun (Weapon)", "RocketLauncher (Weapon)", "Binocular (Item)", "AccessoryBipod (Item)",
        "AccessoryPointer (Item)", "AccessoryMuzzle (Item)", "Uniform (Equipment)", "Headgear (Equipment)",
        "Vest (Equipment)"
    ]:
        for weapon in weapons_by_type.get(wtype, []):
            output_file.write(f"{weapon} {wtype}\n")


"""
====================================ARMA 3 Script Below====================================
"""

"""


private _modFolder = configSourceMod (configFile >> "CfgPatches" >> "rhsusf_c_weapons");
private _itemConfigs = "configSourceMod _x isEqualTo _modFolder" configClasses (configFile >> "CfgWeapons");

diag_log text "========== EXPORTING ITEMS ==========";

{
    private _classname = configName _x;
    private _parentClassname = configName inheritsFrom _x;
    private _displayName = getText (_x >> "displayName");

    private _configPatch = configSourceAddonList _x select 0;
    private _scope = ["private", "protected", "public"] select getNumber (_x >> "scope");

    private _author = getText (_x >> "author");
    if !((_x >> "author") in configProperties [_x, "true", false]) then {
        _author = "Error: No author";
    };

    (_classname call BIS_fnc_itemType) params ["_category", "_type"];

    diag_log text "----------";
    diag_log text format ["    %1 (%2)", _classname, _parentClassname];
    diag_log text format ["        Config Patch:   %1", _configPatch];
    diag_log text format ["        Type:           %1 (%2)", _type, _category];
    diag_log text format ["        Display Name:   %1", _displayName];
    diag_log text format ["        Scope:          %1", _scope];
    diag_log text format ["        Author:         %1", _author];

    if (_category isEqualTo "Weapon") then {
        private _optic = getText (_x >> "LinkedItems" >> "LinkedItemsOptic" >> "item");
        if (_optic != "") then {
            diag_log text format ["            Optic:          %1", _optic];
        };

        private _pointer = getText (_x >> "LinkedItems" >> "LinkedItemsAcc" >> "item");
        if (_pointer != "") then {
            diag_log text format ["            Pointer:        %1", _pointer];
        };

        private _silencer = getText (_x >> "LinkedItems" >> "LinkedItemsMuzzle" >> "item");
        if (_silencer != "") then {
            diag_log text format ["            Silencer:       %1", _silencer];
        };

        private _bipod = getText (_x >> "LinkedItems" >> "LinkedItemsUnder" >> "item");
        if (_bipod != "") then {
            diag_log text format ["            Bipod:          %1", _bipod];
        };
    };

    diag_log text "";
} forEach _itemConfigs;

diag_log text "========== EXPORTING ITEMS END ==========";



"""



