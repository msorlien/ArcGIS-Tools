import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Date Tools"
        self.alias = "datetools"
        self.description = """
                        This toolbox contains a series of tools for changing the way dates are formatted in fields. 
                        
                        MIT License
                        
                        Copyright (c) 2019 Mariel Sorlien

                        Permission is hereby granted, free of charge, to any person obtaining a copy
                        of this software and associated documentation files (the "Software"), to deal
                        in the Software without restriction, including without limitation the rights
                        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                        copies of the Software, and to permit persons to whom the Software is
                        furnished to do so, subject to the following conditions:
                        
                        The above copyright notice and this permission notice shall be included in all
                        copies or substantial portions of the Software.
                        
                        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                        SOFTWARE."""

        # List of tool classes associated with this toolbox
        self.tools = [ClipDate, DateFormat, DateConvert, DateConvert2]

class ClipDate(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Clip to Date Range"
        self.description = "Selects all objects within date range and generates new shapefile. All dates must be in YYYYMMDD format."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        inputFile = arcpy.Parameter(name="inputFile",
                                     displayName="Input",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(inputFile)
        column_name = arcpy.Parameter(name="column_name",
                                        displayName="Column Name",
                                        datatype="Field",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        column_name.parameterDependencies = [inputFile.name]
        params.append(column_name)
        startDate = arcpy.Parameter(name="startDate",
                                        displayName="Start Date",
                                        datatype="GPLong",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        params.append(startDate)
        endDate = arcpy.Parameter(name="endDate",
                                    displayName="End Date",
                                    datatype="GPLong",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Input",  # Input|Output
                                    )
        params.append(endDate)
        outputFile = arcpy.Parameter(name="outputFile",
                                 displayName="Output",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        outputFile.parameterDependencies = [inputFile.name]
        outputFile.schema.clone = True
        params.append(outputFile)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFile = parameters[0].valueAsText
        columnName = parameters[1].valueAsText
        startDate = parameters[2].valueAsText
        endDate = parameters[3].valueAsText
        outputFile = parameters[4].valueAsText


        # select layer by attribute
        # https://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/select-layer-by-attribute.htm

        expression = '"' + columnName + '" >= ' + str(startDate) + ' AND "' + columnName + '" <= ' + str(
            endDate)

        arcpy.AddMessage("Selecting date range...")
        arcpy.MakeFeatureLayer_management(inputFile, "dateselect")
        arcpy.SelectLayerByAttribute_management("dateselect", "NEW_SELECTION", expression)
        arcpy.AddMessage("Generating new file...")
        arcpy.CopyFeatures_management("dateselect", outputFile)
        return

class DateFormat(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Change Date Format"
        self.description = "Converts dates between MMDDYYY, DDMMYYYY, and YYYYMMDD formats."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        inputFile = arcpy.Parameter(name="inputFile",
                                     displayName="Input",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(inputFile)
        column_name = arcpy.Parameter(name="ColumnName",
                                        displayName="Field Name",
                                        datatype="Field",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        column_name.parameterDependencies = [inputFile.name]
        params.append(column_name)
        dateFormat = arcpy.Parameter(name="dateFormat",
                                      displayName="Current Date Format",
                                      datatype="GPString",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Input",  # Input|Output
                                      )
        dateFormat.filter.list = ["DDMMYYYY", "MMDDYYYY", "YYYYMMDD"]
        params.append(dateFormat)
        dateFormat2 = arcpy.Parameter(name="dateFormat2",
                                     displayName="Desired Date Format",
                                     datatype="GPString",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        dateFormat2.filter.type = "ValueList"
        dateFormat2.filter.list = ["DDMMYYYY", "MMDDYYYY", "YYYYMMDD"]
        params.append(dateFormat2)
        outputFile = arcpy.Parameter(name="output",
                                     displayName="Output",
                                     datatype="DEFeatureClass",
                                     parameterType="Derived",  # Required|Optional|Derived
                                     direction="Output",  # Input|Output
                                     )
        outputFile.parameterDependencies = [inputFile.name]
        outputFile.schema.clone = True
        params.append(outputFile)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFile = parameters[0].valueAsText
        columnName = parameters[1].valueAsText
        inputFormat = parameters[2].valueAsText
        outputFormat = parameters[3].valueAsText

        # Update cursor
        # https://pro.arcgis.com/en/pro-app/arcpy/functions/updatecursor.htm

        if inputFormat == outputFormat:
            arcpy.AddWarning("No change requested")
        else:
            arcpy.AddMessage("Updating date format")

            linecount = 0

            cursor = arcpy.UpdateCursor(inputFile)
            for row in cursor:
                date = str(row.getValue(columnName))

                if len(date) < 8:
                    dropcount = 8 - len(date)
                    arcpy.AddMessage("Reapplying " + str(dropcount) + " dropped 0 on line " + str(linecount))
                    while dropcount > 0:
                        date = "0" + str(date)
                        dropcount -= 1
                elif len(date) > 8:
                    arcpy.AddError("Error on line " + str(linecount))

                if inputFormat == "YYYYMMDD":
                    date1 = date
                elif inputFormat == "MMDDYYYY":
                    date1 = date[4:8] + date[0:2] + date[2:4]
                elif inputFormat == "DDMMYYYY":
                    date1 = date[4:8] + date[2:4] + date[0:2]

                if outputFormat == "YYYYMMDD":
                    date2 = date1
                elif outputFormat == "MMDDYYYY":
                    date2 = date1[4:6] + date1[6:8] + date1[0:4]
                elif outputFormat == "DDMMYYYY":
                    date2 = date1[6:8] + date1[4:6] + date1[0:4]

                row.setValue(columnName, date2)
                cursor.updateRow(row)
                linecount += 1
        return

class DateConvert(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Integer to Date"
        self.description = "Copies dates from selected YYYYMMDD long/short field and adds them to new date field."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        inputFile = arcpy.Parameter(name="inputFile",
                                displayName="Input",
                                datatype="DEFeatureClass",
                                parameterType="Required",  # Required|Optional|Derived
                                direction="Input",  # Input|Output
                                )
        params.append(inputFile)
        column_name = arcpy.Parameter(name="ColumnName",
                                      displayName="Existing Column",
                                      datatype="Field",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Input",  # Input|Output
                                      )
        column_name.parameterDependencies = [inputFile.name]
        params.append(column_name)
        column_name2 = arcpy.Parameter(name="ColumnName2",
                                      displayName="New Column",
                                      datatype="GPString",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Input",  # Input|Output
                                      )
        params.append(column_name2)
        outputFile = arcpy.Parameter(name="outputFile",
                                     displayName="Output",
                                     datatype="DEFeatureClass",
                                     parameterType="Derived",  # Required|Optional|Derived
                                     direction="Output",  # Input|Output
                                     )
        params.append(outputFile)
        outputFile.parameterDependencies = [inputFile.name]
        outputFile.schema.clone = True
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFile = parameters[0].valueAsText
        columnName = parameters[1].valueAsText
        outputColumn = parameters[2].valueAsText

        # add column
        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm
        arcpy.AddMessage("Adding new field")
        arcpy.AddField_management(inputFile, outputColumn, "DATE")

        # dump info in new column
        arcpy.AddMessage("Updating new field")
        linecount = 0

        cursor = arcpy.UpdateCursor(inputFile)
        for row in cursor:
            date = str(row.getValue(columnName))

            if len(date) < 8:
                dropcount = 8 - len(date)
                arcpy.AddMessage("Reapplying " + str(dropcount) + "dropped 0 to date on line " + str(linecount))
                while dropcount > 0:
                    date = "0" + str(date)
                    dropcount -= 1
            elif len(date) > 8:
                arcpy.AddError("Error on line " + str(linecount))

            newdate = date[0:4] + "-" + date[4:6] + "-" + date[6:8]

            row.setValue(outputColumn, newdate)
            cursor.updateRow(row)
            linecount += 1
        return

class DateConvert2(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Date to Integer"
        self.description = "Copies dates from selected date field and adds them to new YYYYMMDD long/short field."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        inputFile = arcpy.Parameter(name="inputFile",
                                displayName="Input",
                                datatype="DEFeatureClass",
                                parameterType="Required",  # Required|Optional|Derived
                                direction="Input",  # Input|Output
                                )
        params.append(inputFile)
        column_name = arcpy.Parameter(name="ColumnName",
                                      displayName="Existing Column",
                                      datatype="Field",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Input",  # Input|Output
                                      )
        column_name.parameterDependencies = [inputFile.name]
        params.append(column_name)
        column_name2 = arcpy.Parameter(name="ColumnName2",
                                      displayName="New Column",
                                      datatype="GPString",
                                      parameterType="Required",  # Required|Optional|Derived
                                      direction="Input",  # Input|Output
                                      )
        params.append(column_name2)
        outputFile = arcpy.Parameter(name="outputFile",
                                     displayName="Output",
                                     datatype="DEFeatureClass",
                                     parameterType="Derived",  # Required|Optional|Derived
                                     direction="Output",  # Input|Output
                                     )
        params.append(outputFile)
        outputFile.parameterDependencies = [inputFile.name]
        outputFile.schema.clone = True
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inputFile = parameters[0].valueAsText
        columnName = parameters[1].valueAsText
        outputColumn = parameters[2].valueAsText

        # add column
        # https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm
        arcpy.AddMessage("Adding new field")
        arcpy.AddField_management(inputFile, outputColumn, "LONG",12)

        # dump info in new column
        arcpy.AddMessage("Updating new field")

        cursor = arcpy.UpdateCursor(inputFile)
        for row in cursor:
            date = str(row.getValue(columnName))

            date2 = date.replace("-","")
            newdate = date2[0:8]

            row.setValue(outputColumn, newdate)
            cursor.updateRow(row)
        return