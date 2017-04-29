


def getObject(s):
	
	cursor = 0
	thisObject = {}
	thisName = ""
	thisValue = None
	thisQuote = "\""
	cursorTemp = 0
	
	isError = False
	quoteWarning = False
	boolWarning = False
	allWarnings = {"isError":isError,"quoteWarning":quoteWarning,"boolWarning":boolWarning}
	
	def printErrors(warnings):
		if(warnings[isError] == True):
			print("ERROR IN JSON SYNTAX: due to syntax errors some values may not have been loaded correctly")
		if(warnings[quoteWarning] == True):
			print("WARNING: Improper JSON syntax. Only double quotes should be used for value names and strings, not single quotes. The parser should have handled this correctly though.")
		if(warnings[boolWarning] == True):
			print("WARNING: Improper JSON syntax. Boolean values should be written only in lower case and without quotes. The parser should have handled this correctly though.")
	
	def getUnknown(s,warnings):
		return(None,0)

	def getString(s,warnings):
		prev='0'
		outString = ""
		thisQuote = '\"'
		if(s[0]=='\"' or s[0]=='\''):
			thisQuote = s[0]
			if(thisQuote == "\'"):
				warnings[quoteWarning] = True
		else:
			warnings[isError] = True  ## Error check here
		for i in range(1,len(s)):
			if(s[i]==thisQuote and prev!="\\"):
				break
			elif(i==len(s)-1):
				warnings[isError] = True ## Error check here
			else:	
				outString += s[i];
				prev = s[i]
		return(outString,i) ####
		

	def getBool(s,warnings):
		if(len(s)>=4):
			if(s[0:4]=="true"):
				return(True,3)
			elif(s[0:4]=="True"):
				warnings[boolWarning]=True
				return(True,3)
			elif(s[0:4]=="TRUE"):
				warnings[boolWarning]=True
				return(True,3)	
		if(len(s)>=5):
			if(s[0:5]=="false"):
				return(False,4)
			elif(s[0:5]=="False"):
				warnings[boolWarning] = True
				return(False,4)
			elif(s[0:5]=="FALSE"):
				warnings[boolWarning] = True
				return(False,4)
		else:
			warnings[isError] = True ## Error check here
		return(None,0) ## does not return 1 because the calling function should iterate on its own
				
				
	def getNumber(s,warnings):
		outString = "0"
		isFloat = False
		for i in range(0,len(s)):
			if(s[i].isdigit()):
				outString+=s[i]
			elif(s[i] == "."):
				isFloat=True
				outString+=s[i]
			elif(s[i] == "," or s[i]=="}" or s[i]=="]" or s[i]==" "):
				i-=1
				break		
			else:
				warnings[isError] = True ## Error check here
				i-=1 #this is just so the output int is consistent with other functions
				break
		if(isFloat==False):		
			return(int(outString),i)
		else:
			return(float(outString),i)

	def getNull(s,warnings):
		if(s[0:4]=="null"): 
			return (None,3) 
		else:
			print("Error in getNull")
			return (None,0) ## if the calling funcion iterates, returning 1 may be unnecessary
		
		
	def getArray(s,warnings):
		thisList=[]
		listTemp = ""
		cursor = 0
		cursorTemp = 0 
		type = "Not checked"
		while(cursor<len(s) and s[cursor]==" "): #####
			cursor+=1
		if(s[cursor]=="["):
			cursor+=1
			while(cursor<len(s)):
				
				# check if end of array
				if(s[cursor]=="]"):
					break
				
				# continue from acceptable character ## this needs to be improved
				if(s[cursor]=="," or s[cursor]==" "):
					cursor+=1
					continue
				
				# get type of value
				type,cursorTemp = getType(s[cursor:],allWarnings)
				cursor+=cursorTemp
				
				# add value if real value
				if(type!="Unknown"):
					listTemp,cursorTemp=getValue(type,s[cursor:],allWarnings)
					cursor+=cursorTemp
					thisList.append(listTemp)
				else:
					warnings[isError] = True ## error check
				cursor+=1
		else:
			warnings[isError] = True ## error check
			
		return(thisList,cursor)



	def getType(s,warnings):
		for i in range(0,len(s)):
			if(s[i].isdigit()):
				return("Number",i)
			elif(s[i]=="\"" or s[i]=="\'"):
				return("String",i)
			elif( ((s[i]=="t" or s[i]=="T") and (len(s)-i)>=4) or ((s[i]=="f" or s[i]=="F") and (len(s)-i)>=5) ):
				return("Boolean",i)
			elif(s[i]=="["):
				return("Array",i)
			elif(s[i:i+4]=="null"):
				return("Null",i)
			elif(s[i]!=" "):
				warnings[isError] = True ## Error check here
		return("Unknown",0)
		
		
	def getValue(type,s,warnings):
		return {"String":getString,"Boolean":getBool,"Array":getArray,"Number":getNumber,"Unknown":getUnknown,"Null":getNull}[type](s,warnings)

		
		
		
	
	# ignore spaces
	while(cursor<len(s) and s[cursor]==" "):
		cursor+=1
	
	# check for improper characters, set to first occurrence of "{"
	if(cursor>len(s) or s[cursor]!="{"):
		warnings[isError] = True ##Error check here
		while(cursor<len(s) and s[cursor]=="{"):
			cursor+=1	
	cursor+=1
	

	while(cursor<len(s)):		
		# zero out values
		thisName = ""
		thisValue = None
		thisQuote = "\""
		cursorTemp=0
		
		# find quote mark
		if(cursor>len(s) or (s[cursor]!="\"" and s[cursor!="\'"]) ):
			warnings[isError] ##Error check here
		while(cursor<len(s) and (s[cursor]!="\"" and s[cursor]!="\'") ):
			cursor+=1
		thisQuote = s[cursor]
		cursor+=1
		
		# get value name
		while(cursor<len(s) and s[cursor]!=thisQuote):
			thisName+=s[cursor]
			cursor+=1
		cursor+=1
		
		# find ":"
		while(cursor<len(s) and s[cursor]!=":"):
			if(s[cursor] == " "):
				continue
			else:
				warnings[isError] ## error check
			cursor+=1
		cursor+=1
		
		# find value
		type,cursorTemp = getType(s[cursor:],allWarnings)
		cursor+=cursorTemp
		if(type!="Unknown"):
				thisValue,cursorTemp=getValue(type,s[cursor:],allWarnings)
				cursor+=cursorTemp
		else:
			warnings[isError] ## error check
		thisObject[thisName] = thisValue
		cursor+=1
		
		
		# Check for next key/value pair or end of object
		while(cursor<len(s)):
			if(s[cursor]=="}"):
				printErrors(allWarnings)
				return(thisObject)
			elif(s[cursor]==" "):
				cursor+=1
				continue
			elif(s[cursor]==","):
				break
			else:
				warnings[isError] = True ## error check
				cursor+=1
				continue				
		cursor+=1
	printErrors(allWarnings)
	return(thisObject)
	



#print(getObject("{\"huh\":\'words\',\"some\":\"stuff\",\"chitchat\":[23,\"sf4rf\",null,true,false,[\"this\" ,  \"that\"  ,null  ,  true, false , 2345.234 ]]}"))



