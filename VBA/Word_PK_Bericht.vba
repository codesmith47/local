Private Sub Document_ContentControlOnExit(ByVal ContentControl As ContentControl, Cancel As Boolean)
    If ContentControl.Title = "Startdatum" Or ContentControl.Title = "Enddatum" Then
        ' Get the selected date from the "Startdatum" content control
        Dim startDateString As String
        startDateString = ActiveDocument.SelectContentControlsByTitle("Startdatum").Item(1).Range.Text
        
        ' Get the selected date from the "Enddatum" content control
        Dim endDatePicker As ContentControl
        Set endDatePicker = ActiveDocument.SelectContentControlsByTitle("Enddatum").Item(1)
        Dim endDateString As String
        endDateString = endDatePicker.Range.Text
        
        ' Convert the selected dates to Date values
        Dim startDate As Date
        Dim endDate As Date
        startDate = CDate(ConvertGermanDate(startDateString))
        endDate = CDate(ConvertGermanDate(endDateString))
        
        ' Compare the selected dates and cancel if Startdatum is after Enddatum
        If startDate > endDate Then
            MsgBox "Das Startdatum muss vor dem Enddatum liegen.", vbCritical, "Fehlerhafte Eingabe"
            Cancel = True
        Else
            ' Run the table adjustment script regardless of the content control
            AdjustTableRowCount
        End If
    End If
End Sub

Sub AdjustTableRowCount()
    Application.LanguageSettings.LanguageID(msoLanguageIDUI) = 1031 ' Set the UI language to German
    Application.LanguageSettings.LanguageID(msoLanguageIDUI) = 7 ' Set the locale to German
    
    ' Get the start and end dates from the date picker content controls
    Dim startDatePicker As ContentControl
    Dim endDatePicker As ContentControl
    Set startDatePicker = ActiveDocument.SelectContentControlsByTitle("Startdatum").Item(1)
    Set endDatePicker = ActiveDocument.SelectContentControlsByTitle("Enddatum").Item(1)
    
    ' Get the start and end dates as formatted strings
    Dim startDateString As String
    Dim endDateString As String
    startDateString = startDatePicker.Range.Text
    endDateString = endDatePicker.Range.Text
    
    ' Convert the formatted strings to dates in the German locale
    Dim startDate As Date
    Dim endDate As Date
    startDate = ConvertGermanDate(startDateString)
    endDate = ConvertGermanDate(endDateString)
    
    ' Calculate the number of days between the start and end dates
    Dim numDays As Long
    numDays = DateDiff("d", startDate, endDate)
    
    ' Set the table object
    Dim tbl As Table
    Set tbl = ActiveDocument.Tables(1) ' Assuming the table is the first table in the document
    
    ' Adjust the row count based on the number of days
    Dim targetRowCount As Long
    targetRowCount = numDays + 1 ' Add 1 to include the header row
    
    If targetRowCount < tbl.Rows.Count Then
        ' Remove extra rows
        While tbl.Rows.Count > targetRowCount
            tbl.Rows.Last.Delete
        Wend
    ElseIf targetRowCount > tbl.Rows.Count Then
        ' Add additional rows
        While tbl.Rows.Count < targetRowCount
            tbl.Rows.Add
        Wend
    End If
    
    Dim row As row
    Dim currentDate As Date
    
    For Each row In tbl.Rows
        ' Calculate the current date based on the row number
        currentDate = DateAdd("d", row.Index - 1, startDate)
        
        ' Set the date in the first column of the current row
        row.Cells(1).Range.Text = format(currentDate, "ddd, d. MMMM yyyy")
    Next row
End Sub

Function ConvertGermanDate(ByVal dateString As String) As Date
    Dim GERMAN_MONTHS() As Variant
    Dim REPLACEMENTS() As Variant
    GERMAN_MONTHS = Array("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember")
    REPLACEMENTS = Array("Mo, ", "", "Di, ", "", "Mi, ", "", "Do, ", "", "Fr, ", "", "Sa, ", "", "So, ", "")
    ' Remove day abbreviations, dots, and extra spaces
    For i = LBound(REPLACEMENTS) To UBound(REPLACEMENTS) Step 2
        dateString = Replace(dateString, REPLACEMENTS(i), REPLACEMENTS(i + 1))
    Next i
    dateString = Replace(dateString, ".", "")
    dateString = Trim(dateString)

    ' Parse the formatted date string
    Dim dateParts() As String
    dateParts = Split(dateString, " ")
    
    ' Extract day, month, and year
    Dim day As Integer
    Dim month As Integer
    Dim year As Integer
    day = Val(dateParts(0))
    month = -1
    For i = LBound(GERMAN_MONTHS) To UBound(GERMAN_MONTHS)
        If GERMAN_MONTHS(i) = dateParts(1) Then
            month = i + 1
            Exit For
        End If
    Next i
    year = Val(dateParts(2))

    ' Convert the date components to a valid Date value
    Dim formattedDate As String
    formattedDate = format(day, "00") & "/" & format(month, "00") & "/" & year
    ConvertGermanDate = CDate(formattedDate)
End Function
