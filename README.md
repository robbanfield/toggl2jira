# toggl2jira

Import Toggl Track Export to Jira (on-premise)

Do you ever have to track time in Jira, but the stories you work on are not what you have to report time against?

Do you have doing timesheets at the end of the month and use Toggl to try and help?

I do, so I got fed up of the back and forth and scripted.

## Pre-Requsites

1. In Toggl, you have projects named that match your Jira time tracking stories. (You can import per the sampleproject.csv in the docs folder)
2. In your home directory, create the file .jira.config using [docs/jira.config] as template.
3. Update your timezone in Toggle2Jira

## Usage

1. Export the Detailed Monthly report as CSV to current working directory.
Known working headers are:

```csv

User,Email,Client,Project,Task,Description,Billable,Start date,Start time,End date,End time,Duration,Tags,Amount ()

```
