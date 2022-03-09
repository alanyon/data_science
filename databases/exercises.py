import sqlite3


def main():

    # Exercise 2 - How many rows are in the customers table?
    conn =sqlite3.connect('chinook.db')
    c = conn.cursor()

    c.execute('SELECT * FROM customers')
    rows = c.fetchall()

    print('Number of rows', len(rows))

    # Exercise 3 - How many different Blues composers are in the database?
    c.execute('SELECT DISTINCT Composer FROM tracks WHERE genreId=6')
    blues = c.fetchall()
    print('Number of blues composers', len(blues))

    # Exercise 4 - List the composer, track name and track length from each track on album
    # 204, ordered by composer name and decreasing track length.
    c.execute('SELECT Composer, Name, Milliseconds from tracks WHERE '
              'albumId=204 ORDER BY Composer, Milliseconds DESC')
    album_204 = c.fetchall()
    print('Album 204', album_204)

    # Exercis 5 - Find the average length of tracks which between 3 and 4
    # megabytes.
    c.execute('SELECT AVG(Milliseconds) from tracks WHERE '
              'bytes BETWEEN 3000000 and 4000000')
    mbs = c.fetchall()
    print('mbs', mbs)

    c.execute('PRAGMA table_info(invoices)')
    print('invoices', c.fetchall())

    # Exercise 6 - What is the first and last name of the customer who has the
    # largest invoice?
    c.execute('SELECT FirstName, LastName from customers WHERE '
              'CustomerId=(SELECT CustomerId FROM invoices WHERE '
              'Total=(SELECT MAX(Total) FROM invoices))')
    names = c.fetchall()
    for tup in names:
        for name in tup:
            print('name', name.encode('utf-8'))

    # Exercise 7 - Find the artists whose names begin with ‘The’
    c.execute('SELECT Name FROM artists WHERE Name LIKE "The%"')
    the_names = c.fetchall()
    print('the names', the_names)

    # Exercise 8 - List the tracks in the Brazilian Music Playlist
    c.execute('SELECT Name FROM tracks WHERE tracks.TrackId IN '
              '(SELECT playlist_track.TrackId FROM playlist_track INNER JOIN '
              'playlists ON playlist_track.PlaylistId = playlists.PlaylistId '
              'WHERE playlist_track.PlaylistId=11)')
    brazil = c.fetchall()
    for tup in brazil:
        for name in tup:
            print('name', name.encode('utf-8'))

    # Exercise 9 - List the number of tracks in each genre
    c.execute('SELECT GenreId, COUNT(Name) FROM tracks '
              'GROUP BY GenreId')
    genres = c.fetchall()
    print('genres', genres)

    # Exercise 9 - List the number of tracks in each genre
    c.execute('SELECT genres.Name, COUNT(TrackId) FROM tracks INNER JOIN '
              'genres ON genres.GenreID = tracks.GenreId GROUP BY '
              'tracks.GenreId')
    genres = c.fetchall()
    print('genres', genres)


if __name__ == "__main__":
    main()
