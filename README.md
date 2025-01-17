# rhino-python-scripts

### Parametric lampshades for 3D Printing in [RhinoScript](https://developer.rhino3d.com/api/rhinoscript/).

These could also have been done with 🦗 [grasshopper](https://www.grasshopper3d.com/), but Python is easier for me. 🐍

## Examples

[Fibonacci Sphere](fib-sphere.py)  
<img alt="Fibonacci Sphere with 1815 scales" src="https://github.com/caseprince/rhino-python-scripts/blob/master/images/fibonacci-sphere-1815.png" width="70%">

[Ripple Shade](ripple-shade.py)  
<img alt="Ripple Shade" src="https://github.com/caseprince/rhino-python-scripts/blob/master/images/ripple-shade.png" width="70%">

## Setup

1. Clone here: `%APPDATA%\McNeel\Rhinoceros\5.0\scripts\` (\scripts directory may not exist yet)
2. Button commands: `!-RunPythonScript "rhino-python-scropts/ripple-shade.py"`
3. Install recommended extension: RhinoPython

Settings.json to enable `rhinoscriptsyntax` autocomplete in VSC

```json
{
    // disable certain pylint messages
    "python.linting.pylintArgs": [
        "--errors-only",
        "--disable=E0001",
        "--disable=E0401"
    ],
    // python autocomplete extra path
    "python.autoComplete.extraPaths": [
        "C:\\Users\\case.prince\\AppData\\Roaming\\McNeel\\Rhinoceros\\5.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib",
        "C:\\Program Files (x86)\\Rhinoceros 5\\Plug-ins\\IronPython\\Lib",
        "C:\\Users\\case.prince\\AppData\\Roaming\\McNeel\\Rhinoceros\\5.0\\scripts"
    ],

    // enable new language server. THIS IS EXTREMELY IMPORTANT TO HAVE FAST AUTOCOMPLETE!!
    "python.jediEnabled": false,

    // Enable/Disable rhinopython
    "RhinoPython.Enabled": true,
    // True if you want to reset script engine every time you send code, otherwise False
    "RhinoPython.ResetAndRun": false,
    "python.analysis.extraPaths": [
        "C:\\Users\\case.prince\\AppData\\Roaming\\McNeel\\Rhinoceros\\5.0\\Plug-ins\\IronPython (814d908a-e25c-493d-97e9-ee3861957f49)\\settings\\lib",
        "C:\\Program Files (x86)\\Rhinoceros 5\\Plug-ins\\IronPython\\Lib",
        "C:\\Users\\case.prince\\AppData\\Roaming\\McNeel\\Rhinoceros\\5.0\\scripts"
    ]
}
```
