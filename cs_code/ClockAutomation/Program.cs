using System;
using System.Diagnostics;
using System.Threading;
using System.Windows.Automation;
using WindowsInput;   // Import the InputSimulator library
using WindowsInput.Native;   // Import the Virtual Keycodes

class ClockAutomation
{
    static void Main(string[] args)
    {
        if (args.Length == 0 || (args[0].ToLower() == "timer" && args.Length < 2))
        {
            Console.WriteLine("Please provide a valid command: 'timer <duration>', 'stopwatch', or 'alarm'.");
            return;
        }

        string command = args[0].ToLower();
        string timerDuration = args.Length > 1 ? args[1] : null;

        Process.Start("ms-clock:");
        Console.WriteLine("Opening Microsoft Clock app...");

        Thread.Sleep(3000);  // Adjust the delay as needed

        AutomationElement clockWindow = AutomationElement.RootElement.FindFirst(TreeScope.Children,
            new PropertyCondition(AutomationElement.NameProperty, "Clock"));

        if (clockWindow == null)
        {
            Console.WriteLine("Failed to find the Microsoft Clock app.");
            return;
        }

        Console.WriteLine("Microsoft Clock app found!");

        switch (command)
        {
            case "timer":
                HandleTimer(clockWindow, timerDuration);
                break;
            case "stopwatch":
                HandleStopwatch(clockWindow);
                break;
            case "alarm":
                HandleAlarm(clockWindow);
                break;
            default:
                Console.WriteLine("Unknown command. Please use 'timer', 'stopwatch', or 'alarm'.");
                break;
        }
    }

    static void HandleTimer(AutomationElement clockWindow, string duration)
    {
        // Step 1: Find the Timer tab and click it
        AutomationElement timerTab = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Timer"));

        if (timerTab == null)
        {
            Console.WriteLine("Timer tab not found.");
            return;
        }

        Console.WriteLine("Timer tab found, activating it...");

        object patternObj;
        // Try to select the tab
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

        Thread.Sleep(1000);  // Allow time for the UI to switch

        // Step 2: Check if a timer already exists
        AutomationElement startTimerButton = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Start"));

        if (startTimerButton != null)
        {
            Console.WriteLine("Existing timer found, starting it...");
            if (startTimerButton.TryGetCurrentPattern(InvokePattern.Pattern, out patternObj))
            {
                InvokePattern invokeStartTimer = (InvokePattern)patternObj;
                invokeStartTimer.Invoke();
            }
            else
            {
                Console.WriteLine("Start button does not support InvokePattern.");
            }
        }
        else if (duration != null)
        {
            Console.WriteLine($"Setting a new timer for {duration} minutes.");

            // Step 3: Set the timer duration if no timer exists
            AutomationElement durationButton = FindDurationButton(clockWindow, duration);
            if (durationButton != null && durationButton.TryGetCurrentPattern(InvokePattern.Pattern, out patternObj))
            {
                InvokePattern invokeDuration = (InvokePattern)patternObj;
                invokeDuration.Invoke();
                Console.WriteLine($"{duration} minute timer set.");
            }
            else
            {
                Console.WriteLine($"Failed to find or invoke the timer duration button for {duration} minutes.");
            }
        }
        else
        {
            Console.WriteLine("No existing timer found, but no duration provided for a new timer.");
        }
    }

    static void SimulateKeyPressForTimer()
    {
        // Fallback logic to send key presses to switch to the Timer tab
        Console.WriteLine("Simulating key press for Timer tab.");

        // Use InputSimulator to simulate key press
        var sim = new InputSimulator();
        sim.Keyboard.ModifiedKeyStroke(VirtualKeyCode.CONTROL, VirtualKeyCode.VK_T); // Simulate Ctrl+T
    }

    static AutomationElement FindDurationButton(AutomationElement parent, string duration)
    {
        Console.WriteLine($"Searching for timer duration button: {duration} minutes.");
        return parent.FindFirst(TreeScope.Descendants, new PropertyCondition(AutomationElement.NameProperty, duration));
    }

    static void HandleStopwatch(AutomationElement clockWindow)
    {
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
        }
        else
        {
            Console.WriteLine("The Stopwatch tab does not support SelectionItemPattern.");
        }
    }

    static void HandleAlarm(AutomationElement clockWindow)
    {
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
        }
        else
        {
            Console.WriteLine("The Alarm tab does not support SelectionItemPattern.");
        }
    }
}
