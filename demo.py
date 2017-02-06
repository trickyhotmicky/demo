from google.appengine.ext import ndb
import webapp2
import json


class Book(ndb.Model): 
	title = ndb.StringProperty(required =True)
	isbn = ndb.IntegerProperty()
	genre = ndb.StringProperty(repeated = True)
	author = ndb.StringProperty()
	checkedIn = ndb.BooleanProperty()
	
class Customer(ndb.Model):
	name = ndb.StringProperty(required = True)
	balance = ndb.FloatProperty()
	checked_out = ndb.StringProperty(repeated=True)
	
class CheckOutHandler(webapp2.RequestHandler):
	#check out a book, updates the book the customer.check_out field
    def put(self, cust_id=None, book_id=None):
        cust_id = cust_id.replace('/','')
        if cust_id and book_id:
            customer = ndb.Key(urlsafe=cust_id).get()
            book = ndb.Key(urlsafe=book_id).get()
            customer.checked_out.append('/books/' + book_id)
            customer.put()
            book.checkedIn = false 
            book.put()
			
class FullJsonBooksHandler(webapp2.RequestHandler):
	# displays the checked out json objects for a customer 
	def get(self, cust_id=None):
		cust_id = cust_id.replace('/','')
		if cust_id:
			customer = ndb.Key(urlsafe=cust_id).get()
			custBooks = customer.checked_out
			list_book = list()
			
			myInt = 0  
			for item in custBooks:
				book_key = os.path.relpath(custBooks[myInt], '/books/')
				list_book.append(book_key)
				myInt = myInt + 1
			self.response.write(json.dumps(list_book))
		   
	
class BooksHandler(webapp2.RequestHandler): 
	#adds a new book
	def post(self):
		book_data = json.loads(self.request.body)
		new_book = Book(title = book_data['title'], isbn = book_data['isbn'], author = book_data['author'], genre = book_data["genre"], checkedIn = book_data['checkedIn'])
		new_book.put()
		book_dict = new_book.to_dict()
		book_dict['self'] = '/books' + new_book.key.urlsafe()
		
		self.response.write(json.dumps(book_dict))
	
	# displays a book 
	def get(self, id = None):
		if id:
			b = ndb.Key(urlsafe = id).get()
			b_d = b.to_dict()
			b_d['self'] = "/books/" + id
			self.response.write(json.dumps(b_d))
		#lists all the checked in books  - non working 
	    # elif(self.request.get('checkedIn')):
            # checkedIn_status = self.request.get('checkedIn')
            # if checkedIn_status == true:
				# qry = Book.query(Book.checkedIn == True)
				# book_list = list()
				# for items in qry:
					# item_dict = items.to_dict()
					# item_dict['self'] = '/books/' + items.key.urlsafe()
					# item_dict['id'] = items.key.urlsafe()
					# book_list.append(item_dict)
				# self.response.write(json.dumps(book_list))
		
       
			
    # lists all the checked in books - original version  - non working 
	# def get((self.request.get('checkedIn')): 
		# checkedIn_status = self.request.get('checkedIn')
        # if checkedIn_status == "true":
            # qry = Book.query(Book.checkedIn == True)
            # book_list = list()
            # for items in qry:
                # item_dict = items.to_dict()
                # item_dict['self'] = '/books/' + items.key.urlsafe()
                # book_list.append(item_dict)
            # self.response.write(json.dumps(book_list))
			
	# updates a passed field and the set the rest properties to null
	def put(self, id = None):
		book_info = json.loads(self.request.body)
		book_object = ndb.Key(urlsafe = id).get()
		book_object.title = book_info['title']
		book_object.isbn = book_info['isbn']
		book_object.genre  = book_info['genre']
		book_oject.author = book_info['author']
		book_object.checkedIn = book_info['checkedIn']
		book_object.put()	
	
	
	#updates a passed field and keeps the rest properties unchanged
	def patch(self, id = None):
		book_info = json.loads(self.request.body)
		book_object = ndb.Key(urlsafe = id).get()
		if (book_info['title'] != null) :
			book_object.title = book_info['title']
			book_object.put()
		if(book_info['isbn'] != null ):
			book_object.isbn = book_info['isbn']
			book_object.put()
		if (book_info['genre'] != null ):
			book_object.genre = book_info['genre']
			book_object.put()
		if (book_info['author'] != null) :
			book_object.author = book_info['author']
			book_object.put()
		if (book_info['checkedIn'] != null ) :
			book_object.checkedIn = book_info['checkedIn']
			book_object.put()
			
	# deletes a book	
	def delete (self, id  = None ):
		if id:
			book_key = ndb.Key(urlsafe = id).get()
			#cust = cust_key.get()
			#url_string = cust_key.urlsafe()
			#key = Key(urlsafe = url_string)
			book_key.key.delete()		
			
class CustomersHandler(webapp2.RequestHandler): 
	# adds a new customer
	def post(self):
		customer_data = json.loads(self.request.body)
		new_customer = Customer(name = customer_data['name'], balance = customer_data['balance'], checked_out = customer_data['checked_out'])
		new_customer.put()
		customer_dict = new_customer.to_dict()
		customer_dict['self'] = '/customers' + new_customer.key.urlsafe()
		
		self.response.write(json.dumps(customer_dict))
		
	
	# displays a customer
	def get(self, id = None):
		if id:
			c = ndb.Key(urlsafe = id).get()
			c_d = c.to_dict()
			c_d['self'] = "/customers/" + id
			self.response.write(json.dumps(c_d))
			
	# updates a passed field and the set the rest properties to null
	def put(self, id = None):
		cust_info = json.loads(self.request.body)
		cust_object = ndb.Key(urlsafe = id).get()
		cust_object.name = cust_info['name']
		cust_object.balance = cust_info['balance']
		cust_object.checked_out  = cust_info['checked_out']
		cust_object.put()	
	
	
	#updates a passed field and keeps the rest properties unchanged
	def patch(self, id = None):
		cust_info = json.loads(self.request.body)
		cust_object = ndb.Key(urlsafe = id).get()
		if (cust_info['name'] != null) :
			cust_object.name = cust_info['name']
			cust_object.put()
		if(cust_info['balance'] != null ):
			cust_object.balance = cust_info['balance']
			cust_object.put()
		if (cust_info['checked_out'] != null ):
			cust_object.checked_out = cust_info['checked_out']
			cust_object.put()
			
    # deletes a customer 	
	def delete (self, id  = None ):
		if id:
			cust_key = ndb.Key(urlsafe = id).get()
			#cust = cust_key.get()
			#url_string = cust_key.urlsafe()
			#key = Key(urlsafe = url_string)
			cust_key.key.delete()
			
		
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write("hello")


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/books', BooksHandler), 
	('/books/(.*)', BooksHandler),
	('/customers', CustomersHandler), 
	('/customers/(.*)', CustomersHandler), 
	#('/books?checkedIn=(.*)', BooksHandler),
	('/books/(.*)/customers/(.*)', CheckOutHandler), 
	('customers/(.*)/books', FullJsonBooksHandler)
	
], debug=True)
