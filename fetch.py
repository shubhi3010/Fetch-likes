#Python file to count the total posts liked by a friend on facebook.
import facebook
import sys
import codecs
import json
import requests
import MySQLdb
# creating connection to database
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="XYZ",  		  # your password
                     db="fb") 
cursor = db.cursor()
'''
db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
'''
access_token = 'YOUR ACCESS TOKEN'
graph = facebook.GraphAPI(access_token)

payload = {'access_token' : access_token}
r = requests.get('https://graph.facebook.com/me/feed', params=payload)
result = json.loads(r.text)

next_page = result['paging']['next']
while next_page:
	posts=result['data']

	for post in posts:
		myfacebook_likes_info = graph.get_connections(post['id'], 'likes?summary=1')
		next_pages = 1
		while next_pages:
			for s in myfacebook_likes_info['data']:
				n=s['name']
				q2='select count(*) from fbl1 where name=("%s");'%(n)
				cursor.execute(q2)
				result = cursor.fetchone()
				found = result[0]
				if found == 0: 
					q='insert into fbl1(name,count) values("%s",%d);'%(n,1)
					cursor.execute(q)
					db.commit()
				else:
					q='Update fbl1 set count=count+1 where name=("%s");'%n
					cursor.execute(q)
					db.commit()
			
			if 'paging' in myfacebook_likes_info:
				if 'next' in myfacebook_likes_info['paging']:
					#print "jjjjjjjjjj"
					myfacebook_likes_info = json.loads(requests.get(myfacebook_likes_info['paging']['next']).text)
					next_pages=1
				else:
					#print "next not found"
					#print "xxxxxxx"
					next_pages=0
			else:
				#print "sssssss"
				next_pages=0

	result = json.loads(requests.get(next_page).text)
	if 'paging' in result:
		if 'next' in result['paging']:
			next_page=result['paging']['next']
		else:
			#print "next not found"
			next_page=None  
	else:
		#print "paging not found"
		next_page=None
	    		    
	
    
	    	

   	
     

q1 = "select * from fbl1;"
# Open database connection
#db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )

# prepare a cursor object using cursor() method
#cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute(q1)

# Fetch a single row using fsetchone() method.
results = cursor.fetchall()
for row in results:
    fname = row[0]
    count = row[1]
      # Now print fetched result
    print "fname=%s,count=%d" % \
             (fname,count)
# disconnect from server
db.close()

#It collects the likes per user on total posts
#list=["Friend list"] #contain friendlist
#likes=0
