
import configparser
import click
import csv
import dumper

from datetime import datetime, timezone
from pytz import timezone
from pathlib import Path
from jira import JIRA
from jira.exceptions import JIRAError

DEFAULT_CONFIG = str(Path.home()) + "/.jira_config"
TIMELOG_FORMAT = "{}h {}m"

# Used headers from the Report CSV
PRJ_COLUMN="Project"
DESC_COLUMN="Description"
DUR_COLUMN="Duration"
START_DATE_COLUMN="Start date"
START_TIME_COLUMN="Start time"


def jira_connect(conf: configparser.ConfigParser) -> JIRA:
    """
    Return a connected JIRA object. Credentials & Server specified in the 'conf' ConfigParser
    Not using the default JIRA project "config.ini" because of the need to override the agile_rest_path.
    @TODO - Does V2.0.1 provide this

    \f
    Args:
        conf (configparser.ConfigParser): Config file

    Returns:
        JIRA: JIRA object to the connected instance
    """
    options = {} # "agile_rest_path":'agile' }
    try:
        return JIRA(conf['jira']['server'], options, auth=(conf['jira']['username'], conf['jira']['password']) )
    except:
        print ("Error connecting to JIRA - check your credentials and try again")
        exit(-1)


@click.command()
@click.option('--config', '-c', type=click.STRING, required=False, help="Path to config file",
              default=DEFAULT_CONFIG)
@click.option('--timesheet', '-t', type=click.STRING, required=True, help="Detailed CSV Timesheet to parse")
@click.option('--safe/--unsafe', default=True, help="Ignore")
def cli(config, timesheet, safe):
    """[summary]

    Args:
        ctx (Object): Click context to save the default arg state.
        config (String): Config file parameter defaults to file in DEFAULT_CONFIG
        timesheet (String): Timesheet file to parse
    """
    # ctx
    # ctx.ensure_object(dict)
    conf = configparser.ConfigParser()
    conf.read(config)
    jira = jira_connect(conf)
    print(jira.current_user())

    with open(timesheet) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            if row['Project'] != "" or not safe :
                issue=row[PRJ_COLUMN].split(" - ")[0]
                time=row[DUR_COLUMN].split(":")
                # Time is assume to be hh:mm:ss
                # For Reporting - Not reporting seconds, and for worklog entries, using
                # Jira {}h {}m
                timespent_worklog = TIMELOG_FORMAT.format(int(time[0]), int(time[1]))
                start_time=row[START_TIME_COLUMN].split(":")
                hr = int(start_time[0])
                local_timezone = datetime.utcnow().astimezone().tzinfo
                mangled_start_time = datetime.strptime( "{} {}:{} {}".format(row[START_DATE_COLUMN], hr, start_time[1], local_timezone) , "%Y-%m-%d %H:%M %Z")

                #IDEA: PREVENT DOUBLING UP AN EXISTING WORKLOG
                jira.add_worklog(issue= issue,
                                timeSpent= timespent_worklog,
                                started = mangled_start_time ,
                                comment = row[DESC_COLUMN])

                print ("{} {}   {} {}".format(issue, mangled_start_time, timespent_worklog, row[DESC_COLUMN]))




if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli()
