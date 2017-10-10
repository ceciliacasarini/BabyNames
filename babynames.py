__author__ = "Cecilia Casarini"

# This code defines a class and various methods to analyze a text file containing baby names
# Developed during the course Compuer Programming for Speech and Language Processing at the University of Edinburgh (2015 - 2016)


class Babies:


    def __init__(self, filename=None):
        self.boy=self.read_names_from_file(filename, 'BOY')    # Call of a function (below) to populate one dictionary for boys and one for girls
        self.girl=self.read_names_from_file(filename, 'GIRL')
        

    def read_names_from_file(self, filename, gender): # Definition of a method to store data from a file
        namecount={}                                  # Data will be stored in the 'namecount' dictionary:
        for line in open(filename):                       # the keys will be the names and the values their frequencies
            data_list=line.strip().split()            # This statement splits the text in 'filename' and creates a list of data
            if data_list[1]==gender:                  # This 'if' allows to create two different dictionaries for boys and girls
                if data_list[0] in namecount:         # This 'if' attaches to every name its frequency
                    namecount[data_list[0]] += 1
                else:
                    namecount[data_list[0]] = 1
        return namecount

 
    def get_total_births(self, gender=None):            # Method to obtain the total number of births
        total=0                                         # The variable 'total' will count the total number of births
        if (type(gender)==str):                         # This 'if' checks the gender input
            gender=gender.upper()
        if gender=='BOY':
            for name in self.boy.keys():                # This 'for' loop (For boys, girls, or not specified gender)
                total += self.boy[name]                     # adds name frequencies (the value in our dictionary) to the variable 'total'
            return total
        elif gender=='GIRL':
            for name in self.girl.keys():
                total += self.girl[name]
            return total
        elif gender==None:
            for name in self.boy.keys():
                total += self.boy[name]
            for name in self.girl.keys():
                total += self.girl[name]
            return total
        else:
            print '\nGender value not accepted\n'
    

    def get_names_beginning_with(self, first_char, gender=None):        # Method that returns an alph. sorted list of names starting with the same input character
        same_letter=[]                                                  # The list 'same_letter' will store the names with the same initial
        if (type(gender)==str):                                         # This 'if' checks the gender input
            gender=gender.upper()
        if (type(first_char)==str):                                     # These 'if's checks the 'first_char' input
            first_char=first_char.upper()
        if (type(first_char)!=str or len(first_char)!=1 or str.isalpha(first_char)!=True):
            print "\nFirst character non accepted\n"
        elif gender=='BOY':
            for name in self.boy.keys():
                if (name[0]==first_char and name not in same_letter):   # Comparing the 'first_char' input with the first character of each name
                    same_letter.append(name)                            # Population of the list
            return sorted(same_letter)                                      # alphabetically sorted
        elif gender=='GIRL':
            for name in self.girl.keys():
                if (name[0]==first_char and name not in same_letter):
                    same_letter.append(name)
            return sorted(same_letter)
        elif gender==None:
            for name in self.boy.keys():
                if (name[0]==first_char and name not in same_letter):
                    same_letter.append(name)
            for name in self.girl.keys():
                if (name[0]==first_char and name not in same_letter):
                    same_letter.append(name)
            return sorted(same_letter)
        else:
            print '\nGender value not accepted\n'
                

    def get_top_N(self, N, gender=None):        # Method that returns the list of the top N tuples ordered from most-common to least-common
        top_names=[]                            # The list 'top_names' will store the top N tuples ordered
        test_gender=True
        if (type(gender)==str):                 # This 'if' checks the gender input
            gender=gender.upper()
        if (type(N)!=int or N<=0):              # This 'if' checks the integer input
            print "\nInteger non accepted\n"
        elif gender=='BOY':
            top_names.extend(sorted(self.boy.items(), key=lambda x: x[1], reverse=True))    # This statement adds tuples and reverses them, considering their second component. 
        elif gender=='GIRL':                                                                    # Therefore the sorting is based on the frequency of each name.
            top_names.extend(sorted(self.girl.items(), key=lambda x: x[1], reverse=True))
        elif gender==None:
            mixed=[]                                        # List that will store only names
            test_list=[]                                    # List that will store tuples (name,frequency)
            test_list.extend(self.boy.items())              # Population of test_list first with boys
            test_list.extend(self.girl.items())                 # and then with girls
            for i in test_list:
                copy=-1
                name="".join(map(str,i[0]))                 # This statement converts the first component of the tuple 'i' in the string 'name'
                if name not in mixed:                       # If there's no tuple in 'mixed' list with the given 'name'
                    mixed.append(name)                          # add it to 'mixed'
                    top_names.append(i)                         # and add the whole tuple 'i' to 'top_names'
                else:
                    p=i[1]
                    m=0
                    for j in top_names:                     # Otherwise, check every tuple in 'top_names' from the beginning
                        test_name="".join(map(str,j[0]))
                        if test_name==name:                     # and when the first tuple with the same name is found
                            p+=j[1]                             # sum their frequencies
                            if copy==-1:
                                copy=m                          # ('copy' will be the index of the first tuple with the wanted name)
                        m+=1
                    top_names[copy]=(name,p)                    # and update the tuple of index 'copy'
            top_names.sort(key=lambda x: x[1], reverse=True)
        else:
            test_gender=False
            print '\nGender value not accepted\n'
        if test_gender:
            if N < len(top_names):                          # This 'if' checks the integer 'N'
                if top_names[N][1]==top_names[N-1][1]:      # If with the given 'N' the module returns just some of the names with a specific frequency
                    n=0
                    m=0
                    for i in top_names:
                        if i[1]==top_names[N][1]:
                            n+=1                                # count how many tuples have that specific frequency
                            if i in top_names[0:N]:             # and how many of them are already included in top_names[0:N]
                                m+=1
                    print '\nThere are other %d name(s) occurring exactly %d time(s)' %(n-m,top_names[N][1])
                    print 'To visualize them all, use "get_top_N(%d)"\n' %(N+n-m)
                return top_names[0:N]
            elif N==len(top_names):
                return top_names
            else:
                print "\nInteger too large\n"
                return top_names


    def get_gender_ratio(self, gender):     # Method that returns the ratio between the number of boys or girls and the total number of births
        ratio=float(0)                      # 'Ratio' will be a float number
        if (type(gender)==str):             # This 'if' checks gender input
            gender=gender.upper()
        if gender =='BOY':
            ratio=self.get_total_births('BOY')/float(self.get_total_births())  # Converting the total number of births to float and calculating the ratio
        elif gender =='GIRL':
            ratio=self.get_total_births('GIRL')/float(self.get_total_births())
        else:
            print '\nGender value not accepted\n'
        return ratio

