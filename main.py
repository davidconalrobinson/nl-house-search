from src.funda import Funda
from src.database import Database
from src.notifier import Notifier


SEND_TO = ["davidconalrobinson@gmail.com", "tessannekehayes@gmail.com"]


# Get Funda listings
funda = Funda()
funda_df = funda.get_all()

# Insert listings into database
database = Database()
database.insert_listings(funda_df)

# Get new listings
new_listings = database.get_listings("""
    SELECT
        *
    FROM listings
    WHERE new = "TRUE"
    AND available_on >= "2023-01-01"
""")

# Send notification
notifier = Notifier()
if len(new_listings) > 0:
    notifier.send_email(
        to=SEND_TO,
        subject="New listings",
        content="\n".join(new_listings["listing"])
    )