#!/usr/bin/python

# Sophia Fondell
# sfondell@bu.edu
# CS 108: Final Project - bingeList - render.py
# This file handles printing out HTML, displaying page information, and 
# accepting/reacting to entered information
# URL: http://cs-webapps.bu.edu/cgi-bin/cs108/sfondell/bingeList/render.py

import backend
import MySQLdb as db
import time
import cgi
import cgitb; cgitb.enable()

# print out the HTTP headers right away, before we do any other statements


def htmlHead(title):
	'''This function handles printing out the header for the page and takes a page
	title as a parameter'''
	print('''
	<html>
		<head>
			<title>%s</title>
			<link rel="stylesheet" type="text/css" href="bingelist.css">
			<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins">
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
			<link rel="shortcut icon" type="image/png" href="http://i1225.photobucket.com/albums/ee381/enix-directory/Pixels/a_tvrosinha.gif"/>
		</head>
	<body>
		<h1>%s</h1>
	<p>
	''' % (title, title))

def htmlTail():
	'''This function handles printing out the tail of the page which closes the tags and
	has a link back to the home page'''
	print('''
		<div class="homelink">
			<a href="https://cs-webapps.bu.edu/cgi-bin/cs108/sfondell/bingeList/render.py">Back to home</a>
		</div>
		<p>
	</body>
	</html>
	''')

def showHome():
	'''This function handles printing out the home page'''
	print('''
	<html>
		<head>
			<title>bingeList</title>
			<link rel="stylesheet" type="text/css" href="bingelist.css">
			<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins">
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
			<link rel="shortcut icon" type="image/png" href="http://i1225.photobucket.com/albums/ee381/enix-directory/Pixels/a_tvrosinha.gif"/>
		</head>
	<body>
	<p>
	<header class="netflixbg">
		<b>bingeList</b>
		<p>Rate, review, and keep track of all of your favorite Netflix shows in one place</p>
	</header>
	<h1>Browse by user</h1>
	<div class="userslist">
		<table border=1>
	''')

	# Get a list of all users from the backend
	userdata = backend.getUsers()

	# Loop through the returned tuple and print out each user with a link to their page
	for row in userdata:
		(userid, bio) = row
		print('''
		<tr>
			<td><a href="?userid=%s">%s</a></td>
			<td>%s</td>
		</tr>
		''' % (userid, userid, bio))

	print('''
		</table>
	</div>
	''')


def showShows():
	'''This function handles printing out a list of all tv shows'''

	#Get a list of all shows from the backend
	data = backend.getShows()

	print('''
	<p>
	<div class="sidenav">
	<h1><center>Browse shows</center></h1>
	<table border=0>
	''')

	# Loop through tuple of shows and print out a link to each
	for row in data:
		(sid, tvshow) = row

		print('''
		<tr>
			<td><a href="?sid=%s">%s</a></td>
		</tr>
		''' % (sid, tvshow))

	print('''
	</table>
	</div>
	''')

def showShowPage(data, reviews):
	'''This function handles printing out information about a show and all of its
	reviews and ratings, takes tuples of show data and user reviews as parameters'''

	# Extract variables about show from data param
	(sid, tvshow, avgrating, img, numreviews) = data[0]

	# Printing HTML head
	htmlHead(tvshow)

	print('''
	<div class="showinfo">
		<table border=0>
			<td><img src="%s" width=250><td>
			<table border=0>
				<tr><center>Average rating: %.2f</center></tr>
	''' % (img, avgrating))

	# Printing correct grammar based upon number of reviews for show
	if (numreviews == 1):
		print('''
				<tr><center>Based on 1 review</center><tr>
		''')
	else:
		print('''
				<tr><center>Based on %s reviews</center></tr>
		''' % numreviews)

	print('''
				<form>
					<br><tr><font face="Arial" size="-1">Enter your username to add this show to your watchlist:</font></tr>
					<br><center><input type="text" name="userid" required></center>
					<tr><input type="hidden" name="sid" value="%s"></tr>
					<tr><input type="hidden" name="tvshow" value="%s"></tr>
					<br><tr><center><input type="submit" name="addwatchlist" value="Add to watchlist" id="submit"></center></tr>
				</form>
			</table>
	''' % (sid, tvshow))

	# Printing out reviews
	print('''
		</table>
	</div>
	<h2>Reviews for %s</h2>
	''' % tvshow)

	# If there do not exist any reviews for the show yet
	if (len(reviews) == 0):
		print('''
		<p>
		There are no reviews for this show yet, be the first to leave one!
		</p>
		''')
	# If there are reviews, print them out as part of the reviews class
	else:
		print('''
		<div class="lists">
			<table border=1>
				<tr>
					<td><center><b>User</b></center></td>
					<td><center><b>Rating</b></center></td>
					<td><center><b>Review</b></center></td>
				<tr>
		''')
		# Print and format each review
		for row in reviews:
			(userid, rating, review) = row
			print('''
				<tr>
					<td><a href="?userid=%s">%s</td>
					<td><center>%s</center></td>
					<td>%s</td>
				</tr>
			''' % (userid, userid, rating, review))
		print('''
			</table>
		</div>
		''')

	# Print out the reiew form underneath with the appropriate show id passed
	# in as a hidden form variable
	showReviewForm(sid)

def showReviewForm(sid):
	'''This function handles printing out the form for a user to review a show'''

	print('''
	<h2>Review this show!</h2>
	<p>
	<form>
		<table border=0>
			<tr>
				<th align="left"><label>Username:</label></th>
				<th align="left"><input type="text" name="userid" required></th>
			</tr>

			<tr>
				<th align="left"><label>Rating:</label></th>
				<th align="left">
					<select name = "rating" required>
						<option value="1">1</option>
						<option value="2">2</option>
						<option value="3">3</option>
						<option value="4">4</option>
						<option value="5">5</option>
						<option value="6">6</option>
						<option value="7">7</option>
						<option value="8">8</option>
						<option value="9">9</option>
						<option value="10">10</option>
					</select>
				</th>
			</tr>

			<tr>
				<th align="left"><label>Review:</label></th>
				<th><textarea name="review" rows="3" cols="60" required></textarea>
			</tr>
		</table>
			<input type="hidden" name="sid" value="%s">
			<br><th align="left"><input type="submit" name="addreview" value="Submit review" id="submit"></th>
	</form>
	''' % sid)

def showUpdateBioForm(userdata):
	'''This function handles printing out and prefilling the form to change a user's
	bio, takes a tuple of userdata as a parameter'''

	# Extract user info from passed in userdata tuple
	(userid, bio) = userdata[0]

	print('''
	<html>
		<head>
			<title>bingeList</title>
			<link rel="stylesheet" type="text/css" href="bingelist.css">
			<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins">
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
			<link rel="shortcut icon" type="image/png" href="http://i1225.photobucket.com/albums/ee381/enix-directory/Pixels/a_tvrosinha.gif"/>
		</head>
	<body>
	<h2>Updating bio for %s</h2>
	<p>
	<form>
		<table border=0>
			<tr>
				<th align="left"><label>Bio:</label></th>
				<th><textarea name="bio" rows="3" cols="60">%s</textarea>
			</tr>
		</table>
		<input type="hidden" name="userid" value="%s">
		<br><th align="left"><input type="submit" name="bioupdated" value="Update bio" id="submit"></th>
	</form>
	''' % (userid, bio, userid))


def showUserProfile(userdata, userreviews):
	'''This function handles printing out a user's profile and all of the shows
	they have reviewed'''

	# Extract user data from passed in userdata tuple
	(userid, bio) = userdata[0]

	# Concat string for the title of the page and pass it in 
	# as param to function to print html head
	title = userid + '\'s profile'
	htmlHead(title)
	
	# User hasn't set a bio yet
	if (bio == ''):
		print('''
		<p>
			<font face="Arial" size="-1">This user has not yet set a bio</font>
			<form>
				<div class="button">
					<input type="hidden" name="userid" value="%s">
					<th align="left"><input type="submit" name="updatebio" value="Edit bio" id="submit"></th>
				</div>
			</form>
		</p>
		<h2>Reviews by %s</h2>
		''' % (userid, userid))

	# User has set a bio so we can print it
	else:
		print('''
		<p>
			<b><i>USER BIO:</i></b>
			<font face="Arial" size="-1"><br>%s</font>
			<form>
				<div class="button">
					<input type="hidden" name="userid" value="%s">
					<th align="left"><input type="submit" name="updatebio" value="Edit bio" id="submit"></th>
				</div>
			</form>
		</p>
		<h2>Reviews by %s</h2>
		''' % (bio, userid, userid))

	# This user hasn't reviewed any shows yet
	if (len(userreviews) == 0):
		print('''
		<p>
		This user hasn't reviewed any shows yet.
		</p>
		''')
	# The user has reviwed shows so we need to print them out
	else:
		print('''
		<div class="lists">
			<table border=1>
				<tr>
					<td><center><b>Show</b></center></td>
					<td><center><b>Rating</b></center></td>
					<td><center><b>Review</b></center></td>
				</tr>
		''')
		# Loop through tuple of user reviews and print them all out
		for row in userreviews:
			(tvshow, rating, review, sid) = row
			print('''
				<tr>
					<td><a href="?sid=%s">%s</td>
					<td><center>%s</center></td>
					<td>%s</td>
				</tr>
			''' % (sid, tvshow, rating, review))

		print('''
			</table>
		</div>
		''')

	# Get a user's watchlist from the backend
	watchlist = backend.getWatchlist(userid)
	# Show the user's watchlist with a helper function
	showWatchlist(userid, watchlist)

	# Get a tuple of similar users from the backend
	users = backend.getSimilarUsers(userid)

	print('''
	<h2>Users who watch the same shows as %s</h2>
	''' % userid)

	# No registered users have reviwed any of the same shows
	if (len(users) == 0):
		print('''
		<p>
		No similar users found.
		</p>
		''')
	# Print out similar users
	else:
		print('''
		<div class="lists">
			<table border=1>
		''')
		# Loop through tuple of users and print them all out
		for i in users:
			print('''
				<tr>
					<td><a href="?userid=%s">%s</td>
					<td>%s</td>
				</tr>
			''' % (i[0], i[0], i[1]))

		print('''
			</table>
		</div>
		''')

def showWatchlist(userid, watchlist):
	'''This function takes a tuple of shows that a user wants to watch as a parameter
	and prints them out'''

	print('''
	<h2>%s\'s watchlist</h2>
	''' % userid)

	# User's watchlist is empty
	if (len(watchlist) == 0):
		print('''
		<p>
		This user hasn't added anything to their watchlist yet.
		</p>
		''')
	# User has a watchlist and we want to print it out
	else:
		print('''
		<div class="lists">
			<table border=0>
		''')
		# Loop through tuple of watchlist and print each show out
		for row in watchlist:
			(userid, tvshow, sid) = row
			print('''
			<tr>
				<form>
					<td><a href="?sid=%s">%s</td>
					<td><button class="btn" type="submit" name="deletewatchlist" value="delete from watchlist"><i class="fa fa-close"></i></button></td>
					<input type="hidden" name="userid" value="%s">
					<input type="hidden" name="sid" value="%s">
				</form>
			<tr>
			''' % (sid, tvshow, userid, sid))
		print('''
			</table>
		</div>
		''')

def displayErr(val):
	'''This function prints out an error if the user is trying to add a show to the
	watchlist that's already there or that they've already watched/reviewed or
	if they try to review a show that they've already reviewed '''

	# Show is already in watch list
	if (val == 'already'):
		print('''
		<font color="red">This show is already in the watchlist</font>
		''')
	# Show has already been reviewed
	else:
		print('''
		<font color="red">You've already reviewed this show!</font>
		''')

# main logic controller
if __name__ == '__main__':
	# HTTP Headers
	print('Content-type: text/html')
	print # blank line

	form = cgi.FieldStorage()

	# We want to do something that has to do with a user
	if ('userid' in form):
		# A user wants to add a show to their watchlist
		if ('addwatchlist' in form):
			userid = form['userid'].value
			sid = form['sid'].value
			tvshow = form['tvshow'].value
			val = backend.addToWatchlist(userid, tvshow, sid)
			# If a user has already reviewed this show or added it to their watchlist
			# Display an error message
			if (val == 'reviewed' or val == 'already'):
				displayErr(val)
				sid = form['sid'].value
				data = backend.getOneShow(sid)
				reviews = backend.getReviews(sid)
				showShows()
				showShowPage(data, reviews)
			# Show successfully added to watchlist
			else:
				userreviews = backend.getUserReviews(userid)
				userdata = backend.getUserData(userid)
				showUserProfile(userdata, userreviews)
				showShows()
		# User wants to write a review for a show
		elif ('addreview' in form):
			userid = form['userid'].value
			rating = form['rating'].value
			review = form['review'].value
			sid = form['sid'].value
			val = backend.addReview(userid, rating, review, sid)
			# If the user has already reviewed this show, display an error message
			if (val == 'reviewed'):
				displayErr(val)
			data = backend.getOneShow(sid)
			reviews = backend.getReviews(sid)
			showShows()
			showShowPage(data, reviews)
		# User wants to update their bio
		elif ('updatebio' in form):
			userid = form['userid'].value
			userdata = backend.getUserData(userid)
			showShows()
			showUpdateBioForm(userdata)
		# User has updated their bio
		elif ('bioupdated' in form):
			bio = form['bio'].value
			userid = form['userid'].value
			backend.updateBio(userid, bio)
			userreviews = backend.getUserReviews(userid)
			userdata = backend.getUserData(userid)
			showUserProfile(userdata, userreviews)
			showShows()
		# User wants to delete a show from their watchlist
		elif ('deletewatchlist' in form):
			userid = form['userid'].value
			sid = form['sid'].value
			backend.deleteWatchlist(userid, sid)
			userreviews = backend.getUserReviews(userid)
			userdata = backend.getUserData(userid)
			showUserProfile(userdata, userreviews)
			showShows()
		# We want to just show a user's profile page
		else:
			userid = form['userid'].value
			userreviews = backend.getUserReviews(userid)
			userdata = backend.getUserData(userid)
			watchlist = backend.getWatchlist(userid)
			showUserProfile(userdata, userreviews)
			showShows()
	# We just want to display a show's page
	elif ('sid' in form):
		sid = form['sid'].value
		data = backend.getOneShow(sid)
		reviews = backend.getReviews(sid)
		showShows()
		showShowPage(data, reviews)
	# We just want to display the home page
	else:
		showHome()
		showShows()
	# Print out the HTML tail for the page
	htmlTail()








