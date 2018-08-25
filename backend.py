# Sophia Fondell
# sfondell@bu.edu
# CS 108: Final Project - bingeList - backend.py
# This file handles interacting with and manipulating the various tables 
# and data in the MySQL database
# URL: http://cs-webapps.bu.edu/cgi-bin/cs108/sfondell/bingeList/render.py

import render
import MySQLdb as db
import time
import cgi

def getConnnectionAndCursor():
	'''This function takes no params, connects to the database and returns
	the Connection and Cursor objects.'''
	conn = db.connect(host="localhost",
					user="sfondell",
					passwd="8570",
					db="cs108_sfondell_project")

	cursor = conn.cursor()
	return conn, cursor

def addUser(userid):
	'''A middleware function that takes a userid as a parameter and enters
	this value into the SQL table of statuses and ALSO enters this new user's
	relationship with all TV Shows in the system into the relationships table,
	does not return anything'''

	conn, cursor = getConnnectionAndCursor()

	# Adding the new user into the users table

	sql = '''
	INSERT INTO users
	VALUES ('0', %s, '')
	'''

	param = (userid, )
	cursor.execute(sql, param)
	conn.commit()

	# Getting a list of all TV Shows

	sql = '''
	SELECT sid, tvshow 
	FROM shows
	'''

	cursor.execute(sql)
	data = cursor.fetchall()

	# Inserting an entry for each show into relationships table

	for row in data:
		(sid, tvshow) = row
		sql = '''
		INSERT INTO relationships
		(userid, tvshow, sid)
		VALUES (%s, %s, %s)
		'''
		params = (userid, tvshow, sid)
		cursor.execute(sql, params)
		conn.commit()

	# Close connection and clean up

	cursor.close()
	conn.close()

def getShows():
	'''Middleware function that takes no params and returns a tuple of all shows
	in the database'''

	conn, cursor = getConnnectionAndCursor()

	# Query database for all shows
	sql = '''
	SELECT sid, tvshow
	FROM shows
	ORDER BY tvshow
	'''

	cursor.execute(sql)
	data = cursor.fetchall()
	cursor.close()
	conn.close()
	return data

def getOneShow(sid):
	'''Middleware function that takes a show id as a parameter and returns all 
	information stored in the database about a show'''

	conn, cursor = getConnnectionAndCursor()

	# Select information about one show
	sql = '''
	SELECT *
	FROM shows
	WHERE sid=%s
	'''

	param = (sid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()
	conn.close()
	cursor.close()
	return data

def getReviews(sid):
	'''Middleware function that takes a show id as a parameter and returns all 
	reviews of a show'''

	conn, cursor = getConnnectionAndCursor()

	# Getting all reviews for a show
	sql = '''
	SELECT userid, rating, review
	FROM relationships
	WHERE sid=%s AND
	watched=1
	'''

	param = (sid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()
	conn.close()
	cursor.close()
	return data

def addReview(userid, rating, review, sid):
	'''Middleware function that takes a userid, rating, review and show id as
	parameters and puts a new show review in the database after checking to see
	if the user already exists'''

	conn, cursor = getConnnectionAndCursor()

	# Make sure user has not already reviwed the show (this is the first check
	# because if a user does not already exist they can't have reviewed a show)
	sql = '''
	SELECT *
	FROM relationships
	WHERE userid=%s AND
	sid=%s AND watched=1
	'''

	params = (userid, sid)
	cursor.execute(sql, params)
	data = cursor.fetchall()

	# If something is returned then the user exists and has already reviewed
	# the show so we can return this and exit out of the function
	if (len(data) != 0):
		return 'reviewed'

	# Query to see if this user is already in the database
	sql = '''
	SELECT *
	FROM users
	WHERE userid=%s
	'''

	param = (userid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()

	# If the user is not already in the database we need to add them
	if (len(data) == 0 or data == None):
		addUser(userid)

	# If this show is in the user's watchlist we want to remove it
	# Because now they have watched/reviewed it
	sql = '''
	DELETE FROM watchlist
	WHERE userid=%s AND
	sid=%s
	'''

	params = (userid, sid)
	cursor.execute(sql, params)
	conn.commit()

	# Updating information in relationships table
	sql = '''
	UPDATE relationships
	SET watched=1,
	rating=%s,
	review=%s
	WHERE sid=%s AND
	userid=%s
	'''

	params = (rating, review, sid, userid)
	cursor.execute(sql, params)
	conn.commit()

	# Getting show review information so we can update it accordingly
	sql = '''
	SELECT avgrating, numreviews
	FROM shows
	WHERE sid=%s
	'''

	param = (sid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()
	(avgrating, numreviews) = data[0]

	# Calculating new show average
	newavg = (avgrating * numreviews + float(rating)) / (numreviews + 1)
	numreviews += 1

	# Updating show review information
	sql = '''
	UPDATE shows
	SET avgrating=%s,
	numreviews=%s
	WHERE sid=%s
	'''

	params = (newavg, numreviews, sid)
	cursor.execute(sql, params)
	conn.commit()
	conn.close()
	cursor.close()

	return 'okay'

def getUserReviews(userid):
	'''Middleware function that takes a userid as a parameter and returns all 
	of the reviews a user has left'''

	conn, cursor = getConnnectionAndCursor()

	# Getting user's reviews
	sql = '''
	SELECT tvshow, rating, review, sid
	FROM relationships
	WHERE userid=%s AND
	watched=1
	'''

	param = (userid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()
	conn.close()
	cursor.close()
	return data

def getUserData(userid):
	'''Middleware function that takes a userid as a parameter and returns a 
	user's userid and their bio'''

	conn, cursor = getConnnectionAndCursor()

	# Getting user information from db
	sql = '''
	SELECT userid, bio
	FROM users
	WHERE userid=%s
	'''

	param = (userid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()
	conn.close()
	cursor.close()
	return data

def getUsers():
	'''Middleware function that takes no parameters and returns all users in the
	system'''

	conn, cursor = getConnnectionAndCursor()

	# Getting all users from db
	sql = '''
	SELECT userid, bio
	FROM users
	'''

	cursor.execute(sql)
	data = cursor.fetchall()
	conn.close()
	cursor.close()
	return data

def updateBio(userid, bio):
	'''Middleware function that takes a userid and a new bio as parameters and
	updates that user's bio in the database'''

	conn, cursor = getConnnectionAndCursor()

	# Updating bio for specified user
	sql = '''
	UPDATE users
	SET bio=%s
	WHERE userid=%s
	'''

	params = (bio, userid)
	cursor.execute(sql, params)
	conn.commit()
	conn.close()
	cursor.close()

def getWatchlist(userid):
	'''Middleware function that takes a userid as a parameter and returns all
	of the shows on that user's watchlist'''

	conn, cursor = getConnnectionAndCursor()

	# Querying database for watchlist shows
	sql = '''
	SELECT userid, tvshow, sid
	FROM watchlist
	WHERE userid=%s
	'''

	param = (userid, )
	cursor.execute(sql, param)
	data = cursor.fetchall()
	conn.close()
	cursor.close()
	return data

def addToWatchlist(userid, tvshow, sid):
	'''Middleware function that takes a userid and a show id as parameters and
	adds the show to the specified user's watchlist'''

	conn, cursor = getConnnectionAndCursor()

	# Check to make sure user hasn't already watched/reviewed this show
	sql = '''
	SELECT * FROM
	relationships
	WHERE userid=%s AND
	tvshow=%s AND watched=1
	'''

	params = (userid, tvshow)
	cursor.execute(sql, params)
	data = cursor.fetchall()

	if (len(data) != 0):
		# Display error message because the user has already watched this show
		return 'reviewed'

	# Check to make sure it's not already in the watchlist
	sql = '''
	SELECT * FROM
	watchlist WHERE
	userid=%s AND
	tvshow=%s
	'''

	params = (userid, tvshow)
	cursor.execute(sql, params)
	data = cursor.fetchall()

	if (len(data) == 0 or data == None):
		# Adding to watchlist table
		sql = '''
		INSERT INTO watchlist
		VALUES ('0', %s, %s, %s)
		'''

		params = (userid, tvshow, sid)
		cursor.execute(sql, params)
		conn.commit()
		conn.close()
		cursor.close()
		# Returning so that already in watchlist error is not also returned
		return 'added'

	# This show is already in the watchlist
	return 'already'


def deleteWatchlist(userid, sid):
	'''Middleware function that takes a userid and a show id as parameters and
	deletes the specififed show from the user's watchlist'''

	conn, cursor = getConnnectionAndCursor()

	# Removing from watchlist
	sql = '''
	DELETE FROM watchlist
	WHERE userid=%s AND
	sid=%s
	'''

	params = (userid, sid)
	cursor.execute(sql, params)
	conn.commit()
	conn.close()
	cursor.close()

def getSimilarUsers(userid):
	'''Middleware function that takes a userid and returns a list of users that
	have watched/reviewed at least one of the same shows'''

	conn, cursor = getConnnectionAndCursor()

	# Getting a list of shows that this user has reviewed
	reviews = getUserReviews(userid)
	# If this user hasn't watched anything we can't return a list of similar users
	if (len(reviews) == 0):
		return None

	# Getting a list of shows that this user has reviewed
	shows = []
	for row in reviews:
		(tvshow, rating, review, sid) = row
		shows.append(tvshow)

	# We want to loop through the list of shows that this user has reviewed so that
	# we can build up a list of users who have also reviewed the same shows
	users = []
	for show in shows:
		sql = '''
		SELECT relationships.userid,
		users.bio
		FROM relationships
		INNER JOIN users
		ON relationships.userid = users.userid
		WHERE relationships.tvshow = %s AND
		relationships.watched=1
		'''

		param = (show, )
		cursor.execute(sql, param)
		data = cursor.fetchall()
		# Make sure we haven't already added that user to the user list
		# and that it's not the original user in question
		for row in data:
			(user, bio) = row
			if ([user, bio] not in users and user != userid):
				users.append([user, bio])

	conn.close()
	cursor.close()
	return users















