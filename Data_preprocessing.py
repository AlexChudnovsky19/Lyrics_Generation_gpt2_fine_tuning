import os
import re
import lyricsgenius

# Function to check prerequisites and install packages if not already installed
def install_packages():
    try:
        import lyricsgenius
    except ImportError:
        import subprocess
        subprocess.run(['pip', 'install', 'lyricsgenius'], check=True)

# Setup API
def setup_genius():
    token = 'fHMYQIs4eePtxYbesBRrjTDeiUKKkzLm5Dp_SmOCGDh4pED9b_FjoNlhQprTHd0C' # Ensure you have set the environment variable appropriately
    genius = lyricsgenius.Genius(token)
    genius.remove_section_headers = True
    genius.timeout = 30
    genius.skip_non_songs = True
    genius.excluded_terms = ["(Remix)", "(Live)", "(Radio Edit)"]
    return genius

# Fetch lyrics for a given artist
def fetch_lyrics(genius, artist_name, max_songs=10):
    artist = genius.search_artist(artist_name, max_songs=max_songs, sort='popularity')
    return [song.lyrics for song in artist.songs] if artist else []

# Save lyrics to a file
def save_lyrics(genius, file_path):
    genres_artists = {
        "Pop": [
            "Michael Jackson", "Madonna", "Beyoncé", "Lady Gaga", "Taylor Swift",
            "Justin Bieber", "Katy Perry", "Britney Spears", "Adele", "Bruno Mars"
        ],
        "Rock": [
            "Elvis Presley", "Freddie Mercury", "David Bowie", "Jim Morrison", "Mick Jagger",
            "Bruce Springsteen", "John Lennon", "Paul McCartney", "Robert Plant", "Kurt Cobain"
        ],
        "Jazz": [
            "Ella Fitzgerald", "Billie Holiday", "Louis Armstrong", "Nina Simone", "Sarah Vaughan",
            "Chet Baker", "John Coltrane", "Miles Davis", "Tony Bennett", "Duke Ellington"
        ],
        "Rap": [
            "Tupac Shakur", "Notorious B.I.G.", "Jay-Z", "Eminem", "Kanye West",
            "Nicki Minaj", "Snoop Dogg", "Kendrick Lamar", "Lil Wayne", "Drake"
        ],
        "Country": [
            "Johnny Cash", "Dolly Parton", "Willie Nelson", "Garth Brooks", "Shania Twain",
            "Hank Williams", "Carrie Underwood", "Kenny Rogers", "Miranda Lambert", "Tim McGraw"
        ],
        "R&B": [
            "Aretha Franklin", "Stevie Wonder", "Mariah Carey", "Whitney Houston", "Usher",
            "Alicia Keys", "Ray Charles", "Mary J. Blige", "R. Kelly", "Prince"
        ],
        "Blues": [
            "B.B. King", "Muddy Waters", "John Lee Hooker", "Ray Charles", "Etta James",
            "Robert Johnson", "Buddy Guy", "Howlin’ Wolf", "Janis Joplin", "Lead Belly"
        ],
        "Electronic/Dance": [
            "Daft Punk", "Calvin Harris", "Avicii", "Deadmau5", "David Guetta",
            "Skrillex", "Tiësto", "Diplo", "Marshmello", "Kygo"
        ],
        "Reggae": [
            "Bob Marley", "Peter Tosh", "Bunny Wailer", "Gregory Isaacs", "Jimmy Cliff",
            "Toots Hibbert", "Damian Marley", "Sean Paul", "Shaggy", "Buju Banton"
        ]
    }

    with open(file_path, 'w', encoding='utf-8') as file:
        for genre, artists in genres_artists.items():
            for artist in artists:
                lyrics = fetch_lyrics(genius, artist)
                for lyric in lyrics:
                    file.write(f"[s:genre]{genre}[e:genre][s:lyrics]{lyric}[e:lyrics]\n")

# Clean lyrics from the file
def clean_lyrics(file_path, output_path):
    # Regex pattern to find and remove the undesired parts more aggressively
    contributors_pattern = re.compile(r'\d+\s*Contributors.*?Lyrics', re.DOTALL)
    # Match "Embed" followed by any number, ignoring anything up to the next tag or end of line
    embed_pattern = re.compile(r'\d+\s*Embed.*?(?=\[|$)', re.DOTALL)
    
    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Clean each line using the regex pattern
    cleaned_content = [re.sub(contributors_pattern, '', line) for line in content]
    cleaned_text = [re.sub(embed_pattern, '', line) for line in cleaned_content]

    # Write the cleaned data to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_text)

    print("Lyrics cleaned and saved to:", output_path)

def clean_lyric_content(lyric_text):
    # Remove unwanted metadata like contributor lists and translation notes
    lyric_text = re.sub(r'\d+\s*ContributorsTranslations.*?Lyrics', '', lyric_text, flags=re.DOTALL)
    # Match "Embed" followed by any number, ignoring anything up to the next tag or end of line
    embed_pattern = re.compile(r'\d+\s*Embed.*?(?=\[|$)', re.DOTALL)
    lyric_text = re.sub(embed_pattern, '', lyric_text)
    lyric_text = re.sub(r'\[.*?\](?!\[s:|\[e:)', '', lyric_text)  # Remove all brackets that do not start structural tags

    return lyric_text.strip()

# Main execution flow
if __name__ == "__main__":
    install_packages()
    genius_api = setup_genius()
    lyrics_file_path = r'C:\Users\alexc\Fine_tuning_gpt2\cleaned_lyrics_data.txt'
    if not os.path.exists(lyrics_file_path):
        print('Start using Genius API to load the training data...')
        save_lyrics(genius_api, lyrics_file_path)

    clean_lyrics_path = r'C:\Users\alexc\Fine_tuning_gpt2\final_cleaned_lyrics.txt'
    clean_lyrics(lyrics_file_path, clean_lyrics_path)
    print(f"Lyrics cleaned and saved to: {clean_lyrics_path}")