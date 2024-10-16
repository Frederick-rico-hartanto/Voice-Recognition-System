using System;
using System.Diagnostics;
using System.Threading;
using System.Windows.Automation;  // Add reference to UIAutomationClient

class ClockAutomation
{
    static void Main(string[] args)
    {
        // Ensure a command and timer duration is provided
        if (args.Length == 0 || (args[0].ToLower() == "timer" && args.Length < 2))
        {
            Console.WriteLine("Please provide a valid command: 'timer <duration>', 'stopwatch', or 'alarm'.");
            return;
        }

        string command = args[0].ToLower();
        string timerDuration = args.Length > 1 ? args[1] : null;

        // Step 1: Open Microsoft Clock app
        Process.Start("ms-clock:");
        Console.WriteLine("Opening Microsoft Clock app...");

        // Step 2: Give it some time to open
        Thread.Sleep(3000);  // Adjust the delay as needed

        // Step 3: Find the Clock window
        AutomationElement clockWindow = AutomationElement.RootElement.FindFirst(TreeScope.Children,
            new PropertyCondition(AutomationElement.NameProperty, "Clock"));

        if (clockWindow == null)
        {
            Console.WriteLine("Failed to find the Microsoft Clock app.");
            return;
        }

        Console.WriteLine("Microsoft Clock app found!");

        // Handle different commands: timer, stopwatch, alarm
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
        // Step 4: Find the Timer tab and click it
        AutomationElement timerTab = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Timer"));
        if (timerTab == null)
        {
            Console.WriteLine("Timer tab not found.");
            return;
        }

        Console.WriteLine("Timer tab found, activating it...");
        InvokePattern invokeTimer = timerTab.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
        invokeTimer?.Invoke();
        Thread.Sleep(1000);  // Allow time for the UI to switch

        // Step 5: Check if a timer exists; if not, set a new one based on the provided duration
        AutomationElement startTimerButton = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Start"));

        if (startTimerButton != null)
        {
            Console.WriteLine("Existing timer found, starting it...");
            InvokePattern invokeStartTimer = startTimerButton.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
            invokeStartTimer?.Invoke();
        }
        else if (duration != null)
        {
            Console.WriteLine($"Setting a new timer for {duration}.");

            // Example: Set timer duration dynamically based on the provided duration
            AutomationElement durationButton = FindDurationButton(clockWindow, duration);
            
            if (durationButton != null)
            {
                InvokePattern invokeDuration = durationButton.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
                invokeDuration?.Invoke();
                Console.WriteLine($"{duration} timer set.");
            }
            else
            {
                Console.WriteLine($"Failed to find the timer duration button for {duration}.");
            }
        }
        else
        {
            Console.WriteLine("No existing timer found, but no duration provided for a new timer.");
        }
    }

    static AutomationElement FindDurationButton(AutomationElement parent, string duration)
    {
        // This method simulates searching for the correct timer duration button in the UI
        // Modify this based on the actual UI structure of the Clock app
        return parent.FindFirst(TreeScope.Descendants, new PropertyCondition(AutomationElement.NameProperty, duration));
    }

    static void HandleStopwatch(AutomationElement clockWindow)
    {
        // Step 4: Find the Stopwatch tab and click it
        AutomationElement stopwatchTab = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Stopwatch"));

        if (stopwatchTab == null)
        {
            Console.WriteLine("Stopwatch tab not found.");
            return;
        }

        Console.WriteLine("Stopwatch tab found, activating it...");
        InvokePattern invokeStopwatch = stopwatchTab.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
        invokeStopwatch?.Invoke();
        Thread.Sleep(1000);  // Allow time for the UI to switch

        // Step 5: Check if a stopwatch exists; if not, start a new one
        AutomationElement startStopwatchButton = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Start"));

        if (startStopwatchButton != null)
        {
            Console.WriteLine("Stopwatch exists, starting it...");
            InvokePattern invokeStartStopwatch = startStopwatchButton.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
            invokeStartStopwatch?.Invoke();
        }
        else
        {
            Console.WriteLine("Failed to start the stopwatch.");
        }
    }

    static void HandleAlarm(AutomationElement clockWindow)
    {
        // Step 4: Find the Alarm tab and click it
        AutomationElement alarmTab = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "Alarm"));

        if (alarmTab == null)
        {
            Console.WriteLine("Alarm tab not found.");
            return;
        }

        Console.WriteLine("Alarm tab found, activating it...");
        InvokePattern invokeAlarm = alarmTab.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
        invokeAlarm?.Invoke();
        Thread.Sleep(1000);  // Allow time for the UI to switch

        // Step 5: Check if an alarm exists; if not, create a new one
        AutomationElement startAlarmButton = clockWindow.FindFirst(TreeScope.Descendants,
            new PropertyCondition(AutomationElement.NameProperty, "On"));

        if (startAlarmButton != null)
        {
            Console.WriteLine("Existing alarm found, turning it on...");
            InvokePattern invokeStartAlarm = startAlarmButton.GetCurrentPattern(InvokePattern.Pattern) as InvokePattern;
            invokeStartAlarm?.Invoke();
        }
        else
        {
            Console.WriteLine("No existing alarm found, creating a new one.");
            // Logic to set a new alarm (you would need to customize based on actual UI elements)
        }
    }
}
