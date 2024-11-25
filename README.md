## **Weight Calculator Add-on for Blender**

###
**Introducing.**

Are you a designer, engineer, or architect looking to estimate the weight of your 3D models accurately? Look no further! The **Weight Calculator Add-on** for Blender is here to help.

**Overview**

The **Weight Calculator Add-on** is a powerful tool designed to help Blender users calculate the weight of selected mesh objects based on their material properties. This add-on is particularly useful for engineers, architects, and designers who need to estimate the weight of 3D models for construction, mechanical manufacturing, and other applications. This add-on supports a wide range of materials and provides options for custom density and volume inputs, making it versatile for various applications.

#### **Key Features**

* **Wide Range of Materials**: Choose from a variety of common materials used in construction and mechanical manufacturing, including metals, plastics, and more.
* **Custom Density Input**: For materials not listed, input a custom density value to get precise weight calculations.
* **User-Friendly Interface**: A simple and intuitive panel in the 3D Viewport makes it easy to select materials and calculate weights.
* **Solid Mesh Verification**: The add-on ensures that only solid mesh objects are considered, providing accurate results.

#### **Features**

* **Material Selection**: Choose from a wide range of common materials used in construction and mechanical manufacturing.
* **Custom Density and Volume**: Optionally input a custom density and volume values for materials not listed in the default selection.
* **Solid Mesh Verification**: Ensures that only solid mesh objects are considered for weight calculation.
* **Volume Calculation**: Accurately calculates the volume of the selected mesh objects.
* **Weight Calculation**: Computes the weight of the selected objects based on their volume and material density.
* **User-Friendly Interface**: Easy-to-use panel in the 3D Viewport for selecting materials and calculating weights.
* **Unit System Support**: Supports both Metric and Imperial unit systems.
* **Error Handling**: Provides informative error messages for better user experience.

#### **Supported Materials**

* **Metals**: Iron, Steel, Stainless Steel, Aluminum, Copper, Brass, Bronze, Titanium, Gold, Silver, Lead, Zinc, Magnesium, Nickel, Uranium, Mercury
* **Non-Metals**: Plastic, Wood, Concrete, Glass, Brick, Marble, Granite, Carbon Fiber, Foam, Rubber, Diamond

#### **Installation**

1. **Download the Add-on**:
  * Download the `weight_calculator_addon.py` file from the provided source.
2. **Install the Add-on**:
  * Open Blender.
  * Go to `Edit > Preferences` (or press `F4` and then `P`).
  * Navigate to the `Add-ons` tab.
  * Click on `Install` at the top left corner.
  * Select the `weight_calculator.py` file and click `Install Add-on`.
3. **Enable the Add-on**:
  * In the `Add-ons` tab, search for "Weight Calculator".
  * Check the box next to "Weight Calculator Add-on" to enable it.

#### **Usage**

1. **Open the Weight Calculator Panel**:
  * In the 3D Viewport, go to the `Tool` tab in the right-hand side panel.
  * Scroll down to find the "Weight Calculator" section.
2. **Select a Material**:
  * From the "Material Type" dropdown menu, select the material of the object you want to calculate the weight for.
3. **Use Custom Density (Optional)**:
  * If the material you need is not listed, check the "Use Custom Density" checkbox.
  * Enter the custom density value in the "Density (kg/m³)" field.
4. **Use Custom Volume (Optional)**: Check this box to input a custom volume value.
  * Enter the custom volume value in the "Volume (m³)" field.
5. **Length Unit**: Select the length unit (Millimeters, Centimeters, Meters, Inches, Feet).
6. **Select Objects**:
  * Select one or more mesh objects in the 3D Viewport.
7. **Calculate Weight**:
  * Click the "`Calculate Weight`" button.
  * The add-on will compute the total weight of the selected objects and display the result in the Info area at the bottom of the Blender window.
8. **Calculate Volume**:
  * Click the "`Calculate Volume"` button to compute the total volume of the selected objects.
  * The result will be displayed in the Info bar at the bottom of the Blender window.

#### **Example Usage**

1. **Select a Mesh Object**:
  * In the 3D Viewport, select a mesh object (e.g., a cube).
2. **Choose a Material**:
  * In the "Weight Calculator" panel, select "Aluminum" from the "Material Type" dropdown menu.
3. **Calculate Weight**:
  * Click the "Calculate Weight" button.
  * The add-on will display the total weight of the selected object in the Info area.
4. **Calculate Volume**:
  * Click the `Calculate Volume` button to compute the total volume of the selected objects.
  * The result will be displayed in the Info bar at the bottom of the Blender window.

#### **Troubleshooting**

* **No Object Selected**:
  * Ensure that at least one mesh object is selected in the 3D Viewport.
* **Non-Solid Mesh**:
  * The add-on only calculates the weight of solid mesh objects. Ensure that the selected objects are solid and do not have non-planar or split faces.
* **Custom Density Not Applied**:
  * If you are using a custom density, make sure the "Use Custom Density" checkbox is checked and the density value is entered correctly.

#### **License**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.
