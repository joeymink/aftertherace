from decimal import Decimal, getcontext

def interpret_time(time_str):
	# time_str as <minutes>:<seconds>:<millis>
	split = time_str.split(':')
	minute_s = Decimal(split[0]) * Decimal(60)
	second_s = Decimal(split[1])
	milli_s = Decimal(0.001) * Decimal(split[2])
	return minute_s + second_s + milli_s