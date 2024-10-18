using System;
using System.Diagnostics;
using System.Threading;
using System.Windows.Automation;
using WindowsInput;
using WindowsInput.Native;

class ClockAutomation
{
    static void Main(string[] args)
    {
        if (args.Length == 0 || (args[0].ToLower() == "timer" && args.Length < 2) || (args[0].ToLower() == "alarm" && args.Length < 3))
        {
            Console.WriteLine("Please provide a valid command: 'timer <duration>', 'stopwatch', or 'alarm <time> <day>'.");
            return;
        }

        string command = args[0].ToLower();
        string timerDuration = args.Length > 1 ? args[1] : "1";  // Default to "1" minute if not provided
        string alarmTime = args.Length > 1 ? args[1] : null;  // Alarm time
        string alarmDay = args.Length > 2 ? args[2] : null;  // Alarm day

        // Step 1: Open the Microsoft Clock app
        Process.Start("ms-clock:");
        Console.WriteLine("Opening Microsoft Clock app...");

        Thread.Sleep(3000);  // Adjust the delay to give the app time to load

        // Step 2: Find the Clock window
        AutomationElement clockWindow = AutomationElement.RootElement.FindFirst(TreeScope.Children,
            new PropertyCondition(AutomationElement.NameProperty, "Clock"));

        if (clockWindow == null)
        {
            Console.WriteLine("Failed to find the Microsoft Clock app.");
            return;
        }

        Console.WriteLine("Microsoft Clock app found!");

        // Handle the requested command
        switch (command)
        {
            case "timer":
                HandleTimer(clockWindow, timerDuration);
                break;
            case "stopwatch":
                string stopwatchAction = args.Length > 1 ? args[1].ToLower() : "start";
                HandleStopwatch(clockWindow, stopwatchAction);
                break;
            case "alarm":
                if (alarmTime != null && alarmDay != null)
                {
                    HandleAlarm(clockWindow, alarmTime, alarmDay);
                }
                else
                {
                    Console.WriteLine("Invalid alarm time or day.");
                }
                break;
            default:
                Console.WriteLine("Unknown command. Please use 'timer', 'stopwatch', or 'alarm'.");
                break;
        }
    }

    // Handle setting a timer
static void HandleTimer(AutomationElement clockWindow, string duration)
{
    // Step 1: Find and activate the Timer tab
    AutomationElement timerTab = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Timer"));

    if (timerTab == null)
    {
        Console.WriteLine("Timer tab not found.");
        return;
    }

    Console.WriteLine("Timer tab found, activating it...");

    object patternObj;
    // Try to select the tab (ExpandCollapse or Toggle if supported)
    if (timerTab.TryGetCurrentPattern(ExpandCollapsePattern.Pattern, out patternObj))
    {
        ExpandCollapsePattern expandPattern = (ExpandCollapsePattern)patternObj;
        expandPattern.Expand();
        Console.WriteLine("Timer tab expanded using ExpandCollapsePattern.");
    }
    else if (timerTab.TryGetCurrentPattern(TogglePattern.Pattern, out patternObj))
    {
        TogglePattern togglePattern = (TogglePattern)patternObj;
        togglePattern.Toggle();
        Console.WriteLine("Timer tab toggled using TogglePattern.");
    }
    else
    {
        Console.WriteLine("The Timer tab does not support ExpandCollapsePattern or TogglePattern.");
    }

    Thread.Sleep(1000);  // Wait for the UI to switch

    // Step 2: Find and click the "Add new timer" button
    AutomationElement addTimerButton = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Add new timer"));

    if (addTimerButton != null)
    {
        Console.WriteLine("Add Timer button found, clicking it...");
        if (addTimerButton.TryGetCurrentPattern(InvokePattern.Pattern, out patternObj))
        {
            InvokePattern invokeAddTimer = (InvokePattern)patternObj;
            invokeAddTimer.Invoke();
        }
        else
        {
            Console.WriteLine("Add Timer button does not support InvokePattern.");
        }
    }
    else
    {
        Console.WriteLine("Failed to find the Add Timer button.");
        return;
    }

    Thread.Sleep(1000);  // Wait for the new timer dialog to appear

    // Step 3: Set the new timer
    Console.WriteLine($"Setting a new timer for {duration} (h:m:s).");
    SimulateArrowKeyPressForDuration(duration);

    // Step 4: Save the timer
    AutomationElement saveTimerButton = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Save"));

    if (saveTimerButton != null)
    {
        Console.WriteLine("Saving the timer.");
        if (saveTimerButton.TryGetCurrentPattern(InvokePattern.Pattern, out patternObj))
        {
            InvokePattern invokeSaveTimer = (InvokePattern)patternObj;
            invokeSaveTimer.Invoke();
        }
        else
        {
            Console.WriteLine("Save button does not support InvokePattern.");
        }
    }
    else
    {
        Console.WriteLine("Failed to find the Save button.");
        return;
    }

    Thread.Sleep(1000);  // Allow some time for the new timer to appear

    // Step 5: Start the newly created timer
    StartNewlyCreatedTimer(clockWindow);
}

// Simulate arrow key presses to set the timer duration
static void SimulateArrowKeyPressForDuration(string duration)
{
    Console.WriteLine($"Simulating arrow key press to set the timer to {duration} (h:m:s).");

    var sim = new InputSimulator();

    // Split the duration into hours, minutes, and seconds
    string[] timeParts = duration.Split(':');
    int targetHours = timeParts.Length > 0 ? int.Parse(timeParts[0]) : 0;
    int targetMinutes = timeParts.Length > 1 ? int.Parse(timeParts[1]) : 0;
    int targetSeconds = timeParts.Length > 2 ? int.Parse(timeParts[2]) : 0;

    // Step 1: Set the hours using arrow keys
    AdjustTimerField(sim, 0, targetHours, "hours");

    // Step 2: Tab to the minutes input
    sim.Keyboard.KeyPress(VirtualKeyCode.TAB);
    Thread.Sleep(500);

    // Step 3: Set the minutes using arrow keys
    AdjustTimerField(sim, 0, targetMinutes, "minutes");

    // Step 4: Tab to the seconds input
    sim.Keyboard.KeyPress(VirtualKeyCode.TAB);
    Thread.Sleep(500);

    // Step 5: Set the seconds using arrow keys
    AdjustTimerField(sim, 0, targetSeconds, "seconds");

    Console.WriteLine($"Timer set to {targetHours}:{targetMinutes}:{targetSeconds}.");
}

// Function to adjust hours, minutes, or seconds using the arrow keys
static void AdjustTimerField(InputSimulator sim, int currentValue, int targetValue, string fieldName)
{
    Console.WriteLine($"Adjusting {fieldName} from {currentValue} to {targetValue}");

    if (currentValue == targetValue)
    {
        Console.WriteLine($"{fieldName} is already set to {targetValue}.");
        return;
    }

    while (currentValue != targetValue)
    {
        if (targetValue > currentValue)
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.UP);  // Press up arrow to increase the value
            currentValue++;
        }
        else
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.DOWN);  // Press down arrow to decrease the value
            currentValue--;
        }
        Thread.Sleep(300);  // Allow UI to update
    }
}

// Function to find and start the most recently created timer
static void StartNewlyCreatedTimer(AutomationElement clockWindow)
{
    // Find the most recent "Start" button
    AutomationElementCollection startButtons = clockWindow.FindAll(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Start"));

    if (startButtons.Count > 0)
    {
        // Assuming the last "Start" button belongs to the newly created timer
        AutomationElement latestStartButton = startButtons[startButtons.Count - 1];

        Console.WriteLine("Starting the newly created timer.");
        if (latestStartButton.TryGetCurrentPattern(InvokePattern.Pattern, out object patternObj))
        {
            InvokePattern invokeStartTimer = (InvokePattern)patternObj;
            invokeStartTimer.Invoke();
        }
        else
        {
            Console.WriteLine("Start button does not support InvokePattern.");
        }
    }
    else
    {
        Console.WriteLine("Failed to find the Start button for the timer.");
    }
}




    // Handle the stopwatch feature
static void HandleStopwatch(AutomationElement clockWindow, string action)
{
    // Step 1: Find the Stopwatch tab and click it
    AutomationElement stopwatchTab = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Stopwatch"));

    if (stopwatchTab == null)
    {
        Console.WriteLine("Stopwatch tab not found.");
        return;
    }

    Console.WriteLine("Stopwatch tab found, activating it...");

    object patternObj;
    if (stopwatchTab.TryGetCurrentPattern(SelectionItemPattern.Pattern, out patternObj))
    {
        SelectionItemPattern selectStopwatch = (SelectionItemPattern)patternObj;
        selectStopwatch.Select();
        Console.WriteLine("Stopwatch tab activated.");
    }
    else
    {
        Console.WriteLine("The Stopwatch tab does not support SelectionItemPattern.");
        return;
    }

    Thread.Sleep(1000);  // Wait for the UI to switch

    // Determine the action: Start, Pause, or Reset
    string buttonName = null;
    switch (action.ToLower())
    {
        case "start":
            buttonName = "Start";
            break;
        case "pause":
            buttonName = "Pause";
            break;
        case "reset":
            buttonName = "Reset";
            break;
        default:
            Console.WriteLine("Invalid action. Please use 'start', 'pause', or 'reset'.");
            return;
    }

    // Step 2: Find the corresponding button based on the action
    AutomationElement stopwatchButton = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, buttonName));

    if (stopwatchButton == null)
    {
        Console.WriteLine($"{buttonName} button not found.");
        return;
    }

    Console.WriteLine($"{buttonName} button found, attempting to {action} the stopwatch...");

    // Step 3: Invoke the Start/Pause/Reset button
    if (stopwatchButton.TryGetCurrentPattern(InvokePattern.Pattern, out patternObj))
    {
        InvokePattern invokeStopwatch = (InvokePattern)patternObj;
        invokeStopwatch.Invoke();
        Console.WriteLine($"Stopwatch {action}ed.");
    }
    else
    {
        Console.WriteLine($"{buttonName} button does not support InvokePattern.");
    }
}





    // Handle the alarm feature
static void HandleAlarm(AutomationElement clockWindow, string time, string day)
{
    // Step 1: Find the Alarm tab and click it
    AutomationElement alarmTab = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Alarm"));

    if (alarmTab == null)
    {
        Console.WriteLine("Alarm tab not found.");
        return;
    }

    Console.WriteLine("Alarm tab found, activating it...");

    object patternObj;
    if (alarmTab.TryGetCurrentPattern(SelectionItemPattern.Pattern, out patternObj))
    {
        SelectionItemPattern selectAlarm = (SelectionItemPattern)patternObj;
        selectAlarm.Select();
        Console.WriteLine("Alarm tab activated.");
    }
    else
    {
        Console.WriteLine("The Alarm tab does not support SelectionItemPattern.");
    }

    Thread.Sleep(1000);  // Allow time for the UI to switch

    // Step 2: Find the "+" button to add a new alarm
    AutomationElement addAlarmButton = clockWindow.FindFirst(TreeScope.Descendants,
        new PropertyCondition(AutomationElement.NameProperty, "Add new alarm"));

    if (addAlarmButton != null)
    {
        Console.WriteLine("Add Alarm button found, clicking it...");
        if (addAlarmButton.TryGetCurrentPattern(InvokePattern.Pattern, out patternObj))
        {
            InvokePattern invokeAddAlarm = (InvokePattern)patternObj;
            invokeAddAlarm.Invoke();
        }
        else
        {
            Console.WriteLine("Add Alarm button does not support InvokePattern.");
        }
    }
    else
    {
        Console.WriteLine("Failed to find the Add Alarm button, trying fallback method.");

        // Simulate pressing TAB to navigate to the "+" button and press Enter
        SimulateAddAlarmButtonClick();
    }

    Thread.Sleep(1000);  // Wait for the new alarm creation dialog to appear

    // Step 3: Simulate setting the alarm time and day, and then saving it
    SimulateTabNavigationForAlarm(time, day);
}

static void SimulateTabNavigationForAlarm(string time, string day)
{
    Console.WriteLine($"Simulating key press to set the alarm for {time} on {day}.");

    var sim = new InputSimulator();

    // Extract the hour and minute from the time input
    var timeParts = time.Split(':');
    int targetHour = int.Parse(timeParts[0]);
    int targetMinute = timeParts.Length > 1 ? int.Parse(timeParts[1]) : 0;  // Default to "00" if no minutes provided

    // Step 1: Set the hour using the up/down arrow keys
    SetHour(sim, targetHour);

    // Step 2: Tab to the minutes input (1 time) and set the minutes
    TabToMinutes(sim);
    SetMinute(sim, targetMinute);

    // Step 3: Tab to the day selection and select the appropriate day
    TabToDaySelection(sim);
    SelectDayOfWeek(sim, day);

    // Step 4: Tab to the Save button and press Enter to save the alarm
    TabToSaveButton(sim);
    SaveAlarm(sim);
    Console.WriteLine($"Alarm set for {time} on {day}.");
}

// Function to set the hour using the arrow keys
static void SetHour(InputSimulator sim, int targetHour)
{
    Console.WriteLine($"Setting the hour to {targetHour}");
    int currentHour = 7;  // Assuming the default value is 7 (from the screenshot)

    while (currentHour != targetHour)
    {
        if (targetHour > currentHour)
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.UP);  // Press up arrow to increase the hour
            currentHour++;
        }
        else
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.DOWN);  // Press down arrow to decrease the hour
            currentHour--;
        }
        Thread.Sleep(300);  // Allow UI to update
    }
}

// Function to tab to the minutes input
static void TabToMinutes(InputSimulator sim)
{
    sim.Keyboard.KeyPress(VirtualKeyCode.TAB);
    Thread.Sleep(500);  // Wait for UI to respond
}

// Function to set the minutes using the arrow keys
static void SetMinute(InputSimulator sim, int targetMinute)
{
    Console.WriteLine($"Setting the minute to {targetMinute}");
    int currentMinute = 0;  // Assuming the default value is 00

    while (currentMinute != targetMinute)
    {
        if (targetMinute > currentMinute)
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.UP);  // Press up arrow to increase the minute
            currentMinute += 1;
        }
        else
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.DOWN);  // Press down arrow to decrease the minute
            currentMinute -= 1;
        }
        Thread.Sleep(300);  // Allow UI to update
    }
}

// Function to tab to the day selection section
static void TabToDaySelection(InputSimulator sim)
{
    Console.WriteLine("Tabbing to day selection...");

    // Increase the number of TAB presses to ensure the correct section is reached
    for (int i = 0; i < 3; i++)  // Try tabbing 4 times instead of 3
    {
        sim.Keyboard.KeyPress(VirtualKeyCode.TAB);
        Console.WriteLine($"Tab {i+1} pressed.");
        Thread.Sleep(1000);  // Increase the wait time to allow the UI to catch up
    }
    Console.WriteLine("Should be at day selection.");
}


// Function to select the correct day
static void SelectDayOfWeek(InputSimulator sim, string day)
{
    Console.WriteLine($"Navigating to the day: {day}");

    // Days of the week as they appear in the alarm screen (abbreviations)
    string[] daysOfWeek = { "Su", "M", "Tu", "We", "Th", "Fr", "Sa" };

    // Convert the input day to its abbreviation (e.g., "tuesday" -> "Tu")
    string normalizedDay = day.Substring(0, 2).ToLower();
    string targetDay = "";

    // Map the first two characters of the input to the corresponding day abbreviation
    switch (normalizedDay)
    {
        case "su":
            targetDay = "Su";
            break;
        case "mo":
            targetDay = "M";
            break;
        case "tu":
            targetDay = "Tu";
            break;
        case "we":
            targetDay = "We";
            break;
        case "th":
            targetDay = "Th";
            break;
        case "fr":
            targetDay = "Fr";
            break;
        case "sa":
            targetDay = "Sa";
            break;
        default:
            Console.WriteLine("Invalid day provided.");
            return;
    }

    int targetIndex = Array.IndexOf(daysOfWeek, targetDay);

    if (targetIndex >= 0)
    {
        // Since the day starts at "Su" (Sunday), we'll press the arrow to the right targetIndex times.
        for (int i = 0; i < targetIndex; i++)
        {
            sim.Keyboard.KeyPress(VirtualKeyCode.RIGHT);  // Simulate pressing right arrow to select the day
            Thread.Sleep(300);  // Give time for the UI to respond
        }
        
        // Simulate pressing Enter to confirm the selection
        sim.Keyboard.KeyPress(VirtualKeyCode.RETURN);
        Console.WriteLine($"{targetDay} selected and confirmed.");
    }
    else
    {
        Console.WriteLine("Invalid day provided.");
    }
}


// Function to tab to the Save button
static void TabToSaveButton(InputSimulator sim)
{
    for (int i = 0; i < 3; i++)  // Adjust based on the actual number of tabs needed to reach Save
    {
        sim.Keyboard.KeyPress(VirtualKeyCode.TAB);
        Thread.Sleep(500);  // Wait for the UI to respond
    }
}

// Function to press Enter and save the alarm
static void SaveAlarm(InputSimulator sim)
{
    sim.Keyboard.KeyPress(VirtualKeyCode.RETURN);
}




// Fallback method: Simulate keypresses to navigate and press the Add Alarm button
static void SimulateAddAlarmButtonClick()
{
    Console.WriteLine("Simulating key press to navigate to Add Alarm button.");

    var sim = new InputSimulator();

    // Simulate pressing TAB multiple times to reach the Add Alarm button
    for (int i = 0; i < 3; i++)  // Adjust the number of TAB presses based on the UI structure
    {
        sim.Keyboard.KeyPress(VirtualKeyCode.TAB);
        Thread.Sleep(500);  // Wait for the UI to respond
    }

    // Simulate pressing Enter to click the Add Alarm button
    sim.Keyboard.KeyPress(VirtualKeyCode.RETURN);
}


}
