from dfa import DFA
from nfa import NFA
from collections import deque
from DataStructures import Stack
from DataStructures import SyntaxTreeNode
from regex import RegEx

class InvalidToken(Exception):
	""" 
	Raised if while scanning for a token,
	the lexical analyzer cannot identify 
	a valid token, but there are still
	characters remaining in the input file
	"""
	pass

class Lex:
	def __init__(self, regex_file, source_file):
		"""
		Initializes a lexical analyzer.  regex_file
		contains specifications of the types of tokens
		(see problem assignment for format), and source_file
		is the text file that tokens are returned from.
		"""
		f = open(regex_file)
		self.alphabet_str = f.readline().strip()[1:-1]
		self.alphabet_set = set()
		self.token_dict = {}
		#this dict will be used to see which regular expression was scanned first.
		self.token_heirachy = {}
		heirachy_counter = 1
		next_regex_str = f.readline().strip().split()
		while(next_regex_str):
			regex_object = RegEx(filename=None,regex_str=next_regex_str[1][1:-1],alphabet_str=self.alphabet_str)
			#now set key value pair in dictonary
			self.token_dict[next_regex_str[0]] = regex_object
			#set key value pair for heirachy mapping
			self.token_heirachy[next_regex_str[0]] = heirachy_counter
			heirachy_counter+=1
			#set alphabet_set equal to parsed one in file
			self.alphabet_set = regex_object.alphabet_set
			#initalize for next iteration
			next_regex_str = f.readline().strip().split()
		
		#Now do part 2 and initalize any variables needed from the source_file
		f = open(source_file)
		self.potential_tokens = []
		line = f.readline().strip().split()
		while(line):
			for item in line:
				self.potential_tokens.append(item)
			line = f.readline().strip().split()


	def next_token(self):
		"""
		Returns the next token from the source_file.
		The token is returned as a tuple with 2 item:
		the first item is the name of the token type (a string),
		and the second item is the specific value of the token (also
		as a string).
		Raises EOFError exception if there are not more tokens in the
		file.
		Raises InvalidToken exception if a valid token cannot be identified,
		but there are characters remaining in the source file.
		"""
		token_str = ""
		return_val_tuple = None, None,None
		char_index = -1

		if(len(self.potential_tokens)==0):
			raise EOFError
		#iterate over all chars
		for char in self.potential_tokens[0]:
			if(char not in self.alphabet_set):
				raise InvalidToken
			token_str+=char
			char_index+=1
			for token_name, regex_object in self.token_dict.items():
				#run the simulate method to see if the str is accepted
				if(regex_object.simulate(token_str)):
					if(not return_val_tuple[0] or (return_val_tuple[2]!=char_index)):
						#that means that regex_object accepted the following string
						return_val_tuple = token_name, token_str, char_index
					else:
						if((return_val_tuple[2]==char_index) and self.token_heirachy[token_name]<self.token_heirachy[return_val_tuple[0]]):
							return_val_tuple = token_name, token_str, char_index
		#If this value was not set than it is invalid token
		if(not return_val_tuple[0]):
			raise InvalidToken
		final_char_index = return_val_tuple[2]
		if(final_char_index==(len(self.potential_tokens[0])-1)):
			self.potential_tokens.pop(0)
		else:
			self.potential_tokens[0] = self.potential_tokens[0][final_char_index+1:]
		
		return return_val_tuple[0],return_val_tuple[1]


if __name__ == "__main__":
	num = 19   # can replace this with any number 1, ... 20.
			  # can also create your own test files.
	reg_ex_filename = f"regex{num}.txt" 
	source_filename = f"src{num}.txt"
	lex = Lex(reg_ex_filename, source_filename)
	try:
		count = 0
		while True:
			token = lex.next_token()
			count+=1
			print(token)
			print(count)
			print()

	except EOFError:
		pass
	except InvalidToken:
		print("Invalid token")


