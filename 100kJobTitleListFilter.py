import pandas as pd
import re
from pathlib import Path

print("this is the path")
print(Path.cwd())

# Load the data
file_path = 'Original100kJobTitleList.csv'
df = pd.read_csv(file_path, header=None)

# Melanie notes
# Keywords to consider filtering out: "Seeking", "Helping" (i included this one)
# Keywords to consider not filtering: "Retired", "Sr" (bc it's not formatted correctly), "An", "Attend"
# Before cleaning further count: 101163
# After cleaning further count (1) : 100928
# After cleaning further count (2) : 100484
# After cleaning further count (3) : 98220
# After cleaning further count (3) : 96060
# After cleaning further count (4) : 95805
# After cleaning further count (4) : 92560 
# After cleaning further count (5) : 92202 




# Define nonsense instances
nonsense_instances = {"You ", "Your ", "Yep ", "YOU ", "Without ", "With", "Why ", "Who ", "What", "When", "Whey", "Where", "Which",
    "Whistling ", "Whether ", "We ", "Was ", "Want ", "Wants ", "In ", "IM ", "Im", "If ", "YOUTUBE ", "A ", "Having ", "Have", "Has ",  
    "Above ", "Here ", "Hi", "U ", "Yuqiu Wang", "YUKI MATSUURA", "Zero Crashes", "Zero Trust", "Get ", "Getting ",  
    "YWCA Hanover", "Zanies Nashville", "Whitty", "Whitney", "Jesus ", "There ", "Think ", "This ", "The ", "Christ", "Follower", 
    "Following", "A10C", "Above", "Aboriginally", "Absolute Ray", "Accept ", "Accepted ", "All things", "Always", "Anything ", 
    "As of ", "Ask", "Awesome", "Bop ", "Born ", "Boring ", "Bring ", "C  ", "Craft", "Driven  ", "God", "H  ", "Happily r", "Happily R",
    "Happy", "Make ", "Making ", "Man ", "People first", "Permanently ", "Proving ", "Ready ", "Well h", "Well s", "Working hard ", "Working to",
    "A d", "A n", "A passionate  ", "An i", "Busting", "Communism S", "Contact me", "Containerize", "Containerizing", "Containers",
    "Come ", "Coming", "Compete", "Competence", "Furniture I", "Future is", "Future P", "Futurist", "Gainfully", "Go ", "Gone", "Good G",
    "Good m", "Good w", "Helping", "Herd", "Identity i", "Information i", "Inspire Change", "Inspire t", "Inspiring", "Let ", "Lets ", "Look ", 
    "Looking", "Love", "Loving", "Master of my", "Master of N", "Mindful M", "Mission to", "Mom ", "Mommy", "More ", "Mostly", "Mother ", "Motivated t",
    "Move ", "Mover", "Moves ", "Moving", "My ", "Now ", "On the", "On to", "Passionate l", "Putting", "Recently ", "As", "Delightful", "Deliver", "Drape",
    "Dream", "Driven", "Empower", "Energetic ", "Enjoy", "Seeking", "Actively", "Hard ", "Join ", "Keep", "Learning new", "Life is", "Living", "Proud",
    "Providing", "Pursuing new", "Retired", "Retiring", "Sr", "Starting", "Stay", "Still ", "Strengthen", "Striving", "Strong", "Taking", "Team p", 
    "Teamo", "Teamwork", "Technically", "Transforming", "Un", "using", "Work ", "Working on", "Ambitious", "An ", "Anger", "Attend", "Available",
    "Ben", "Bringing", "Business Analyst  ", "Business Development Manager  ", "Chief Ninjaneer", "Chief monkey", "Confidence", "Connecting people", 
    "Zoom dad", "Zurich"} 

# Define a function to clean job titles
def clean_job_titles(job_titles):
    cleaned_titles = []
    exceptions = ['3D', '911', "Sr ", "Unix", "Benefits", "DevOps"]

    for title in job_titles:
        if pd.isna(title):
            continue

        title = str(title).strip()

        # Check if the title is an exception (e.g., starts with "3D" or "911")
        if any(title.startswith(exc) for exc in exceptions):
            cleaned_titles.append(title)
            continue

        # Remove entries that are single words or don't start with a capital letter
        if len(title.split()) < 2 or not title[0].isupper():
            continue

        # This is possibly too much of a clean
        # Remove entries that are entirely capitalized (or have unecessary acronyms in the beginning)
        if title[0].isupper() and title[1].isupper() and title[2].isupper() and title[3].isupper() and title[4].isupper():
            continue

        # Remove entries with invalid spacing (e.g. "DevOps Manager  Containerization")
        twoSpaces = "  "

        if twoSpaces in title:
            continue

        # Remove entries that are entirely capitalized (contain all caps?) (e.g. BELT ASSEMBLY)

        if title.isupper():
            continue

        # Remove entries containing numbers (excluding the exceptions)
        if re.search(r'\d', title):
            continue

        # Remove entries starting with specific phrases
        if any(title.startswith(nonsense) for nonsense in nonsense_instances):
            continue

        # Remove entries with special characters or random letters
        if re.search(r'[^a-zA-Z\s\-\'/]', title):
            continue

        cleaned_titles.append(title)

    return cleaned_titles

# Combine all columns into a single list of job titles
all_job_titles = df.values.flatten().tolist()

# Clean the job titles
cleaned_job_titles = clean_job_titles(all_job_titles)

# Create a DataFrame with the cleaned job titles
cleaned_df = pd.DataFrame(cleaned_job_titles)

# Save the cleaned job titles to a new CSV file
cleaned_df.to_csv('Cleaned_100k_JobTitle_List.csv', index=False, header=False)

print("Job titles have been cleaned successfully.")
