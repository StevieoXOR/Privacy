
def printDynamicCountdownTimer(countdownMsg:str = "", delayInSec:int = 10):
	from time import sleep
	from math import ceil
	assert type(countdownMsg) is str,        f"`countdownMsg` must be of type `str`. Type={type(countdownMsg)}."
	assert type(delayInSec) in [int, float], f"`delayInSec` must be of type `int` (or `float`). Type={type(delayInSec)}."
	delayInSec = (int)(ceil(delayInSec))	# Just in case a float was provided.

	print(countdownMsg, end="", flush=True)
	for i in range(delayInSec)[::-1]:
		j, numDigitsOfJ  =  i+1,  len(str(i+1))
		print(j, end="", flush=True)
		sleep(1)
		print(("\b" * numDigitsOfJ), end="")	# Backspace exactly as many times as the number of digits of the TimeRemaining value.
		print((" "  * numDigitsOfJ), end="")	# Overwrite the already-written characters (same line).
		print(("\b" * numDigitsOfJ), end="")	# Move back to the start of where the number was printed.
	print("\b" * len(countdownMsg), end="")	# Backspace exactly as many times as the number of characters in the countdown string
	# NOTE: You must include the `end=""` parameter (which prevents the default printing of the newline character) to perform a backspace.
	#       70 backspaces on a single line that contains just 5 characters will not erase any characters from any previous lines.
	# NOTE:  `flush=True` forces the string (and any previously unprinted (waiting) strings) to print to console immediately
	#        rather than being held in an invisible buffer.

	# To actually delete the backspaced characters without relying on the next-printed string to fully (hopefully not partially) overwrite them. write spaces to overwrite the backspaced characters.
	print(" " * (len(countdownMsg) + len(str(delayInSec)) ), end="\n\n")



def stripSensitiveFilepath(data:str, SLASH:str, DEBUG_LVL:int):
	import re
	# Convert string to bytestream so that file-reading and file-writing can occur, if used before this function is called.
	if type(data) is str:
		data = data.encode("utf-8")
		if DEBUG_LVL>0:
			print("\n[INFO]  Converted data from str to UTF-8 bytestream for maximum compatibility with unusual characters possibly present in binary file.")

	###########################################################################################
	# CHANGE ME! :)
	findSlash = "([/\\\\]{0,10})"	# Up to 10 contiguous slashes (like \\) are allowed to be present in text. DO NOT ENCODE THIS TO A BYTESTREAM UNTIL AFTER IT'S PULLED INTO A STRING THAT IS ABOUT TO BE ENCODED
	findAsRegex = f"C:{findSlash}Users{findSlash}(.*)challenges{findSlash}".encode("utf-8")
	leftOfRedaction, rightOfRedaction  =  r"C:\1Users\2",  r"challenges\4"
	###########################################################################################


	if DEBUG_LVL>0:
		print(f"\nLooking for all strings that match the following RegEx pattern:\n* {findAsRegex}\n")
	# findAsSingleLengthString = f"C:{SLASH}Users{SLASH}challenges{SLASH}".encode("utf-8")	# No Regex in here, no escape characters in here. Only raw characters.

	def replacementCallbackFunc(matchobj: re.Match):
		# Can't naively delete sensitive data since that messes up file's LUT of memory offsets. So, replace/overwrite it with garbage data of equivalent byte-length.
		m, idx_getAllGroups = matchobj, 0
		matchedStr       =  m.group(idx_getAllGroups)
		if DEBUG_LVL>1:
			print("\nEntire `match` object:             ", m)
			print("Matched string  (v1, byt):          ", m.string[m.start(idx_getAllGroups) : m.end(idx_getAllGroups)] )
			print("Matched string  (v2, byt):          ", matchedStr )			# Will be exact same as above line.
		if DEBUG_LVL>2:
			try:
				print("Matched string  (v1, str):            ", m.string[m.start(idx_getAllGroups) : m.end(idx_getAllGroups)].decode("utf-8") )
				print("Matched string  (v2, str):            ", matchedStr.decode("utf-8") )
				print("Escaped mstring (3, str):             ", re.escape(matchedStr).decode("utf-8") )
				print("Escaped mstring (3, byt):           ", re.escape(matchedStr) )	# This escapes everything, which is why I can't use it here...
			except:
				pass

		# Not actually critical to be in the code, hence its very high debug level.
		if DEBUG_LVL>3:
			# r"\\\\" will be counted as 4 backslashes
			# Correct, except is counting the full matched string instead of only counting what will NOT get replaced
			numDoubledUpBackslashes = sum([1  for idx in range(0,len(matchedStr)-1) if (matchedStr[idx:idx+2]==r"\\")])
			# numDoubledUpBackslashes = sum([1  for idx in range(0,len(matchedStr)-1) if (idx%2==0 and matchedStr[idx:idx+2]==r"\\")])	# Counts 6pairs instead of 8pairs
			# numDoubledUpBackslashes = ([(1,matchedStr[idx:idx+2])  for idx in range(0, len(matchedStr)-1) if matchedStr[idx:idx+2]==r"\\"])
			# numDoubledUpBackslashes = ([(1,matchedStr[idx:idx+2])  for idx in range(0, len(matchedStr)-1) if (idx%2==0 and matchedStr[idx:idx+2]==r"\\")])
			print("[UNUSED] numDoubledUpBackslashesInEntireMatch:", numDoubledUpBackslashes)
		# 
		# \1, \2, \3, \4 are each a regex backreference to a captured group.
		# match.expand(stringWithBackrefs) substitutes those captured group strings (e.g., "\1") back into the main string.
		# backrefsInUnreplacedPortion = m.expand(fr"\1 \2 \4".encode("utf-8"))	# The string to expand must be a bytestream if the matches found are a bytestream.
		# # 
		# # Erroneously thinks "\\\" is two groups of double backslashes instead of just 1 group.
		# # numDoubledUpBackslashesInUnreplacedPortion = sum([1  for idx in range(0,len(backrefsInUnreplacedPortion)-1) \
		# # 														if (backrefsInUnreplacedPortion[idx:idx+2] == "\\\\")])
		# numDoubledUpBackslashesInUnreplacedPortion = 0
		# prevCharWasBackslash = False
		# for idx in range(0,len(backrefsInUnreplacedPortion)-1):
		# 	if ((backrefsInUnreplacedPortion[idx:idx+2] == "\\\\") and (not prevCharWasBackslash)):
		# 		numDoubledUpBackslashesInUnreplacedPortion += 1
		# 	# Set up for next iteration without having to do a lookahead.
		# 	prevCharWasBackslash  =  True if backrefsInUnreplacedPortion[idx] == "\\"  else False
		# if DEBUG_LVL>1:
		# 	print("numDoubledUpBackslashesInUnreplacedPortionOfMatch:", numDoubledUpBackslashesInUnreplacedPortion)

		# # I only want to delete doubled-up slashes and doubled-up backslashes, specifically the ones that would appear in a raw (i.e., unescaped) string, and of those, specifically the doubled-up backslashes, and of those, the ones that won't get redacted.
		# redactedSection = "X" * (len(matchedStr) - (len(findAsSingleLengthString) + numDoubledUpBackslashesInUnreplacedPortion))
		# # replacement = f"C:{SLASH}Users{SLASH}{redactedSection}challenges{SLASH}"	# IS VERY BRITTLE. CANNOT TOLERATE MULTIPLE CONTIGUOUS SLASHES, WHETHER FORWARD SLASHES OR BACKWARD SLASHES
		# # replacement    = m.expand(fr"C:\1Users\2{redactedSection}challenges\4".encode("utf-8"))


		# replacementWithoutFiller    = m.expand(fr"C:\1Users\2challenges\4".encode("utf-8"))
		# redactedSection = "X" * (len(re.sub(b"\\\\", b"\\\\\\\\", matchedStr)) - len(replacementWithoutFiller))	# Too long. I need to not replace every backslash with a pair, but rather replace just the won't-be-replaced backslashes.
		# Too long, by the same # of *groups* of backslashes that are present in the unreplacedPortionOfMatchedString
		# unreplacedPart_backslashesToDoubled = re.sub(b"\\\\", b"\\\\\\\\", m.expand(br"\3"))	# In the unreplacedPortionOfMatchedString (i.e., backreference "\3"), replace each "\" with a "\\".
		unreplacedPart_backslashesToDoubled = m.expand(br"\3")
		redactedSection = "X" * (len(unreplacedPart_backslashesToDoubled))

		# replacement    = m.expand(fr"C:\1Users\2{redactedSection}challenges\4".encode("utf-8"))	# Same as line immediately below
		replacement    = m.expand(fr"{leftOfRedaction}{redactedSection}{rightOfRedaction}".encode("utf-8"))
		# replacement = re.sub(b"\\\\", b"\\\\\\\\", replacement)	# Replace any surviving backslashes with doubled-up versions. DO NOT EVER DO THIS.
		if DEBUG_LVL>3:
			try:
				b_matchedItems   = m.expand(fr"\1, \2, \3, \4".encode("utf-8"))
				b_matchedSlashes = m.expand(fr"\1, \2, \4".encode("utf-8"))
				s_matchedItems   = m.expand(fr"\1, \2, \3, \4".encode("utf-8")).decode("utf-8")
				s_matchedSlashes = m.expand(fr"\1, \2, \4".encode("utf-8")).decode("utf-8")
				print("Replacement string (redacted, str):   ", replacement.decode("utf-8"))
				print("Replacement string (redacted, byt): ",   replacement, "\n")
				print(f"Matched items (str):      {s_matchedItems}")
				print(f"Matched items (byt):    {b_matchedItems}\n")
				print(f"Matched slashes (str):    {s_matchedSlashes}")
				print(f"Matched slashes (byt):  {b_matchedSlashes}\n")
			except:
				pass
		elif DEBUG_LVL>2:
			b_matchedItems   = m.expand(fr"\1, \2, \3, \4".encode("utf-8"))
			b_matchedSlashes = m.expand(fr"\1, \2, \4".encode("utf-8"))
			print("Replacement string (redacted, byt): ",   replacement, "\n")
			print(f"Matched items (byt):    {b_matchedItems}")
			print(f"Matched slashes (byt):  {b_matchedSlashes}\n")
		elif DEBUG_LVL>0:
			print("Replacement string (redacted, byt): ", replacement)

		lenInfo = \
			f"* len={len(replacement)} (redacted, byt):  {replacement}\n" + \
			f"* len={len(matchedStr)} (original, byt):  {matchedStr}\n" + \
			f"* len={len(replacement.decode("utf-8"))} (redacted, str):    {replacement.decode("utf-8")}\n" + \
			f"* len={len(matchedStr.decode("utf-8"))} (original, str):    {matchedStr.decode("utf-8")}\n\n"
		if DEBUG_LVL>1:
			print(lenInfo)
		
		assert ((type(replacement) == type(matchedStr)) and (type(replacement) == type("".encode("utf-8")))), "Not comparing apples to apples."
		assert (len(replacement) == len(matchedStr)), \
			"ERROR:\n* Byte-length mismatch between unredacted and redacted strings. PDF will be corrupted after redaction.\n" + \
			f"* TEST: {len(replacement)} == {len(matchedStr)}\n" + \
			"* Ensure that 1) the string being searched for and 2) the string being replaced are the exact same length (byte-wise).\n" + \
			"  * Just because a bytestring and its converted result (to a regular string) seem to have different lengths when printed doesn't mean they actually have different lengths.\n" + \
			lenInfo
		return replacement
	return re.sub(pattern=findAsRegex, repl=replacementCallbackFunc, string=data)



example_testing_file = r"""
C:/Users\\alpha/OneDrive - Google Content Provider/short\\Folder Name/Razorhack 2026/challenges\sheet_music\LearnYour7(or12)ABCs_1
C:/Users/alpha/OneDrive - Google Content Provider/short/Folder Name/Razorhack 2026/challenges/sheet_music/LearnYour7(or12)ABCs_1
C://Users//alpha//OneDrive - Google Content Provider/////short////Folder Name///Razorhack 2026///challenges///////sheet_music///LearnYour7(or12)ABCs_1
C:\Users\alpha\OneDrive - Google Content Provider\short\Folder Name\Razorhack 2026\challenges\sheet_music\LearnYour7(or12)ABCs_1
C:\\Users\\alpha\\OneDrive - Google Content Provider\\short\\Folder Name\\Razorhack 2026\\challenges\\sheet_music\\LearnYour7(or12)ABCs_1

---- ExifTool ----
ExifTool Version Number         : 13.43
---- System ----
File Name                       : LearnYour7(or12)ABCs_1-Tutorial.pdf
Directory                       : C:/Users/alpha/OneDrive - Google Content Provider/short/Folder Name/Razorhack 2026/challenges/sheet_music/LearnYour7(or12)ABCs_1/dist
File Size                       : 65 kB
File Modification Date/Time     : 2026:09:06 17:32:52-05:00
File Access Date/Time           : 2026:09:06 17:42:30-05:00
File Creation Date/Time         : 2026:08:31 20:09:00-05:00
File Permissions                : -rw-rw-rw-
---- File ----

"""





def redactFile(filepathToModify_notToRedactInsideFile:str, output_filepathToModify_notToRedactInsideFile:str, DEBUG_LVL:int = 2):
	from time import sleep
	if (filepathToModify_notToRedactInsideFile == output_filepathToModify_notToRedactInsideFile):
		warningMsg = r"""
	  / \   It's strongly recommended to NOT make the input and output filepaths be the exact same.
	 / ! \  You are very likely to make a mistake in the regex when modifying the search/replace patterns.
	 ``````  , accidentally overwriting your original file.        Your original file may be irreplaceable.

	 Press CTRL and C on your keyboard simultaneously if you want to abort the overwrite.
	"""
		# Sleep for many seconds, allowing user to read the warning.
		printDynamicCountdownTimer(countdownMsg=warningMsg, delayInSec=16)

	
	READ_WRITE_BINARY = "rwb"	# Illegal. `ValueError: must have exactly one of create/read/write/append mode`
	READ_BINARY = "rb"
	WRITE_BINARY = "wb"
	fileContents = ""
	SLASH = "/"

	print("[TIP]  Valid debugging levels:\n* 0[minimal]\n* 1\n* 2\n* 3\n* 4[maximal verbosity]\n")

	with open(filepathToModify_notToRedactInsideFile, READ_BINARY) as f:
		unredactedPaths_fileContents = f.read()
		print(f"\nRead in {len(unredactedPaths_fileContents):,} bytes from file \"{filepathToModify_notToRedactInsideFile}\".\n")

	
	redactedFilepath_fileContents = stripSensitiveFilepath(unredactedPaths_fileContents, SLASH, DEBUG_LVL)

	if DEBUG_LVL>3:
		print(redactedFilepath_fileContents)

	with open(output_filepathToModify_notToRedactInsideFile, WRITE_BINARY) as f:
		f.write(redactedFilepath_fileContents)
		if DEBUG_LVL != 0:
			print()
		print(f"Wrote   {len(redactedFilepath_fileContents):,} bytes to   file \"{output_filepathToModify_notToRedactInsideFile}\".\n")







#################
# CHANGE ME! :) #
#################
# 
filepathToModify_notToRedactInsideFile = "./challenges/zeblegiroctopus/LearnYour7(or12)ABCs_1-Tutorial.pdf"
# 
# output_filepathToModify_notToRedactInsideFile  = filepathToModify_notToRedactInsideFile
output_filepathToModify_notToRedactInsideFile  = \
	filepathToModify_notToRedactInsideFile[:-4]+"-REDACTED_PATH"+filepathToModify_notToRedactInsideFile[-4:]
# 
# print("Output file after redaction:\n", stripSensitiveFilepath(example_testing_file, "/", DEBUG_LVL=5))
print("Output file after redaction:\n", stripSensitiveFilepath(example_testing_file, "/", DEBUG_LVL=2))
# 
# redactFile(filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile, DEBUG_LVL=4)	# Extremely verbose
# redactFile(filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile, DEBUG_LVL=3)
redactFile(filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile, DEBUG_LVL=2)
# redactFile(filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile, DEBUG_LVL=1)
# redactFile(filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile, DEBUG_LVL=0)	# Quiet
