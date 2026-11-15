
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
	print(" " * (len(countdownMsg) + len(str(delayInSec)) ), end="\n")





def printFindAsRegex(findAsRegex_humanReadable: list[str]|str, findAsRegex_b4gap: list[str]|str, findAsRegex_gapped: list[str]|str):
	print("\n1) findAsRegex (mentally): ")
	if type(findAsRegex_humanReadable)==list:
		[print("* "+s) for s in findAsRegex_humanReadable]
	else:
		print("*",findAsRegex_humanReadable)
	
	print("\n2) findAsRegex (no gaps):  ")
	if type(findAsRegex_b4gap)==list:
		[print("* "+s) for s in findAsRegex_b4gap]
	else:
		print("*",findAsRegex_b4gap)
	
	print("\n3) findAsRegex (with gaps):")
	if type(findAsRegex_gapped)==list:
		[print("* "+s) for s in findAsRegex_gapped]
	else:
		print("*",findAsRegex_gapped)
	
	print()



def getLengthInfo(replacement:bytes, matchedStr:bytes) -> str:
	lenInfo  = f"* len={len(replacement)} (redacted, byt):  {replacement}\n"
	lenInfo += f"* len={len(matchedStr) } (original, byt):  {matchedStr}\n"
	lenInfo += f"* len={len(replacement.decode("utf-8", errors="replace"))} (redacted, str):    {replacement.decode("utf-8", errors="replace")}\n"
	lenInfo += f"* len={len( matchedStr.decode("utf-8", errors="replace"))} (original, str):    { matchedStr.decode("utf-8", errors="replace")}\n\n"
	return lenInfo

def assertEqualByteLengths(replacement:bytes, matchedStr:bytes):
	assert ((type(replacement) == type(matchedStr)) and (type(replacement) == type("".encode("utf-8")))), "Not comparing apples to apples."
	assert (len(replacement) == len(matchedStr)),  (
		"ERROR:\n* Byte-length mismatch between unredacted and redacted strings. PDF will be corrupted after redaction.\n"
		f"* TEST: {len(replacement)} == {len(matchedStr)}\n"
		"* Ensure that 1) the string being searched for and 2) the string being replaced are the exact same length (byte-wise).\n"
		"  * [NOTE] Just because a bytestring and its converted result (to a regular string) seem to have different lengths *when printed* doesn't mean they actually have different lengths.\n" + 
		getLengthInfo(replacement, matchedStr)
	)



import re
def printDebug_callback(matchobj: re.Match, replacement:bytes, DEBUG_LVL:int, hasPrintedAtLeastOnce:bool, CALLER:str):
	CALLER_IS_FILEPATH = CALLER.lower() in ["filepath", "stripfilepath", "redactfilepath"]
	CALLER_IS_AUTHOR   = CALLER.lower() in [  "author",   "stripauthor",   "redactauthor"]
	assert not (CALLER_IS_FILEPATH and CALLER_IS_AUTHOR),  "It's impossible for two different functions to call this at the same time in the same call."
	# If they're both False, I don't care. That situation is okay.

	m, idx_getAllGroups = matchobj, 0
	matchedStr       =  m.group(idx_getAllGroups)

	if DEBUG_LVL>1:
		print("\nEntire `match` object:             ", m)
		print("Matched string  (v1, byt):          ",  m.string[m.start(idx_getAllGroups) : m.end(idx_getAllGroups)] )
		print("Matched string  (v2, byt):          ",  matchedStr )			# Will be exact same as above line.
	if DEBUG_LVL>2:
		print("Matched string  (v1, str):            ", m.string[m.start(idx_getAllGroups) : m.end(idx_getAllGroups)].decode("utf-8", errors="replace") )
		print("Matched string  (v2, str):            ", matchedStr.decode("utf-8", errors="replace") )
		print("Escaped mstring (3, str):             ", re.escape(matchedStr).decode("utf-8", errors="replace") )
		print("Escaped mstring (3, byt):           ",   re.escape(matchedStr) )	# This escapes everything, which is why I can't use it here...

	# Not actually critical to be in the code, hence its very high debug level.
	if DEBUG_LVL>3 and CALLER_IS_FILEPATH:
		# r"\\\\" will be counted as 4 backslashes
		# Correct, except is counting the full matched string instead of only counting what will NOT get replaced
		numDoubledUpBackslashes = sum([1  for idx in range(0,len(matchedStr)-1) if (matchedStr[idx:idx+2]==r"\\")])
		# numDoubledUpBackslashes = sum([1  for idx in range(0,len(matchedStr)-1) if (idx%2==0 and matchedStr[idx:idx+2]==r"\\")])	# Counts 6pairs instead of 8pairs
		# numDoubledUpBackslashes = ([(1,matchedStr[idx:idx+2])  for idx in range(0, len(matchedStr)-1) if matchedStr[idx:idx+2]==r"\\"])
		# numDoubledUpBackslashes = ([(1,matchedStr[idx:idx+2])  for idx in range(0, len(matchedStr)-1) if (idx%2==0 and matchedStr[idx:idx+2]==r"\\")])
		print("[UNUSED] numDoubledUpBackslashesInEntireMatch:", numDoubledUpBackslashes)


	if DEBUG_LVL>3:
		print("Replacement string (redacted, str):   ", replacement.decode("utf-8", errors="replace"))
		print("Replacement string (redacted, byt): ",   replacement, "\n")
		if CALLER_IS_FILEPATH:
			b_matchedItems   = m.expand(fr"\1, \2, \3, \4".encode("utf-8"))
			b_matchedSlashes = m.expand(fr"\1, \2, \4".encode("utf-8"))
			s_matchedItems   = m.expand(fr"\1, \2, \3, \4".encode("utf-8")).decode("utf-8", errors="replace")
			s_matchedSlashes = m.expand(fr"\1, \2, \4".encode("utf-8")).decode("utf-8", errors="replace")
			print(f"Matched items (str):      {s_matchedItems}")
			print(f"Matched items (byt):    {b_matchedItems}\n")
			print(f"Matched slashes (str):    {s_matchedSlashes}")
			print(f"Matched slashes (byt):  {b_matchedSlashes}\n")
	elif DEBUG_LVL>2:
		print("Replacement string (redacted, byt): ",   replacement, "\n")
		if CALLER_IS_FILEPATH:
			b_matchedItems   = m.expand(fr"\1, \2, \3, \4".encode("utf-8"))
			b_matchedSlashes = m.expand(fr"\1, \2, \4".encode("utf-8"))
			print(f"Matched items (byt):    {b_matchedItems}")
			print(f"Matched slashes (byt):  {b_matchedSlashes}\n")
		elif CALLER_IS_AUTHOR:
			b_matchedItems   = m.expand(fr"\1".encode("utf-8"))
			print(f"Matched items (byt):    {b_matchedItems}")
	elif DEBUG_LVL>0:
		print("Replacement string (redactedBytes): ", replacement)

	
	if not hasPrintedAtLeastOnce:
		if DEBUG_LVL>1:
			print(getLengthInfo(replacement, matchedStr))
	
	


"""
These gapifyXYZ() functions having a gap of *at least*:
* size 2 allows matching even when spanning across a single Windows newline (CR+LF).
* size 6 allows matching even when spanning across {3 Windows newlines (CR+LF)} OR {6 spaces} OR {6 tabs} OR {1 Windows newline with 2 tabs and 2 spaces} OR {2 Windows newline with 1 tab and 1 space} OR ... .

Size -1 (infinity) allows matching even when spanning across thousands of newlines.
* However, longer spans means the regex parser will
  1) backtrack *a lot more* on larger files (causing more lag), and
  2) seemingly-greedily consume extra strings it wasn't meant to (e.g., "<<hi>>ImportantCharsToNotRedactButGetsRedactedAnyway<<hi>>AdditionalImportantChars<<hi>>").
"""

# defaultMaxGapSize WAS set to -1 because defaults should (nearly) always be set to the safest value.
#   If user notices performance issues or too-greedy regex consumption, and the user therefore looks through the code, then they can modify this default value.
#######################
defaultMaxGapSize = 10
#######################

def getGapPattern(maxGapSize:int) -> str:
	DOTALL = r"[\s\S]"	# Matches any character that either: 1) IS a whitespace character, or 2) is NOT a whitespace character.  I.e., matches every character, including those that "dot" won't match (like newlines)
	NONGREEDY_ANY = DOTALL+"*?"		# Greedy: ".*",   Non-Greedy: ".*?"
	if maxGapSize==-1:
		gapMatch = NONGREEDY_ANY
	else:
		gapMatch = DOTALL+"{0,"+str(maxGapSize)+"}"	# Idea behind it: ".{0,2}"
	return gapMatch

def gapifyM(s:str, maxGapSize:int = defaultMaxGapSize) -> str:
	"""
	Insert RegEx chars that allow gaps of characters while still making a match.
	
	Gap is present at: ~L~ = LeftEnd, **M** = Middle, ~R~ = RightEnd.
	
	Example:
	* Hey  ->  H.{0,2}e.{0,2}y	(if maxGapSize ==  2)
	* Hey  ->  H.*e.*y			(if maxGapSize == -1)
	"""

	gapMatch = getGapPattern(maxGapSize)
	# `c if(idx == len(s)-1)`: Don't insert a gap AFTER the last char.
	# `c if(c in ["\\", "*"])`: Don't insert a gap AFTER the "escape" part (\) of an escape char NOR after a "0 or more" quantifier that already consumes gaps.
	return "".join([(c  if((c in ["\\", "*"]) or (idx == len(s)-1))   else c+gapMatch)   for idx,c in enumerate(s)])

def gapifyMR(s:str, maxGapSize:int = defaultMaxGapSize) -> str:
	"""
	Insert RegEx chars (including at the end) that allow gaps of characters while still making a match.
	
	Useful when dealing with substrings.
	
	Gap is present at: ~L~ = LeftEnd, **M** = Middle, **R** = RightEnd.
	
	Example:
	* Hey  ->  H.{0,2}e.{0,2}y.{0,2}	(if maxGapSize ==  2)
	* Hey  ->  H.*e.*y.*				(if maxGapSize == -1)
	"""

	gapMatch = getGapPattern(maxGapSize)
	# `c if(c in ["\\", "*"])`: Don't insert a gap AFTER the "escape" part (\) of an escape char NOR after a "0 or more" quantifier that already consumes gaps.
	return "".join([(c  if(c in ["\\", "*"])   else c+gapMatch)   for c in s])

def gapifyLMR(s:str, maxGapSize:int = defaultMaxGapSize) -> str:
	"""
	Insert RegEx chars (including at the beginning & end) that allow gaps of characters while still making a match.

	Gap is present at: **L** = LeftEnd, **M** = Middle, **R** = RightEnd.

	Example:
	* Hey  ->  .{0,2}H.{0,2}e.{0,2}y.{0,2}	(if maxGapSize ==  2)
	* Hey  ->  .*H.*e.*y.*					(if maxGapSize == -1)
	"""

	gapMatch = getGapPattern(maxGapSize)
	# `c if(c in ["\\", "*"])`: Don't insert a gap AFTER the "escape" part (\) of an escape char NOR after a "0 or more" quantifier that already consumes gaps.
	return "".join([gapMatch] + [(c  if(c in ["\\", "*"])   else c+gapMatch)   for c in s])



def getPatternGappedFilepath() -> str:
	LEGAL_WINDOWS_FILEPATH_CHARS = r"[^\|\?:\*<>\"]" + "*?"
	FP_GAP = LEGAL_WINDOWS_FILEPATH_CHARS + gapifyLMR("")
	# print("gapifyLMR(""):", gapifyLMR(""))
	return FP_GAP

def gapifyFilepathM(s:str) -> str:
	FP_GAP = getPatternGappedFilepath()
	return FP_GAP.join([c for c in s])	# str.join(list)

def gapifyFilepathMR(s:str) -> str:
	FP_GAP = getPatternGappedFilepath()
	return FP_GAP.join([c for c in s]) + FP_GAP

def gapifyFilepathLMR(s:str) -> str:
	FP_GAP = getPatternGappedFilepath()
	return FP_GAP + FP_GAP.join([c for c in s]) + FP_GAP


def stripSensitiveFilepath(data: str|bytes,  SLASH: str,  DEBUG_LVL: int) -> tuple[bytes, int]:
	import re
	# Convert string to bytestream so that file-reading and file-writing can occur, if used before this function is called.
	if type(data) is str:
		data = data.encode("utf-8")
		if DEBUG_LVL>0:
			print("\n[INFO]  Converted data from `str` to UTF-8 `bytes`tream for maximum compatibility with unusual characters possibly present in binary file.")

	NONGREEDY_ANY = ".*?"
	# USE_DOTALL, DOTALL allows parsing across newlines rather than killing and restarting the search upon each newline encountered.
	USE_DOTALL = "(?s)"		# RegEx Flag for `re.DOTALL`. Put this anywhere in the pattern (that ISN'T inside any capture groups)
	DOTALL = r"[\s\S]"	# Matches any character that either: 1) IS a whitespace character, or 2) is NOT a whitespace character.  I.e., matches every character, including those that "dot" won't match (like newlines)
	###########################################################################################
	# CHANGE ME! :)
	# DO NOT ENCODE THIS TO A BYTESTREAM UNTIL AFTER IT'S PULLED INTO A STRING THAT IS ABOUT TO BE ENCODED
	findSlash = "([/\\\\]{0,10})"	# Up to 10 contiguous slashes (like \\) are allowed to be present in text.
	

	# TRY #2
	findAsRegex_humanReadable = r"C:/Users/(.*)challenges/"	# The idea.
	# findAsRegex = rf"(?s)C:/Users/(.*?)challenges/"		# The string that the idea resolves to (without using per-character gaps).
	findAsRegex_b4gap  = USE_DOTALL + f"C:{findSlash}Users{findSlash}("  + NONGREEDY_ANY +  f")challenges{findSlash}"
	findAsRegex_gapped = USE_DOTALL + gapifyFilepathMR("C:") +findSlash+ gapifyFilepathLMR("Users") +findSlash+ "(" \
		+ NONGREEDY_ANY \
		+ ")" + gapifyFilepathMR("challenges") +findSlash + ""

	# TRY #3
	findAsRegex = f"C:{findSlash}Users{findSlash}({NONGREEDY_ANY})challenges{findSlash}".encode("utf-8")
	# TRY #1
	# findAsRegex = f"C:{findSlash}Users{findSlash}(.*)challenges{findSlash}".encode("utf-8")
	leftOfRedaction, rightOfRedaction  =  r"C:\1Users\2",  r"challenges\4"
	###########################################################################################


	hasPrintedAtLeastOnce = False
	if DEBUG_LVL>0:
		print(f"\nstripSensitiveFilepath():\nLooking for all strings that match the following RegEx pattern:\n* {findAsRegex}\n")
		# print(f"\nstripSensitiveFilepath():\nLooking for all strings that match the following RegEx pattern:\n* {findAsRegex_gapped}\n")
		# printFindAsRegex(findAsRegex_humanReadable, findAsRegex_b4gap, findAsRegex_gapped)
	# findAsSingleLengthString = f"C:{SLASH}Users{SLASH}challenges{SLASH}".encode("utf-8")	# No Regex in here, no escape characters in here. Only raw characters.

	def replacementCallbackFunc(matchobj: re.Match) -> bytes:
		# Can't naively delete sensitive data since that messes up file's LUT of memory offsets. So, replace/overwrite it with garbage data of equivalent byte-length.
		m, idx_getAllGroups = matchobj, 0
		matchedStr       =  m.group(idx_getAllGroups)

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

		# print("leftOfRedaction:  ",leftOfRedaction, "\nredactedSection:  ",redactedSection, "\nrightOfRedaction: ",rightOfRedaction)
		# print("\nleftOfRedaction:  ",m.expand(leftOfRedaction.encode("utf-8")), "\nredactedSection:  ",redactedSection, "\nrightOfRedaction: ",m.expand(rightOfRedaction.encode("utf-8")))

		
		# Explicitly allow access inside this function, to the variable that was defined outside this function yet was not passed into this function.		
		nonlocal hasPrintedAtLeastOnce
		# Without the above line:  Error: `cannot access local variable 'hasPrintedAtLeastOnce' where it is not associated with a value`

		if not hasPrintedAtLeastOnce:
			printDebug_callback(m, replacement, DEBUG_LVL, hasPrintedAtLeastOnce, "Filepath")
			# Update the outer function's variable (now that the function is over, no longer depending on the variable being a constant value)
			hasPrintedAtLeastOnce = True
		
		assertEqualByteLengths(replacement, matchedStr)
		

		return replacement

	# Try #2
	# findAsRegex_gapped = findAsRegex_gapped.encode("utf-8")
	# replacedStr, numMatches = re.subn(pattern=findAsRegex_gapped, repl=replacementCallbackFunc, string=data)
	# Try #1
	findAsRegex = findAsRegex
	replacedStr, numMatches = re.subn(pattern=findAsRegex, repl=replacementCallbackFunc, string=data)
	return replacedStr, numMatches




def stripAuthor(data: str|bytes, DEBUG_LVL: int) -> list[tuple[bytes, int]]:
	import re
	# Convert string to bytestream so that file-reading and file-writing can occur, if used before this function is called.
	if type(data) is str:
		data = data.encode("utf-8")
		if DEBUG_LVL>0:
			print("\n[INFO]  Converted data from str to UTF-8 bytestream for maximum compatibility with unusual characters possibly present in binary file.")

	NONGREEDY_ANY = ".*?"
	# USE_DOTALL, DOTALL allows parsing across newlines rather than killing and restarting the search upon each newline encountered.
	USE_DOTALL = "(?s)"		# RegEx Flag for `re.DOTALL`. Put this anywhere in the pattern (that ISN'T inside any capture groups)
	DOTALL = r"[\s\S]"	# Matches any character that either: 1) IS a whitespace character, or 2) is NOT a whitespace character.  I.e., matches every character, including those that "dot" won't match (like newlines)
	findAsRegex_humanReadable, findAsRegex_b4gap, findAsRegex_gapped  =  2*[""], 2*[""], 2*[""]
	###########################################################################################
	# CHANGE ME! :)

	# ENSURE THIS IS NON-GREEDY
	# DO NOT ENCODE THIS TO A BYTESTREAM UNTIL AFTER IT'S PULLED INTO A STRING THAT IS ABOUT TO BE ENCODED (so that debug printing works as expected)

	findAsRegex_humanReadable[0] = "<</Author(.*).*>>"	# The idea.
	# findAsRegex = rf"(?s)(<<\/Author\(.*\).*?>>)"		# The string that the idea resolves to (without using per-character gaps).
	findAsRegex_b4gap[0]  = USE_DOTALL + r"(<<\/Author\(" + NONGREEDY_ANY + r"\)>>)"
	findAsRegex_gapped[0] = USE_DOTALL + "(" + gapifyM(r"<<\/Author\(") + NONGREEDY_ANY + gapifyM(r"\)>>") + ")"

	findAsRegex_humanReadable[1] = "<dc:creator>.*</dc:creator>"	# The idea.
	# findAsRegex = rf"(?s)(<dc:creator>.*?</dc:creator>)"			# The string that the idea resolves to (without using per-character gaps).
	findAsRegex_b4gap[1]  = USE_DOTALL + "(<dc:creator>" + NONGREEDY_ANY + "</dc:creator>)"
	findAsRegex_gapped[1] = USE_DOTALL + "(" + gapifyM("<dc:creator>") + NONGREEDY_ANY + gapifyM("</dc:creator>") + ")"
	###########################################################################################

	if DEBUG_LVL>0:
		printFindAsRegex(findAsRegex_humanReadable, findAsRegex_b4gap, findAsRegex_gapped)
				


	hasPrintedAtLeastOnce = False
	def replacementCallbackFunc(matchobj: re.Match) -> bytes:
		# Can't naively delete sensitive data since that messes up file's LUT of memory offsets. So, replace/overwrite it with garbage data of equivalent byte-length.
		m, idx_getAllGroups = matchobj, 0
		matchedStr       =  m.group(idx_getAllGroups)

		
		# unreplacedPart  = m.expand(fr"\1".encode("utf-8"))	# Same as line immediately below
		unreplacedPart  = m.expand(br"\1")
		redactedSection = "X" * (len(unreplacedPart))	# Plain string, not `bytes`

		replacement    = m.expand(fr"{redactedSection}".encode("utf-8"))
		
		
		nonlocal hasPrintedAtLeastOnce
		if not hasPrintedAtLeastOnce:
			printDebug_callback(m, replacement, DEBUG_LVL, hasPrintedAtLeastOnce, "Author")
			hasPrintedAtLeastOnce = True
		
		
		assertEqualByteLengths(replacement, matchedStr)
		
		return replacement

	replacedStrs, numMatches_list  =  2*[""], 2*[""]
	replacedStrs[0], numMatches_list[0] = re.subn(pattern=findAsRegex_gapped[0].encode("utf-8"),   repl=replacementCallbackFunc,   string=data)
	replacedStrs[1], numMatches_list[1] = re.subn(pattern=findAsRegex_gapped[1].encode("utf-8"),   repl=replacementCallbackFunc,   string=replacedStrs[0])
	return replacedStrs[1], sum(numMatches_list)



def runUnitTest(DEBUG_LVL:int) -> None:
	example_filepath_testing_file = r"""
Single:
C:/Users/alpha/challenges/sheet_music/LearnYour7(or12)ABCs_1
Doubled up:
C:/Users/alpha/challenges/sheet_music/LearnYour7(or12)ABCs_1    C:/Users/alpha/challenges/sheet_music/LearnYour7(or12)ABCs_1

Single:
C:\Users\alpha\challenges\\sheet_music\LearnYour7(or12)ABCs_1
Doubled up:
C:\Users\alpha\challenges\\sheet_music\LearnYour7(or12)ABCs_1   C:\Users\alpha\challenges\\sheet_music\LearnYour7(or12)ABCs_1

123456789
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





	example_author_testing_file = r"""
1)
Single occurrence:
<</Author(Abraham Benedict Charles) /Creator(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) /CreationDate(D:20230402230748-05'00') /ModDate(D:20230402230748-05'00') /Producer(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) >>


Back-to-back Double occurrence:
<</Author(Abraham Benedict Charles) /Creator(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) /CreationDate(D:20230402230748-05'00') /ModDate(D:20230402230748-05'00') /Producer(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) >><</Author(Abraham Benedict Charles) /Creator(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) /CreationDate(D:20230402230748-05'00') /ModDate(D:20230402230748-05'00') /Producer(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) >>


Double occurrence but with newlines & tabs & spaces:
<</Author(Abraham Benedict Charles)
		 /Creator(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5)
	 /CreationDate(D:20230402230748-05'00')
	 /ModDate(D:20230402230748-05'00')
	 /Producer(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) 	
	 >>
	 
<</Author(Abraham Benedict Charles)
		 /Creator(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5)
	 /CreationDate(D:20230402230748-05'00')
	 /ModDate(D:20230402230748-05'00')
	 /Producer(þÿ M i c r o s o f t ®   W o r d   f o r   M i c r o s o f t   3 6 5) 	
>>




2)
Single occurrence:
<dc:creator><rdf:Seq><rdf:li>Abraham Benedict Charles</rdf:li></rdf:Seq></dc:creator>


Back-to-back Double occurrence:
<dc:creator><rdf:Seq><rdf:li>Abraham Benedict Charles</rdf:li></rdf:Seq></dc:creator><dc:creator><rdf:Seq><rdf:li>Abraham Benedict Charles</rdf:li></rdf:Seq></dc:creator>


Double occurrence but with newlines and tabs:
<dc:creator>
	<rdf:Seq>
		<rdf:li>Abraham Benedict Charles</rdf:li>
	</rdf:Seq>
</dc:creator>

<dc:creator>
	<rdf:Seq>
		<rdf:li>Abraham Benedict Charles</rdf:li>
	</rdf:Seq>
</dc:creator>


"""
	redactedFilepaths, _ = stripSensitiveFilepath(example_filepath_testing_file, "/", DEBUG_LVL)
	redactedAuthors,   _ = stripAuthor(example_author_testing_file, DEBUG_LVL)

	print("[INFO]  You should NOT be able to see the author's name nor filepaths in these two outputs.")
	print("Output file after redaction of filepaths:\n",     redactedFilepaths.decode("utf-8", errors="replace"))
	print("\n\n\nOutput file after redaction of authors:\n", redactedAuthors.decode("utf-8", errors="replace"))
	
	
	shouldBeRedacted_Filepath = "alpha"
	shouldBeRedacted_Author = "Abraham Benedict Charles"
	
	# str.find(str)  OR  bytes.find(bytes).  You cannot mix and match `str` and `bytes` when using `find()`.
	idxWithinText_Filepath  = redactedFilepaths.find(shouldBeRedacted_Filepath.encode("utf-8"))

	idxWithinText_Author  = redactedAuthors.find(shouldBeRedacted_Author.encode("utf-8"))
	# VESTIGIAL CODE FOR SEARCHING THROUGH *EACH* REDACTION PROCESS'S RESULTS FOR ANY AUTHOR WHOSE NAME SHOULD'VE BEEN REDACTED.
	# redactedAuthors = stripAuthor(example_author_testing_file, DEBUG_LVL=_DEBUG_LVL)
	# idxWithinText_Author = []
	# for tup2 in redactedAuthors:
	# 	redactedBytestring  =  tup2[0]
	# 	idxFound = redactedBytestring.find(shouldBeRedacted_Author)
	# 	if idxFound != -1:
	# 		idxWithinText_Author.append(idxFound)
	# discoveredIndices_Author = ",".join( [i for i in idxWithinText_Author] )
	# assert len(idxWithinText_Author) == 0, f"TEST FAILED.  You should NOT be able to see the authors in this output. Found \"{shouldBeRedacted_Author}\" at index={discoveredIndices_Author}."

	assert idxWithinText_Filepath == -1,   f"TEST FAILED.  You should NOT be able to see the filepaths in this output. Found \"{shouldBeRedacted_Filepath}\" at index={idxWithinText_Filepath}."
	assert idxWithinText_Author == -1,   f"TEST FAILED.  You should NOT be able to see the authors in this output. Found \"{shouldBeRedacted_Author}\" at index={idxWithinText_Author}."




# This decorator lets me only execute the contents of this method a single time, storing and re-using the returned/output value.
# However, this decorator also means that I can only call this method a single time.
#   The first call can be `self.func()`, but all future calls must be `self.func` to access the result value.
#   If you attempt to call the function two or more times, you'll be executing the output as a function.
#     So, if your decorated function returns `str`, then calling your decorated function a *second* (or more) time will result in something like:
#       filepathAsStr = self.getInputFilepath()
#                       ^^^^^^^^^^^^^^^^^^^^^^^
#       TypeError: 'str' object is not callable
import functools
# @functools.cached_property
# @functools.cache
def getInputFilepath() -> str:
	promptToUser  = "\nProvide either the relative/local or absolute filepath of the file in which you want to redact:\n"
	promptToUser += "* Include the file extension, like \".pdf\"\n"
	promptToUser += "* DO NOT include any backslashes, like \"myDir\\myFile.pdf\"\n"
	promptToUser += "* E.g., \"directoryName/deeperDir/myFile.pdf\" (without the surrounding quotes)\n"
	promptToUser += "> "

	filepathAsStr = input(promptToUser)

	return filepathAsStr



def redactFile(filepathToModify_notToRedactInsideFile:str, output_filepathToModify_notToRedactInsideFile:str,
			   ACCIDENTAL_OVERWRITE_DELAY_SEC:int = 7, DEBUG_LVL:int = 2):
	from time import sleep
	inFile, outFile  =  filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile

	if (inFile == outFile) and (inFile != ""):
		warningMsg = r"""
	  / \   It's strongly recommended to NOT make the input and output filepaths be the exact same.
	 / ! \  You are very likely to make a mistake in the regex when modifying the search/replace patterns.
	 ``````  , accidentally overwriting your original file.        Your original file may be irreplaceable.

	 Press CTRL and C on your keyboard simultaneously if you want to abort the overwrite.

	 Seconds remaining to cancel file-overwrite:  """
		# Sleep for many seconds, allowing user to read the warning.
		printDynamicCountdownTimer(countdownMsg=warningMsg, delayInSec=ACCIDENTAL_OVERWRITE_DELAY_SEC)


	# If filepath is not already provided, then Get filepath from user typing it into the terminal.
	EMPTY_STRING = [None, "", "n/a", "none", "empty", "idk", "unknown"]
	if inFile.lower() in EMPTY_STRING:
		inFile = getInputFilepath()
		outFile = inFile[:-4]+"--REDACTED_PATH+AUTHOR"+inFile[-4:]
	assert outFile.lower() not in EMPTY_STRING, \
		f"Output file's filepath \"{outFile}\" must not be empty."

	
	READ_WRITE_BINARY = "rwb"	# Illegal. `ValueError: must have exactly one of create/read/write/append mode`
	READ_BINARY = "rb"
	WRITE_BINARY = "wb"
	fileContents = ""
	SLASH = "/"

	print("[TIP]  Valid debugging levels for RedactFilepathInsideFile:\n* 0[minimal]\n* 1\n* 2\n* 3\n* 4[maximal verbosity]\n")

	with open(inFile, READ_BINARY) as f:
		unredactedPaths_fileContents = f.read()
		print(f"\nRead in {len(unredactedPaths_fileContents):,} bytes from file \"{inFile}\".\n")


	# Apply the redactions
	redactedFilepath_fileContents, numReplacements_filepaths     = stripSensitiveFilepath(unredactedPaths_fileContents, SLASH, DEBUG_LVL)
	redactedFilepathAuthor_fileContents, numReplacements_authors = stripAuthor(redactedFilepath_fileContents, DEBUG_LVL)
	# Shorten the variable name
	redactedFileContents = redactedFilepathAuthor_fileContents

	if DEBUG_LVL>0:
		print(f"[INFO]  Replaced a filepath string {numReplacements_filepaths} times.")
		print(f"[INFO]  Replaced an author string {numReplacements_authors} times.")
		print()

	if DEBUG_LVL>3:
		print("==== Redacted file contents ====\n")
		print("* With only filepaths redacted:")
		print(redactedFilepath_fileContents)
		print("\n\n* With both author and filepaths redacted:")
		print(redactedFilepathAuthor_fileContents,"\n\n")
	elif DEBUG_LVL>1:
		print("Redacted file contents (of both author and filepaths)(bytes):\n", redactedFilepathAuthor_fileContents,"\n\n")
		print("Redacted file contents (of both author and filepaths)(str):\n",   redactedFilepathAuthor_fileContents.decode("utf-8", errors="replace"),"\n\n")
	elif DEBUG_LVL>0:
		print("Redacted file contents (of both author and filepaths)(str):\n",   redactedFilepathAuthor_fileContents.decode("utf-8", errors="ignore"),"\n\n")

	with open(outFile, WRITE_BINARY) as f:
		f.write(redactedFileContents)
	if DEBUG_LVL != 0:
		print()
	print(f"[INFO]  Wrote   {len(redactedFileContents):,} bytes to   file \"{outFile}\".\n")









#################
# CHANGE ME! :) #
#################


DO_TEST = False
USE_RELATED_FILEPATH = True
USE_USER_PROVIDED_FILEPATH = True

if DO_TEST:
	# runUnitTest(DEBUG_LVL = 5)
	runUnitTest(DEBUG_LVL = 2)

else:
	if USE_USER_PROVIDED_FILEPATH:
		# Providing redactFile() with both filepaths being "" means it'll prompt the user to provide a filepath.
		filepathToModify_notToRedactInsideFile = ""
		output_filepathToModify_notToRedactInsideFile  = filepathToModify_notToRedactInsideFile
	else:
		# filepathToModify_notToRedactInsideFile = "./challenges/zeblegiroctopus/LearnYour7(or12)ABCs_1-Tutorial.pdf"
		filepathToModify_notToRedactInsideFile = "C:/Users/<YOUR_COMPUTER'S_NAME_GOES_HERE>/Desktop/Blank PDF.pdf"
		
		if USE_RELATED_FILEPATH:
			output_filepathToModify_notToRedactInsideFile  = \
				filepathToModify_notToRedactInsideFile[:-4]+"--REDACTED_PATH+AUTHOR"+filepathToModify_notToRedactInsideFile[-4:]
		else:
			output_filepathToModify_notToRedactInsideFile = "C:/Users/<YOUR_COMPUTER'S_NAME_GOES_HERE>/Desktop/Blank PDF - Redacted.pdf"
	
	
	# DEBUG_LVL=4 is Extremely verbose.  DEBUG_LVL=0 is Quiet
	redactFile(filepathToModify_notToRedactInsideFile, output_filepathToModify_notToRedactInsideFile, DEBUG_LVL=1)
