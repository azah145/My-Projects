
class Security:
	def __init__(self,attempts=3,password='Taxonomy'):
		self.attempts = 3
		self.taxonomy = 'Taxonomy'
	def authentication(self):
		while self.attempts > 0:
			user_input = input("Please enter the password before accessing the database ")
			if user_input != self.taxonomy and self.attempts > 0:
				self.attempts -= 1
				if self.attempts == 1:
					print("Sorry this password is not correct, you can try 1 more time ")
				elif self.attempts <= 3 and self.attempts > 1:
					print(f"Sorry this password is not correct, you can try {self.attempts} more times ")
			else:
				print('Access Granted')
				break
		else:
			print("Too many incorrect attempts")
			exit() 


		
s = Security()

s.authentication()
