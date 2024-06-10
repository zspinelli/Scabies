
"""def _increment_ordinator_string(ord_string: str) -> str:
	# saftey mechanism.
	if not ord_string:
		return ""

	i: int = len(ord_string)

	while True:
		front: str = ord_string[:i - 1]
		back: str = ord_string[i:]
		ord_val: int = ord(ord_string[i - 1])

		# rollover everything and increase length.
		if all(char == 'z' for char in ord_string):
			ord_string = '0' * (len(ord_string) + 1)
			break

		# rollover from '9' to 'a'.
		if ord_val == 57:
			ord_string = front + "a" + back
			break

		# rollover from 'z' to '0'.
		elif ord_val == 122:
			ord_string = front + "0" + back
			i -= 1

		# increment 0-9, or a-z.
		elif ord_val < 57 or ord_val < 122:
			ord_string = front + chr(ord_val + 1) + back
			break

	return ord_string"""


def _increment_ordinator_string(ord_string: str) -> str:
	# saftey mechanism.
	if not ord_string:
		return ""

	i: int = len(ord_string)

	while True:
		front: str = ord_string[:i - 1]
		back: str = ord_string[i:]
		ord_val: int = ord(ord_string[i - 1])

		# rollover everything and increase length.
		if all(char == 'z' for char in ord_string):
			ord_string = '0' * (len(ord_string) + 1)
			break

		# rollover from '-' to '0'.
		if ord_val == 45:
			ord_string = front + "0" + back
			break

		# rollover from '9' to 'a'.
		elif ord_val == 57:
			ord_string = front + "a" + back
			break

		# rollover from 'z' to '-' or '0'.
		elif ord_val == 122:
			# rollover to '-' or '0'.
			if len(ord_string) > i > 0:
				ord_string = front + "-" + back
			else:
				ord_string = front + "0" + back

			i -= 1

		# increment 0-9, or a-z.
		elif ord_val < 57 or ord_val < 122:
			ord_string = front + chr(ord_val + 1) + back
			break

	return ord_string


hash: str = "0-0"

while hash != "z" * 6:
	group_hash: str = f"{hash}"
	print(f"testing: {group_hash} ... ")
	hash = _increment_ordinator_string(hash)
