from src.app import generate_playlist 

test_prompt = 'Lonely days'
def test_playlist_generation(prompt):
    """A test that ensures that we can generate playlists and song cover_arts"""
    result = generate_playlist(test_prompt)
    songs  = result[0]
    cover_art = result[1]
    
    assert len(cover_art) == len(songs)
    assert error not in   